from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class ChangeClubDetailsTest(TestCase, LogInTester):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other = User.objects.get(pk=2)
        self.club = Club.objects.get(pk=1)
        self.other_club = Club.objects.get(pk=2)
        self.url = reverse('change_club_details', kwargs={'club_id': self.club.id})


    def test_set_meeting_URL(self):
        self.assertEqual(self.url, f'/change_club_details/{self.club.id}')

    def test_change_club_details_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'change_club_details.html')

    def test_change_club_club_details_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_leader_can_access_change_club_club_details(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_change_club_details_view(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(reverse('change_club_details', kwargs={'club_id': self.club.id}),
        {'theme': 'Fiction'})
        self.assertEqual(response.status_code, 200)
        self.club.refresh_from_db()
        self.assertEqual(self.club.theme, 'Fiction')

    def test_other_than_leader_will_recieve_404_when_trying_to_update_club_details(self):
        self.client.login(username = self.other.username, password = 'Password123')
        response = self.client.post(reverse('change_club_details', kwargs={'club_id': self.club.id}),
        {'theme': 'Humor', 'name':'ox', 'description':'sjbdsa', 'maximum_members':'20', 'city':'London'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.club.theme, 'Fiction')
