from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
class CustomUser(AbstractUser):
 
    USER_TYPE_CHOICES = (
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    )
 # Override email to make it required and unique
    email = models.EmailField(unique=True, blank=False)

    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default='patient'
    )
    
    # Profile picture with upload path
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text='Upload a profile picture'
    )
    
    # Phone validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Additional fields
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True
    )
    
    # Address fields
    address_line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
    
    @property
    def full_address(self):
        """Returns formatted complete address"""
        address_parts = [
            self.address_line1,
            self.city,
            self.state,
            self.pincode
        ]
        return ', '.join(filter(None, address_parts))