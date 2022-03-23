from django import forms
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import BookReviewForm, MeetingForm
from clubs.models import Book, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class SetBookTestCase(TestCase ,LogInTester):
    """Unit tests of the set up meeting form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',

        ]

    def setUp(self):
        self.default_user = User.objects.get(username='johndoe')
        self.default_club = Club.objects.get(name='Oxford Book Club')
        self.default_book = Book.objects.get(isbn= "0195153448")
        self.url = reverse('book')
       
    def test_set_book_uses_correct_template(self):
        pass