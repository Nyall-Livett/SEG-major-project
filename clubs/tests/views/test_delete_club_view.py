from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class DeleteClubTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(id=1)
        self.url = reverse('delete_club', kwargs = {'club_id' : self.club.id})

    def test_delete_club_url(self):
        self.assertEqual(self.url, f'/delete_club/{self.club.id}')

    def test_delete_club_redirects_when_user_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_delete_club_when_leader(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        before = Club.objects.count()
        response = self.client.post(self.url, follow=True)
        after = Club.objects.count()
        self.assertEqual(before-1, after)

    def test_delete_club_when_not_leader(self):
        self.other_user = User.objects.get(username='janedoe')
        self.client.login(username=self.other_user, password='Password123')
        before = Club.objects.count()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 404)
        after = Club.objects.count()
        self.assertEqual(before, after)
