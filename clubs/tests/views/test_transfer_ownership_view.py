from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class TransferOwnershipTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.default_user = User.objects.get(username='johndoe')
        self.secondary_user = User.objects.get(username='janedoe')
        self.default_club = Club.objects.get(pk=1)
        self.url = reverse('transfer_ownership', args=[self.secondary_user.pk, self.default_club.pk])

    # Test URL is correct
    def test_url(self):
        self.assertEqual(self.url, '/transfer_ownership/2/1')

    # Test post access case for users
    def test_post_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    # Test new club has been created
    def test_transfer_ownership_to_new_user(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertEqual(self.default_user, self.default_club.leader)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.default_club.refresh_from_db()
        self.assertEqual(self.secondary_user, self.default_club.leader)

    # Test for correct exception when current user is not the club leader
    def test_exception_when_not_leader(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.assertEqual(self.default_user, self.default_club.leader)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.default_club.refresh_from_db()
        self.assertEqual(self.secondary_user, self.default_club.leader)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 403)

    # Test for correct redirect url after passing ownership
    def test_correct_redirect_after_passing_ownership(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
    # Test correct message is being rendered

    def test_correct_message_is_shown_after_creation(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), f"You have successfully passed leadership of {self.default_club.name} to {self.secondary_user.full_name()}.")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
