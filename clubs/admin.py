"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from .models import User, Club


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Club)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'name', 'description', 'founder',
    ]
