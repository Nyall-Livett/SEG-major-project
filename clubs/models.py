"""Models in the clubs app."""
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar
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

class Club(models.Model):
    """Club model"""
    name = models.CharField(max_length=64, unique=True, blank=False)
    description = models.CharField(max_length=2048, blank=False)
    founder = models.ForeignKey(User, related_name="founder_of", on_delete=models.PROTECT)
    members = models.ManyToManyField(User, symmetrical=True, related_name="clubs")

    def add_member(self, user):
        if user not in self.members.all():
            user.clubs.add(self)

    def grant_ownership(self, user):
        self.founder = user
        self.save()

    def __str__(self):
        return self.name

class Book(models.model):
    name = models.CharField(max_length=64, unique=True, blank=False)
    description = models.CharField(max_length=2048, blank=False)
    

class Meeting(models.model):
    date = models.DateTimeField("date", default=timezone.now)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="members")
    book = models.ManyToManyField(Book, related_name="book")



