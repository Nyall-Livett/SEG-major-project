from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next
from clubs.models import Moment
from django.contrib import messages

class FollowToggleTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.followee = User.objects.get(username='janedoe')
        self.url = reverse('accept_request', kwargs={'user_id': self.followee.id})

    def test_accept_request_url(self):
        self.assertEqual(self.url,f'/accept_request/{self.followee.id}')

    def test_get_accept_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_moments_created_after_user_accepts_follow_request(self):
        moments_before_accept = Moment.objects.all().count()
        self.client.login(username=self.user.username, password='Password123')
        self.followee.send_follow_request(self.user)
        self.user.accept_request(self.followee)
        response = self.client.get(self.url, follow=True)
        moments_after_accept = Moment.objects.all().count()
        self.assertEqual(moments_before_accept+2, moments_after_accept)
        user_moment = Moment.objects.get(id=1)
        self.assertEqual(user_moment.type, 1)
        self.assertEqual(user_moment.user, self.user)
        self.assertEqual(user_moment.associated_user.id, self.followee.id)
        followee_moment = Moment.objects.get(id=2)
        self.assertEqual(followee_moment.type, 1)
        self.assertEqual(followee_moment.user, self.followee)
        self.assertEqual(followee_moment.associated_user.id, self.user.id)

    def test_get_accept_request_for_followee(self):
        self.client.login(username=self.user.username, password='Password123')
        user_follow_requests_before = self.user.follow_requests.count()
        user_followers_count_before = self.user.followers_count()
        self.followee.send_follow_request(self.user)
        user_follow_requests_after = self.user.follow_requests.count()
        user_followers_count_after = self.user.followers_count()
        self.assertEqual(user_follow_requests_before+1, user_follow_requests_after)
        self.assertEqual(user_followers_count_before, user_followers_count_after)
        self.user.accept_request(self.followee)
        response = self.client.get(self.url, follow=True)
        user_follow_requests_after_accept = self.user.follow_requests.count()
        user_followers_count_after_accept = self.user.followers_count()
        self.assertEqual(user_follow_requests_after, user_follow_requests_after_accept+1)
        self.assertEqual(user_followers_count_after+1, user_followers_count_after_accept)
        response_url = reverse('show_user', kwargs={'user_id': self.followee.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_user.html')

    def test_get_follow_toggle_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('accept_request', kwargs={'user_id': self.followee.id+100000})
        response = self.client.get(url, follow=True)
        response_url = reverse('follow_requests_page')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'follow_requests.html')

    def test_correct_message_is_shown_after_rejecting_follow_request(self):
        self.followee.send_follow_request(self.user)
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('accept_request', kwargs={'user_id': self.followee.id})
        response = self.client.get(url, follow=True)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "You have successfully accepted follow request from {user}".format(user=self.followee.username))
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
