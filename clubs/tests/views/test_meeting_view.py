from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Meeting, Book
from clubs.forms import MeetingForm
from clubs.tests.helpers import LogInTester, reverse_with_next



class MeetingTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        #'clubs/tests/fixtures/default_meeting.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',
        ]

    def setUp(self):
        self.url = reverse('set_meeting')
        self.default_user = User.objects.get(username='johndoe')
        #self.default_meeting = Meeting.objects.get(date='2022-01-27 11:00:00')
        self.default_club = Club.objects.get(name='Oxford Book Club')
        self.default_book = Book.objects.get(isbn= "0195153448")

        self.form_input = {
            #"date": "2022-02-27 11:00:00",
            "date": "2022-02-27 11:00:00",
            "URL": "www.aaa.com",
            "club":1,
            "notes": "This is a note.",
            "book":1,
            "members":1
        }





    # Test URL is correct
    def test_set_meeting_url(self):
        self.assertEqual(self.url,'/set_meeting/')
    '''
    # Test new meeting has been created mark 1
    def test_create_new_meeting(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        meeting_count_before = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        meeting_count_after = Meeting.objects.count()
        self.assertEqual(meeting_count_before, meeting_count_after-1)
    '''

    # Test the correct template is rendered
    def test_get_meeting_gives_correct_used(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'set_meeting.html')

    # Test the current user is the also the host of meeting
    """def test_current_user_is_meeting_host(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        meeting_count_before = Meeting.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        meeting_count_after = Meeting.objects.count()
        self.assertEqual(meeting_count_before, meeting_count_after-1)
        meeting = Meeting.objects.get(name=self.form_name)
        self.assertEqual(meeting.founder, self.default_user)"""

    # Test new club has current user as member mark 2
    """def test_current_user_is_in_club_members_after_creating(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_before, club_count_after-1)
        club = Club.objects.get(name=self.form_name)
        self.assertTrue(club.members.filter(username=self.default_user.username).exists())"""

    # Test the form is not bound
    def test_form_is_not_bound_upon_arrival(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    # Test the form is bound after submitting an invalid form mark3
    def test_form_is_bound_after_being_invalid(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['url'] = ""
        response = self.client.post(self.url, self.form_input, follow=True)
        form = response.context['form']
        self.assertTrue(form.is_bound)

    # Test correct message is being rendered
    """def test_correct_message_is_shown_after_creation(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), f"You have successfully created {self.form_input['name']}.")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)"""
