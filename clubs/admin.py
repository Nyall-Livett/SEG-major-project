"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from .models import Book, Club, Meeting, User

class MembershipInline(admin.TabularInline):
    model = Club.members.through

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    inlines = [
        MembershipInline,
        ]
    exclude = ('password',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'name', 'description', 'leader',
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
