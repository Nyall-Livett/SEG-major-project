from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User
from clubs.tests.helpers import reverse_with_next, LogInTester

class ClubListTest(TestCase, LogInTester):
    
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.url = reverse('club_list')
        self.user = User.objects.get(pk=1)
        self.club = Club.objects.get(name='Oxford Book Club')
        self.form_input = {}
    
    def test_club_list_url(self):
        self.assertEqual(self.url,'/clubs/')
    
    

    def test_post_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)