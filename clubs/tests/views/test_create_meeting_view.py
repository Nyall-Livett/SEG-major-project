from django.test import TestCase
from django.urls import reverse
from clubs.models import Notification, User, Club, Meeting
from clubs.tests.helpers import LogInTester, isUrlLegit
from datetime import datetime, timedelta
import pytz

class MeetingTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        utc=pytz.UTC
        self.user = User.objects.get(pk=1)
        self.club = Club.objects.get(pk=1)
        self.book = Club.objects.get(pk=1)
        self.url = reverse('set_meeting', kwargs={'club_id': self.club.id})
        self.form_input = {
            'start': datetime.now().replace(tzinfo=utc) + timedelta(days=1),
            'finish': datetime.now().replace(tzinfo=utc) + timedelta(days=2),
            'location': 'London',
            'book': self.book.id,
            'notes': 'This is a meeting for test purposes'
        }
        self.club.add_or_remove_member(User.objects.get(pk=2))
        self.club.add_or_remove_member(User.objects.get(pk=3))
        self.club.add_or_remove_member(User.objects.get(pk=4))

    def test_set_meeting_URL(self):
        self.assertEqual(self.url, f'/set_meeting/{self.club.id}')

    def test_create_meeting_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'set_meeting.html')

    def test_create_meeting_with_correct_correct_form_data_creates_a_new_meeting(self):
        self.client.login(username=self.user.username, password='Password123')
        meeting_count_before = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        meeting_count_after = Meeting.objects.count()
        response_url = reverse('show_club', kwargs={'club_id': self.club.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertEqual(meeting_count_before+1, meeting_count_after)

    def test_create_meeting_with_incorrect_form_data_does_not_create_new_meeting(self):
        self.form_input['notes'] = 'a'*301
        self.client.login(username='johndoe', password='Password123')
        meeting_count_before = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        meeting_count_after = Meeting.objects.count()
        self.assertEqual(meeting_count_before, meeting_count_after)
        self.assertTemplateUsed(response, 'set_meeting.html')

    def test_form_is_not_bound_upon_arrival(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_form_is_bound_after_being_invalid(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['notes'] = 'a'*301
        response = self.client.post(self.url, self.form_input, follow=True)
        form = response.context['form']
        self.assertTrue(form.is_bound)

    def test_form_has_error_messeges_after_being_invalid(self):
        self.client.login(username=self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['start'] = 'wrong date format'
        response = self.client.post(self.url, self.form_input, follow=True)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['start'][0], 'Enter a valid date/time.')
        self.assertTemplateUsed(response, 'set_meeting.html')

    def test_meeting_URL_works_after_creating_meeting(self):
        self.client.login(username=self.user.username, password='Password123')
        meetings_before = Meeting.objects.all()
        meetings_before_pk_list = []
        for meeting in meetings_before:
            meetings_before_pk_list.append(meeting.id)
        response = self.client.post(self.url, self.form_input, follow=True)
        meetings_after = Meeting.objects.all()
        self.assertEqual(len(meetings_before)+1, len(meetings_after))
        meetings_after_pk_list = []
        for meeting in meetings_after:
            meetings_after_pk_list.append(meeting.id)
        recently_created_meeting = None
        for pk in meetings_after_pk_list:
            if pk not in meetings_before_pk_list:
                recently_created_meeting = Meeting.objects.get(id=pk)
                break
        self.assertTrue(recently_created_meeting is not None)
        site_url = recently_created_meeting.URL
        if site_url != 'KeyError':
            self.assertTrue(isUrlLegit(site_url))
            
    def test_creating_meeting_creates_notification_for_all_users_of_the_club(self):
        self.client.login(username=self.user.username, password='Password123')
        club = Club.objects.get(id=1)
        user_one = User.objects.get(id=2)
        user_two = User.objects.get(id=3)
        club.add_or_remove_member(user_one)
        notification_before = Notification.objects.count()
        self.client.post(self.url, self.form_input, follow=True)
        notification_after = Notification.objects.count()
        self.assertTrue(notification_before+2, notification_after)