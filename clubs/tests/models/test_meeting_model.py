"""Unit tests for the Meeting model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Meeting, Book

class MeetingModelTestCase(TestCase):
    """Unit tests for the Meeting model."""

    fixtures = [
        "clubs/tests/fixtures/default_user.json",
        "clubs/tests/fixtures/default_club.json",
        #'clubs/tests/fixtures/other_clubs.json',
        #"clubs/tests/fixtures/default_meeting.json",
        "clubs/tests/fixtures/default_book.json",
        #'clubs/tests/fixtures/other_books.json',

    ]

    def setUp(self):


        self.default_user = User.objects.get(username='johndoe')
        #self.default_meeting = Meeting.objects.get(date='2022-01-27 11:00:00')
        self.default_club = Club.objects.get(name='Oxford Book Club')
        self.default_book = Book.objects.get(isbn= "0195153448")
        self.default_meeting = Meeting(
            date="2022-01-27 11:00:00",
            club=self.default_club,
            book= self.default_book,
            location="Online",
            URL="www.aaa.com",
            notes="This is a note.",
            )

    def test_valid_meeting(self):
        self._assert_meeting_is_valid()

    def test_date_cannot_be_blank(self):
        self.default_meeting.date = ''
        self._assert_meeting_is_invalid()

    def test_meeting_must_have_club(self):
        self.default_meeting.club = None
        self._assert_meeting_is_invalid()

    def test_meeting_may_not_have_book(self):
        self.default_meeting.book = None
        self._assert_meeting_is_valid()

    def test_date_must_not_be_blank(self):
        self.default_meeting.date = ''
        self._assert_meeting_is_invalid()

    def test_notes_may_be_blank(self):
        self.default_meeting.notes = ''
        self._assert_meeting_is_valid()

    def test_location_may_be_blank(self):
        self.default_meeting.location = ''
        self._assert_meeting_is_valid()

    def test_URL_may_be_blank(self):
        self.default_meeting.URL = ''
        self._assert_meeting_is_valid()

    def test_passcode_may_be_blank(self):
        self.default_meeting.passcode = ''
        self._assert_meeting_is_valid()

    def test_meeting_must_not_be_more_than_100_characters(self):
        self.default_meeting.passcode = 'a' * 101
        self._assert_meeting_is_invalid()

    def test_meeting_may_be_less_than_100_or_100_characters(self):
        self.default_meeting.passcode = 'a' * 100
        self._assert_meeting_is_valid()

    def _assert_meeting_is_valid(self):
        try:
            self.default_meeting.full_clean()
        except (ValidationError):
            self.fail('Test meeting should be valid')

    def _assert_meeting_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_meeting.full_clean()
