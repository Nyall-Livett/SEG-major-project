from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Notification
from clubs.tests.helpers import LogInTester, reverse_with_next


class DeleteNotificationTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_notification.json',
    ]

    def setUp(self):
        self.url = reverse('notification_delete')
        self.default_user = User.objects.get(pk = 1)


    # Test URL is correct
    def test_log_in_url(self):
        self.assertEqual(self.url,'/notification_delete/')

    # Test get access case for users
    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_notification_gets_deleted(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = Notification.objects.count()
        response = self.client.post(self.url, {'notifications': '["1"]'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        count_after = Notification.objects.count()
        self.assertEqual(count_before -1, count_after)
