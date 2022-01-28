"""Unit tests for the Club model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User

class ClubModelTestCase(TestCase):
    """Unit tests for the Club model."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.default_club = Club.objects.get(name='Oxford Book Club')

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_name_cannot_be_blank(self):
        self.default_club.name = ''
        self._assert_club_is_invalid()

    def test_name_can_be_64_characters_long(self):
        self.default_club.name = 'x' * 64
        self._assert_club_is_valid()

    def test_name_cannot_be_over_64_characters_long(self):
        self.default_club.name = 'x' * 65
        self._assert_club_is_invalid()

    def test_name_must_be_unique(self):
        other_club = Club.objects.get(name='London Book Club')
        self.default_club.name = other_club.name
        self._assert_club_is_invalid()

    def test_name_may_contain_non_alphanumericals(self):
        self.default_club.name = '0xford B00k Club'
        self._assert_club_is_valid()

    def test_name_may_contain_numbers(self):
        self.default_club.name = 'Oxford Book Club 2022'
        self._assert_club_is_valid()

    def test_description_may_contain_2048_characters(self):
        self.default_club.description = 'x' * 2048
        self._assert_club_is_valid()

    def test_description_must_not_contain_more_than_2048_characters(self):
        self.default_club.description = 'x' * 2049
        self._assert_club_is_invalid()

    def test_description_must_not_be_blank(self):
        self.default_club.description = ''
        self._assert_club_is_invalid()

    def test_theme_must_not_be_blank(self):
        self.default_club.theme = ''
        self._assert_club_is_invalid()

    def test_theme_may_contain_512_characters(self):
        self.default_club.theme = 'x' * 512
        self._assert_club_is_valid()

    def test_theme_must_not_contain_more_than_512_characters(self):
        self.default_club.theme = 'x' * 513
        self._assert_club_is_invalid()

    def test_maximum_members_must_not_be_less_than_2(self):
        self.default_club.maximum_members = 1
        self._assert_club_is_invalid()

    def test_maximum_members_can_be_2_characters(self):
        self.default_club.maximum_members = 2
        self._assert_club_is_valid()

    def test_maximum_members_can_be_64_characters(self):
        self.default_club.maximum_members = 64
        self._assert_club_is_valid()

    def test_maximum_members_must_not_be_more_than_64(self):
        self.default_club.maximum_members = 65
        self._assert_club_is_invalid()

    def test_club_must_have_leader(self):
        self.default_club.leader = None
        self._assert_club_is_invalid()

    def _assert_club_is_valid(self):
        try:
            self.default_club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_club.full_clean()
