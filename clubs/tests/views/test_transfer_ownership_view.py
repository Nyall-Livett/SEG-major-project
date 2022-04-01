from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Notification
from clubs.tests.helpers import LogInTester, reverse_with_next


class TransferOwnershipTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json',
    ]

    def setUp(self):
        self.default_user = User.objects.get(username='johndoe')
        self.secondary_user = User.objects.get(username='janedoe')
        self.default_club = Club.objects.get(pk=1)
        self.secondary_club = Club.objects.get(pk=2)
        self.url = reverse('transfer_ownership')

    # Test URL is correct
    def test_url(self):
        self.assertEqual(self.url, '/transfer_ownership/')

    # Test post access case for users
    def test_post_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    # Test for when new leader is not a member of the club
    def test_returns_403_when_new_leader_not_a_member(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertTrue(self.secondary_user not in self.default_club.members.all())
        self.assertEqual(self.default_user, self.default_club.leader)
        response = self.client.post(self.url, {
            'club_id': f'"{self.default_club.id}"',
            'new_leader_id': f'"{self.secondary_user.id}"'
        },
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 403)

    # Test for when current user is not the leader
    def test_returns_403_when_current_user_not_leader(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertNotEqual(self.default_user, self.secondary_club.leader)
        response = self.client.post(self.url, {
            'club_id': '"2"',
            'new_leader_id': '"1"'
        },
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 403)

    # Test transfer completes okay
    def test_transfer_ownership_to_new_user(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertEqual(self.default_user, self.default_club.leader)
        self.default_club.members.add(self.secondary_user)
        self.default_club.refresh_from_db()
        self.assertTrue(self.secondary_user in self.default_club.members.all())
        response = self.client.post(self.url, {
            'club_id': '"1"',
            'new_leader_id': '"2"'
        },
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.default_club.refresh_from_db()
        self.assertEqual(self.secondary_user, self.default_club.leader)


    def test_notification_gets_sent(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        before_count = Notification.objects.count()
        self.assertEqual(before_count, 0)
        self.assertEqual(self.default_user, self.default_club.leader)
        self.default_club.members.add(self.secondary_user)
        self.default_club.refresh_from_db()
        self.assertTrue(self.secondary_user in self.default_club.members.all())
        response = self.client.post(self.url, {
            'club_id': '"1"',
            'new_leader_id': '"2"'
        },
            **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        )
        self.assertEqual(response.status_code, 200)
        self.default_club.refresh_from_db()
        self.assertEqual(self.secondary_user, self.default_club.leader)
        after_count = Notification.objects.count()
        self.assertEqual(after_count, 1)
