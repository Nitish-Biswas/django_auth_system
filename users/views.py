from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .forms import SignUpForm, LoginForm
from .models import CustomUser

# ======= AJAX Validation Views ========

@require_http_methods(["POST"])
def check_username_availability(request):
    """AJAX endpoint to check if username is available"""
    username = request.POST.get('username', '').strip()
    if not username:
        return JsonResponse({
            'available': False,
            'message': 'Username is required',
            'type': 'error'
        })
    
    #Check length
    if len(username) < 3:
        return JsonResponse({
            'available': False,
            'message': 'Username must be at least 3 characters',
            'type': 'error'
        })
    
    #Check if username exists
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({
            'available': False,
            'message': 'This username is already taken',
            'type': 'error'
        })
    
    return JsonResponse({
        'available': True,
        'message': 'Username is available',
        'type': 'success'
    })

@require_http_methods(["POST"])
def check_email_availability(request):
    """AJAX endpoint to check if email is available"""
    email = request.POST.get('email', '').strip().lower()
    if not email:
        return JsonResponse({
            'available': False,
            'message': 'Email is required',
            'type': 'error'
        })
    
    #Basic email format validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return JsonResponse({
            'available': False,
            'message': 'Invalid email format',
            'type': 'error'
        })
    
    #Check if email exists
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({
            'available': False,
            'message': 'This email address is already registered',
            'type': 'error'
        })
    
    return JsonResponse({
        'available': True,
        'message': 'Email is available',
        'type': 'success'
    })

@require_http_methods(["POST"])
def validate_password(request):
    """AJAX endpoint to validate password strength"""
    password = request.POST.get('password', '')
    
    if not password:
        return JsonResponse({
            'valid': False,
            'message': 'Password is required',
            'strength': 'weak',
            'type': 'error'
        })

    #Password strength checks
    issues = []
    strength = 'weak'
    valid = False

    if len(password) < 8:
        issues.append('At least 8 characters')
    if not re.search(r'[A-Z]', password):
        issues.append('One uppercase letter')
    if not re.search(r'[a-z]', password):
        issues.append('One lowercase letter')
    if not re.search(r'[0-9]', password):
        issues.append('One number')
    if not re.search(r'[!@#$%^&*()..?":{}|<>]', password): # Adjusted special chars
        issues.append('One special character')

    #Determine strength
    if len(issues) == 0:
        strength = 'strong'
        message = 'Strong password'
        valid = True
    elif len(issues) <= 2:
        strength = 'medium'
        message = 'Medium strength. Add: ' + ', '.join(issues)
        valid = True # Still valid, but medium
    else:
        strength = 'weak'
        message = 'Weak password. Needs: ' + ', '.join(issues)
        valid = False

    return JsonResponse({
        'valid': valid,
        'message': message,
        'strength': strength,
        'issues': issues,
        'type': 'success' if valid and strength != 'weak' else 'warning'
    })

# ==================== Original Views ====================

@never_cache
@require_http_methods(["GET", "POST"])
def signup_view(request):
    """Handle user registration for both Patient and Doctor"""
    if request.user.is_authenticated:
        return redirect('users:dashboard_redirect')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                #Log the user in automatically after signup
                login(request, user)
                messages.success(
                    request,
                    f'Welcome {user.get_full_name()}! Your account has been created successfully.'
                )
                #Redirect to appropriate dashboard
                return redirect('users:dashboard_redirect')
            except Exception as e:
                messages.error(
                    request,
                    f'An error occurred during registration: {str(e)}'
                )
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    
    context = {
        'form': form,
        'title': 'Sign Up'
    }
    return render(request, 'users/signup.html', context)

@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('users:dashboard_redirect')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f'Welcome back, {user.get_full_name()}!'
                )
                #Redirect to next page or dashboard
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('users:dashboard_redirect')
            else:
                messages.error(
                    request,
                    'Invalid username or password. Please try again.'
                )
        else:
            messages.error(
                request,
                'Invalid username or password. Please try again.'
            )
    else:
        form = LoginForm()
        
    context = {
        'form': form,
        'title': 'Login'
    }
    return render(request, 'users/login.html', context)

@login_required
def logout_view(request):
    """Handle user logout"""
    user_name = request.user.get_full_name()
    logout(request)
    messages.info(request, f'Goodbye {user_name}! You have been logged out successfully.')
    return redirect('users:login')

@login_required
def dashboard_redirect(request):
    """Redirect users to their respective dashboards based on user type"""
    if request.user.user_type == 'patient':
        return redirect('users:patient_dashboard')
    elif request.user.user_type == 'doctor':
        return redirect('users:doctor_dashboard')
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('users:login')

@login_required
def patient_dashboard(request):
    """Dashboard for Patient users"""
    #Verify user is actually a patient
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied. You are not a patient.')
        return redirect('users:dashboard_redirect')
    
    context = {
        'user': request.user,
        'title': 'Patient Dashboard'
    }
    return render(request, 'users/patient_dashboard.html', context)

@login_required
def doctor_dashboard(request):
    """Dashboard for Doctor users"""
    #Verify user is actually a doctor
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied. You are not a doctor.')
        return redirect('users:dashboard_redirect')
    
    context = {
        'user': request.user,
        'title': 'Doctor Dashboard'
    }
    return render(request, 'users/doctor_dashboard.html', context)
#     Handle user registration for both Patient and Doctor
#     """
#     if request.user.is_authenticated:
#         return redirect('users:dashboard_redirect')
    
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             try:
#                 user = form.save()
                
#                 # Log the user in automatically after signup
#                 login(request, user)
                
#                 messages.success(
#                     request,
#                     f'Welcome {user.get_full_name()}! Your account has been created successfully.'
#                 )
                
#                 # Redirect to appropriate dashboard
#                 return redirect('users:dashboard_redirect')
            
#             except Exception as e:
#                 messages.error(
#                     request,
#                     f'An error occurred during registration: {str(e)}'
#                 )
#         else:
#             # Display form errors
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f'{field}: {error}')
#     else:
#         form = SignUpForm()
    
#     context = {
#         'form': form,
#         'title': 'Sign Up'
#     }
#     return render(request, 'users/signup.html', context)
# @never_cache
# @require_http_methods(["GET", "POST"])
# def login_view(request):

#     if request.user.is_authenticated:
#         return redirect('users:dashboard_redirect')
    
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
        
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
            
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 messages.success(
#                     request,
#                     f'Welcome back, {user.get_full_name()}!'
#                 )
                
#                 # Redirect to next page or dashboard
#                 next_url = request.GET.get('next')
#                 if next_url:
#                     return redirect(next_url)
                
#                 return redirect('users:dashboard_redirect')
#             else:
#                 messages.error(
#                     request,
#                     'Invalid username or password. Please try again.'
#                 )
#         else:
#             messages.error(
#                 request,
#                 'Invalid username or password. Please try again.'
#             )
#     else:
#         form = LoginForm()
    
#     context = {
#         'form': form,
#         'title': 'Login'
#     }
#     return render(request, 'users/login.html', context)
# @login_required
# def logout_view(request):
#     """
#     Handle user logout
#     """
#     user_name = request.user.get_full_name()
#     logout(request)
#     messages.info(request, f'Goodbye {user_name}! You have been logged out successfully.')
#     return redirect('users:login')
# @login_required
# def dashboard_redirect(request):
#     """
#     Redirect users to their respective dashboards based on user type
#     """
#     if request.user.user_type == 'patient':
#         return redirect('users:patient_dashboard')
#     elif request.user.user_type == 'doctor':
#         return redirect('users:doctor_dashboard')
#     else:
#         messages.error(request, 'Invalid user type.')
#         return redirect('users:login')
# @login_required
# def patient_dashboard(request):
#     """
#     Dashboard for Patient users
#     """
#  # Verify user is actually a patient
#     if request.user.user_type != 'patient':
#         messages.error(request, 'Access denied. You are not a patient.')
#         return redirect('users:dashboard_redirect')
#     context = {
#     'user': request.user,
#     'title': 'Patient Dashboard'
#     }
#     return render(request, 'users/patient_dashboard.html', context)

# @login_required
# def doctor_dashboard(request):
#     """
#     Dashboard for Doctor users
#     """
#  # Verify user is actually a doctor
#     if request.user.user_type != 'doctor':
#         messages.error(request, 'Access denied. You are not a doctor.')
#         return redirect('users:dashboard_redirect')
#     context = {
#     'user': request.user,
#     'title': 'Doctor Dashboard'
#     }
#     return render(request, 'users/doctor_dashboard.html', context)