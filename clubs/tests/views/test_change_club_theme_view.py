from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class ChangeClubThemeTest(TestCase, LogInTester):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.club = Club.objects.get(pk=1)
        self.url = reverse('change_theme', kwargs={'club_id': self.club.id})


    def test_set_meeting_URL(self):
        self.assertEqual(self.url, f'/change_theme/{self.club.id}')

    def test_change_theme_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'change_theme.html')

    def test_change_club_theme_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_leader_can_access_change_club_theme(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_change_theme_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(reverse('change_theme', kwargs={'club_id': self.club.id}), 
        {'theme': 'new_theme'})
        self.assertEqual(response.status_code, 302)
        self.club.refresh_from_db()
        self.assertEqual(self.club.theme, 'new_theme')