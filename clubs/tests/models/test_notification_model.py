"""Unit tests for the notification model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Notification

class NotificationModelTestCase(TestCase):
    """Unit tests for the notification model."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_notification.json',
    ]

    def setUp(self):
        self.default_notification = Notification.objects.get(pk=1)
        pass

    def test_valid_notification(self):
        self._assert_notification_is_valid()

    def test_title_can_be_128_characters_long(self):
        self.default_notification.title = 'x' * 128
        self._assert_notification_is_valid()

    def test_title_cannot_be_over_128_characters_long(self):
        self.default_notification.title = 'x' * 129
        self._assert_notification_is_invalid()

    def test_title_must_not_be_blank(self):
        self.default_notification.title= ''
        self._assert_notification_is_invalid()

    def test_notification_must_have_receiver(self):
        self.default_notification.receiver = None
        self._assert_notification_is_invalid()

    def _assert_notification_is_valid(self):
        try:
            self.default_notification.full_clean()
        except (ValidationError):
            self.fail('Test notification should be valid')

    def _assert_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_notification.full_clean()
