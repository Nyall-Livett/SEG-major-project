from django.test import TestCase
from django.urls import reverse
from clubs.models import Notification
from clubs.models import User, Notification
from clubs.tests.helpers import LogInTester, reverse_with_next


class MarkAllNotActedUponNotificationsTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_notification.json',
        'clubs/tests/fixtures/other_notifications.json'
    ]

    def setUp(self):
        self.url = reverse('notification_mark_all_not_acted_upon')
        self.seen_url = reverse('notification_mark_all_acted_upon')
        self.default_user = User.objects.get(pk = 1)
        self.default_notification = Notification.objects.get(pk = 1)

    def test_url(self):
        self.assertEqual(self.url,'/notification_mark_all_not_acted_upon/')

    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_get_access_for_authenticated_throws_405(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, {'notifications': '["1"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 405)

    def test_returns_status_code_200(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, {'notifications': '["1"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)

    def test_notification_acted_upon_to_false(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertTrue(self.default_notification.acted_upon == False)
        response = self.client.post(self.seen_url, {'notifications': '["1"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.default_notification.refresh_from_db()
        self.assertTrue(self.default_notification.acted_upon == True)
        response = self.client.post(self.url, {'notifications': '["1"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.default_notification.refresh_from_db()
        self.assertTrue(self.default_notification.acted_upon == False)

    def test_multiple_notifications_gets_acted_upon_at_once_false(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        notification_count = Notification.objects.count()
        not_acted_upon_count = Notification.objects.filter(acted_upon=False).count()
        self.assertEqual(not_acted_upon_count, notification_count)
        response = self.client.post(self.seen_url, {'notifications': '["1","2","3","4"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        acted_upon_count = Notification.objects.filter(acted_upon=True).count()
        self.assertEqual(acted_upon_count, notification_count)
        response = self.client.post(self.url, {'notifications': '["1","2","3","4"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        not_acted_upon_count = Notification.objects.filter(acted_upon=False).count()
        self.assertEqual(not_acted_upon_count, notification_count)
