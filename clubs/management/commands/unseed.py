from django.core.management.base import BaseCommand, CommandError
from clubs.models import User, Post, Club, Book, Meeting

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):

        Post.objects.all().delete()
        Club.objects.all().delete()
        Book.objects.all().delete()
        Meeting.objects.all().delete()
        User.objects.filter(is_staff=False).delete()
