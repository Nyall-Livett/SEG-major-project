"""Configuration of the admin interface for clubs."""
from django.contrib import admin
from .models import Book, Club, Meeting, User, Post, BooksRead

class MembershipInline(admin.TabularInline):
    model = Club.members.through

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    #inlines = [
        #MembershipInline,
        #]
    #exclude = ('password',)

    list_display = [
        'id', 'username', 'first_name', 'last_name', 'email',
    ]


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for clubs."""

    list_display = [
        'id', 'name', 'description', 'leader', 'image'
    ]

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for meetings."""

    list_display = [
        'id', 'date', 'club',
    ]

@admin.register(BooksRead)
class BooksReadAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for books read."""

    list_display = [
        'id', 'reviewer', 'book', 'rating',
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for posts."""

    list_display = [
        'club','author','title', 'body',
    ]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for books."""

    list_display = [
        'isbn', 'name', 'author',
    ]
