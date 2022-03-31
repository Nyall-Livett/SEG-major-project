"""Unit tests for the notification model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club, User, Notification
from clubs.enums import NotificationType
from clubs.factories.notification_factory import CreateNotification


class NotificationModelTestCase(TestCase):
    """Unit tests for the notification model."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/default_notification.json',
    ]

    def setUp(self):
        self.default_user = User.objects.get(pk=1)
        self.default_club = Club.objects.get(pk=1)
        self.default_notification = Notification.objects.get(pk=1)
        self.notifier = CreateNotification()

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

    def test_description_must_not_be_blank(self):
        self.default_notification.description= ''
        self._assert_notification_is_invalid()

    def test_description_can_be_256_characters_long(self):
        self.default_notification.description = 'x' * 256
        self._assert_notification_is_valid()

    def test_description_cannot_be_over_257_characters_long(self):
        self.default_notification.description = 'x' * 257
        self._assert_notification_is_invalid()

    def test_notification_must_have_receiver(self):
        self.default_notification.receiver = None
        self._assert_notification_is_invalid()

    def test_notification_must_have_created_on(self):
        self.default_notification.created_on = None
        self._assert_notification_is_invalid()

    def test_acted_upon_defaults_to_false(self):
        self.assertFalse(self.default_notification.acted_upon)

    def test_read_defaults_to_false(self):
        self.assertFalse(self.default_notification.read)

    def test_notification_must_have_created_on(self):
        self.default_notification.created_on = None
        self._assert_notification_is_invalid()

    def test_type_cannot_be_out_of_range(self):
        self.default_notification.type = 99999
        self._assert_notification_is_invalid()

    def test_title_is_correct_for_FOLLOW_REQUEST(self):
        self.notifier.notify(NotificationType.FOLLOW_REQUEST, self.default_user, {'user': self.default_user})
        latest_notification = Notification.objects.last()
        self.assertEqual(latest_notification.title, "Follow request")

    def test_title_is_correct_for_MEETING_SOON(self):
        self.notifier.notify(NotificationType.MEETING_CREATED, self.default_user, {'club': self.default_club})
        latest_notification = Notification.objects.last()
        self.assertEqual(latest_notification.title, "Meeting scheduled")

    def test_title_is_correct_for_CLUB_CREATED(self):
        self.notifier.notify(NotificationType.CLUB_CREATED, self.default_user, {'club': self.default_club})
        latest_notification = Notification.objects.last()
        self.assertEqual(latest_notification.title, "Club created")

    def test_title_is_correct_for_CLUB_JOINED(self):
        self.notifier.notify(NotificationType.CLUB_JOINED, self.default_user, {'club': self.default_club})
        latest_notification = Notification.objects.last()
        self.assertEqual(latest_notification.title, "Club joined")

    def test_title_is_correct_for_CLUB_RECEIVED(self):
        self.notifier.notify(NotificationType.CLUB_RECEIVED, self.default_user, {'club': self.default_club})
        latest_notification = Notification.objects.last()
        self.assertEqual(latest_notification.title, "Received club leadership")

    def _assert_notification_is_valid(self):
        try:
            self.default_notification.full_clean()
        except (ValidationError):
            self.fail('Test notification should be valid')

    def _assert_notification_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.default_notification.full_clean()
