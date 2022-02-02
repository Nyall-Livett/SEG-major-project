"""Models in the clubs app."""
from pickle import TRUE
from re import T
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import request
from libgravatar import Gravatar
from django.utils import timezone
from datetime import date, datetime
from django.core.validators import MaxValueValidator, MinValueValidator
import pytz

"""used for meeting model"""
from django.utils import timezone
from datetime import date

class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)

    class Meta:
        """Model options."""
        ordering = ['last_name', 'first_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)

    def future_meetings(self):
        utc=pytz.UTC
        list = []
        for i in Meeting.objects.all():
            if i.date.replace(tzinfo=utc) > datetime.now().replace(tzinfo=utc):
                list.append(i)
        return list

    def previous_meetings(self):
        utc=pytz.UTC
        list = []
        for i in Meeting.objects.all():
            if i.date.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):
                list.append(i)
        return list
    def notification_count(self):
        return self.notification_set.filter(read=False).count()

    def get_unread_notifications(self):
        return self.notification_set.filter(read=False)

    def clubBooks(self):
        list = []
        for i in Book.objects.all():
                list.append(i)
        return len(list) > 0



class Club(models.Model):
    """Club model"""
    name = models.CharField(max_length=64, unique=True, blank=False)
    description = models.CharField(max_length=2048, blank=False)
    leader = models.ForeignKey(User, related_name="leader_of", on_delete=models.PROTECT)
    members = models.ManyToManyField(User, symmetrical=True, related_name="clubs")
    theme = models.CharField(max_length=512, blank=False)
    maximum_members = models.IntegerField(blank=False, default=2, validators=[MinValueValidator(2), MaxValueValidator(64)])

    def add_member(self, user):
        if user not in self.members.all():
            user.clubs.add(self)

    def remove_member(self, user):
        if user in self.members.all():
            user.clubs.remove(self)

    def grant_leadership(self, user):
        self.leader = user
        self.save()

    def member_count(self):
        return f"{self.members.count()}/{self.maximum_members}"

    def __str__(self):
        return self.name

    def is_member(self,request):
        for i in self.members.all():
            if request == i:
                return True
        return False


class Notification(models.Model):
    """Notification model."""
    title = models.CharField(max_length=128, blank=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length = 64, blank=False)
    body = models.CharField(max_length = 300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club,on_delete=models.CASCADE, related_name="club")
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author")

    class Meta:
        """Model options."""
        ordering = ['-created_at']


class Book(models.Model):
    """Book model"""
    isbn = models.CharField(max_length=13, unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=2048)
    author = models.CharField(max_length=64, blank=False)
    publication_year = models.CharField(max_length=4)
    publisher = models.CharField(max_length=64)
    image_url_s = models.URLField(max_length=200)
    image_url_m = models.URLField(max_length=200)
    image_url_l = models.URLField(max_length=200)

    class Meta:
        """Model options."""
        ordering = ['isbn']

    def __str__(self):
        return self.name

class Meeting(models.Model):
    """Meeting model"""
    date = models.DateTimeField("date", default=timezone.now)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="members")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    notes = models.CharField(max_length=300, blank=True)


    def add_meeting(self, meeting):
        if meeting not in self.meeting.all():
            meeting.meeting_members.add(self)
