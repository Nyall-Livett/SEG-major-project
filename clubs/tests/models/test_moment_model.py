"""Unit tests for the Moment model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Moment, Book
from clubs.enums import MomentType

class MomentModelTestCase(TestCase):
    """Unit tests for the Moment model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/default_club.json",
        "clubs/tests/fixtures/default_book.json",
    ]

    def setUp(self):

        self.default_user = User.objects.get(username='johndoe')
        self.default_club = Club.objects.get(name='Oxford Book Club')
        self.default_book = Book.objects.get(isbn= "0195153448")

        self.default_moment = Moment(
            body='This is a moment',
            type= MomentType.CUSTOM,
            user= self.default_user
        )


    def test_valid_moment(self):
        self._assert_moment_is_valid()


    def _assert_moment_is_valid(self):
        try:
            self.default_moment.full_clean()
        except (ValidationError):
            self.fail('Test moment should be valid')

    def _assert_moment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_moment.full_clean()
