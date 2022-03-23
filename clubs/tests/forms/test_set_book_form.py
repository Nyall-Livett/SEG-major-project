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
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.book = Book.objects.get(isbn= "0195153448")
        self.url = reverse('book')
       
    def test_set_book_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'set_book.html')

    def test_set_book_redirects_when_user_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
