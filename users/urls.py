from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    #Authentication URLS
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    #Dashboard URLS
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    
    #AJAX Validation URLS
    path('ajax/check-username/', views.check_username_availability, name='check_username'),
    path('ajax/check-email/', views.check_email_availability, name='check_email'),
    path('ajax/validate-password/', views.validate_password, name='validate_password'),
]