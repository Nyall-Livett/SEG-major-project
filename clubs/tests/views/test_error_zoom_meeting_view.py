from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class ErrorZoomMeetingTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json'
    ]
    
    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('zoom_meeting')

    def test_error_zoom_meeting_url(self):
        self.assertEqual(self.url, f'/zoom_meeting/')

    def test_error_zoom_meeting_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_error_zoom_meeting_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'error_zoom_meeting.html')
