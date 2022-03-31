"""Unit tests for the Moment view."""
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Moment, Book, Post
from clubs.enums import MomentType
from clubs.tests.helpers import reverse_with_next

class MomentViewTestCase(TestCase):
    """Unit tests for the Moment model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/default_book.json",
    ]

    def setUp(self):

        self.url = reverse('create_moment')
        self.user = User.objects.get(pk = 1)

    def test_url(self):
        self.assertEqual(self.url,'/create_moment/')

    def test_new_moment_posted(self):
        form_input = {
            'moment_body': 'This is a test moment'
        }
        self.client.login(username=self.user.username, password="Password123")
        moment_count_before = Moment.objects.count()
        response = self.client.post(self.url, form_input, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        moment_count_after = Moment.objects.count()
        self.assertEqual(moment_count_after, moment_count_before + 1)
        self.assertEqual(response.status_code, 200)
