"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from .models import User, Club, Meeting

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
    """Configuration of the admin interface for Club"""
    
    inlines = [
        MembershipInline,
    ]
    exclude = ('members',)

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for Meeting"""

    list_display = ['date', 'club', 'URL' ,'member_selected', 'next_book' ,'meeting_notes',]
