"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from .models import Book, Club, Meeting, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active',
    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'description', 'founder',
    ]

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for meetings."""

    list_display = [
        'date', 
    ]

@admin.register(Book)
class MeetingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for books."""

    list_display = [
        'name', 'description',
    ]





