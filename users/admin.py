
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'user_type', 'is_staff', 'created_at'
    ]
    
    list_filter = ['user_type', 'is_staff', 'is_active', 'created_at']
    
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'user_type', 'profile_picture', 'phone_number',
                'address_line1', 'city', 'state', 'pincode'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': (
                'user_type', 'email', 'first_name', 'last_name',
                'profile_picture', 'phone_number',
                'address_line1', 'city', 'state', 'pincode'
            )
        }),
    )