from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class FollowRequestTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.followee = User.objects.get(username='janedoe')
        self.url = reverse('follow_request', kwargs={'user_id': self.followee.id})

    def test_follow_request_url(self):
        self.assertEqual(self.url,f'/follow_request/{self.followee.id}')

    def test_get_follow_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_follow_request_for_follower(self):
        self.client.login(username=self.user.username, password='Password123')
        user_sent_requests_before = self.user.sent_requests.count()
        user_followees_count_before = self.user.followees_count()
        self.user.send_follow_request(self.followee)
        response = self.client.get(self.url, follow=True)
        user_followees_count_after = self.user.followees_count()
        user_sent_requests_after = self.user.sent_requests.count()
        self.assertEqual(user_followees_count_before, user_followees_count_after)
        self.assertEqual(user_sent_requests_before+1, user_sent_requests_after)
        response_url = reverse('show_user', kwargs={'user_id': self.followee.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_user.html')

    def test_get_follow_request_for_followee(self):
        self.client.login(username=self.user.username, password='Password123')
        followee_follow_request_before = self.followee.follow_requests.count()
        followee_follower_count_before = self.followee.followers_count()
        self.user.send_follow_request(self.followee)
        response = self.client.get(self.url, follow=True)
        followee_follow_request_after = self.followee.follow_requests.count()
        followee_follower_count_after = self.followee.followers_count()
        self.assertEqual(followee_follower_count_before, followee_follower_count_after)
        self.assertEqual(followee_follow_request_before+1, followee_follow_request_after)
        response_url = reverse('show_user', kwargs={'user_id': self.followee.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_user.html')

    def test_get_follow_request_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('follow_request', kwargs={'user_id':self.followee.id+1000000})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "user_list.html")
        

