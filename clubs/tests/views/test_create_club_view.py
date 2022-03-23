from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next


class CreateClubTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/recommendations_books',
    ]

    def setUp(self):
        self.url = reverse('create_club')
        self.default_user = User.objects.get(username='johndoe')
        self.form_name = 'Oxford Book Club'
        self.form_input = {
            'name': f'{self.form_name}',
            'description': 'Book club based in oxfordshire',
            'theme': 'Humor',
            'maximum_members': 2
        }

    # Test URL is correct
    def test_log_in_url(self):
        self.assertEqual(self.url,'/create_club/')

    # Test get access case for users
    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    # Test post access case for users
    def test_post_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    # Test new club has been created
    def test_create_new_club(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_before, club_count_after-1)

    # Test the correct template is rendered
    def test_get_clubs_gives_correct_template_used(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')

    # Test the current user is the also the leader of new club
    def test_current_user_is_club_leader(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_before, club_count_after-1)
        club = Club.objects.get(name=self.form_name)
        self.assertEqual(club.leader, self.default_user)

    # Test new club has current user as member
    def test_current_user_is_in_club_members_after_creating(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_before, club_count_after-1)
        club = Club.objects.get(name=self.form_name)
        self.assertTrue(club.members.filter(username=self.default_user.username).exists())

    # Test the form is not bound
    def test_form_is_not_bound_upon_arrival(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertFalse(form.is_bound)

    # Test the form is bound after submitting an invalid form
    def test_form_is_bound_after_being_invalid(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        self.form_input['name'] = ""
        response = self.client.post(self.url, self.form_input, follow=True)
        form = response.context['form']
        self.assertTrue(form.is_bound)

    # Test correct message is being rendered
    def test_correct_message_is_shown_after_creation(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.post(self.url, self.form_input, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), f"You have successfully created {self.form_input['name']}.")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
