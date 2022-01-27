"""Unit tests for the Meeting model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Meeting

class MeetingModelTestCase(TestCase):
    """Unit tests for the Meeting model."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json',
        'clubs/tests/fixtures/default_meeting.json'

    ]

    def setUp(self):
        self.default_meeting = Meeting.objects.get(date='2022-01-27 11:00:00')

    def test_valid_meeting(self):
        self._assert_meeting_is_valid()

    def test_date_cannot_be_blank(self):
        self.default_meeting.date = ''
        self._assert_meeting_is_invalid()

    def test_notes_can_be_3000_characters_long(self):
        self.default_meeting.meeting_notes = 'x' * 64
        self._assert_meeting_is_valid()

    def test_club_cannot_be_over_64_characters_long(self):
        self.default_meeting.club = 'x' * 65
        self._assert_meeting_is_invalid()

    def test_notes_may_contain_numbers(self):
        self.default_meeting.club= '2022'
        self._assert_meeting_is_valid()

    def test_members_may_contain_3000_characters(self):
        self.default_meeting.member_selected = 'x' * 2048
        self._assert_meeting_is_valid()

    def test_date_must_not_be_blank(self):
        self.default_meeting.date = ''
        self._assert_meeting_is_invalid()

    def _assert_meeting_is_valid(self):
        try:
            self.default_meeting.full_clean()
        except (ValidationError):
            self.fail('Test meeting should be valid')

    def _assert_meeting_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_meeting.full_clean()
