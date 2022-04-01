from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class ClubViewTest(TestCase, LogInTester):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.url = reverse('show_club', kwargs = {'club_id' : self.club.id})
        self.profile_url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': 'johndoe2',
            'email': 'johndoe2@example.org',
            'bio': 'New bio',
        }

    def test_club_url(self):
        self.assertEqual(self.url, f'/club/{self.club.id}')
    
    def test_redirect_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.profile_url)
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_correct_template_used(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')

    def test_club_id_does_not_exist_redirects(self):
        self.client.login(username = self.user.username, password = "Password123")
        self.assertTrue(self._is_logged_in())
        non_existing_club_url = reverse('show_club', kwargs = {'club_id' : 900})
        response = self.client.get(non_existing_club_url)
        self.assertEquals(response.status_code, 302)

    

    



