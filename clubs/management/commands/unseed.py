from django.core.management.base import BaseCommand
from clubs.models import User, Post, Club, Book, Meeting, Moment, Notification, BooksRead
from ...helpers import delete_ratings

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        self.delete_user_ratings()
        Post.objects.all().delete()
        Club.objects.all().delete()
        Book.objects.all().delete()
        Meeting.objects.all().delete()
        User.objects.filter(is_staff=False).delete()
        Moment.objects.all().delete()
        Notification.objects.all().delete()
        BooksRead.objects.all().delete()

    def delete_user_ratings(self):
        users = User.objects.filter(is_staff=False)
        for user in users:
            user_id = user.id
            delete_ratings(user_id)
