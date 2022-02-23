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
from clubs.enums import NotificationType, MomentType

import pytz
import random


class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="followees")
    follow_requests = models.ManyToManyField('self', symmetrical=False, related_name='sent_requests')

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
        return self.gravatar(size=50)

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

    def now(self):
        utc=pytz.UTC
        return datetime.now().replace(tzinfo=utc)

    #def applicants(self):


    def notification_count(self):
        return self.notification_set.filter(read=False).count()

    def get_unread_notifications(self):
        return self.notification_set.filter(read=False)

    def notifications_not_acted_upon_count(self):
        return self.notification_set.filter(acted_upon=False).count()

    def clubBooks(self):
        list = []
        for i in Book.objects.all():
                list.append(i)
        return len(list) > 0

    """ methods relating to follow system """
    def add_follower(self, user):
        """ add other users as followers to self """
        self.followers.add(user)

    def follow(self, user):
        """ follow user """
        self.followees.add(user)

    def unfollow(self, user):
        """ unfollow user self is following """
        self.followees.remove(user)

    def followers_count(self):
        """ number of followers self has """
        return self.followers.count()

    def followees_count(self):
        """ number of users self follows """
        return self.followees.count()

    def is_following(self, user):
        """ returns if self follows a given user """
        return user in self.followees.all()

    def toggle_follow(self, user):
        """ unfollows if self follows the user, follows if self does not follow the user """
        if self.is_following(user):
            self.unfollow(user)
        else:
            self.follow(user)

    """ methods relating to follow requests """
    def send_follow_request(self, user):
        """ send follow requests to a user """
        self.sent_requests.add(user)

    def is_request_sent(self, user):
        """ returns if a follow request to a user has already been sent """
        return user in self.sent_requests.all()

    def has_request(self, user):
        """ returns if a follow request has been sent by a user """
        return user in self.follow_requests.all()

    def accept_request(self, user):
        """ accepts a follow request from a user """
        if self.has_request(user):
            self.follow_requests.remove(user)
            self.add_follower(user)

    def reject_request(self, user):
        """ rejects a follow request from a user """
        if self.has_request(user):
            self.follow_requests.remove(user)


class Club(models.Model):
    """Club model"""
    name = models.CharField(max_length=64, unique=True, blank=False)
    description = models.CharField(max_length=2048, blank=False)
    leader = models.ForeignKey(User, related_name="leader_of", on_delete=models.PROTECT)
    members = models.ManyToManyField(User, symmetrical=True, related_name="clubs")
    applicants = models.ManyToManyField(User,blank=True, related_name="applicants" )
    theme = models.CharField(max_length=512, blank=False)
    maximum_members = models.IntegerField(blank=False, default=2, validators=[MinValueValidator(2), MaxValueValidator(64)])

    def add_or_remove_member(self, user):
        if user not in self.members.all():
            user.clubs.add(self)
        else:
            user.clubs.remove(self)

    def applicant_manager(self, user):
        if user not in self.applicants.all():
            user.applicants.add(self)

    def acceptmembership(self, user):
        user.applicants.remove(self)
        user.clubs.add(self)

    def rejectmembership(self,user):
        user.applicants.remove(self)

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
    type = models.IntegerField(blank=False, default = NotificationType.DEFAULT, choices = NotificationType.choices)
    description = models.CharField(max_length=256, blank=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    acted_upon = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
    associated_user = models.IntegerField(blank=True, null=True)
    associated_club = models.IntegerField(blank=True, null=True)

class Moment(models.Model):
    """docstring for Moments."""

    body = models.CharField(blank=False, max_length=128)
    type = models.IntegerField(blank=False, choices = MomentType.choices)
    likes = models.IntegerField(blank=False, default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
    associated_user = models.IntegerField(blank=True, null=True)
    associated_club = models.IntegerField(blank=True, null=True)


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

# default values are used for any existing instances of books.
class Book(models.Model):
    """Book model"""
    isbn = models.CharField(max_length=13, unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=2048, blank=True)
    author = models.CharField(max_length=64, blank=False)
    publication_year = models.CharField(max_length=4, blank=True)
    publisher = models.CharField(max_length=64, blank=True)
    image_url_s = models.URLField(max_length=200, blank=True)
    image_url_m = models.URLField(max_length=200, blank=True)
    image_url_l = models.URLField(max_length=200, blank=True)

    class Meta:
        """Model options."""
        ordering = ['isbn']

    def __str__(self):
        return self.name

class Meeting(models.Model):
    """Meeting model"""
    date = models.DateTimeField("date", default=timezone.now)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="meetings")
    members = models.ManyToManyField(User, related_name="members")
    chosen_member = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    URL = models.CharField(max_length=300, blank=True)
    notes = models.CharField(max_length=300, blank=True)


    def add_meeting(self, meeting):
        if meeting not in self.meeting.all():
            meeting.meeting_members.add(self)

    def get_random_member(self):
        list = []
        for i in self.members.all():
            list.append(i)
        return random.choice(list)
