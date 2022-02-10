from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class ShowFollowersTest(TestCase):   

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('show_following', kwargs={'user_id':self.user.id})

    def test_followers_list_url(self):
        self.assertEqual(self.url, f'/show_following/{self.user.id}')

    def test_followers_page_context_contains_right_no_of_followers_when_has_followers(self):
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.client.login(username='johndoe', password='Password123')
        self.user.send_follow_request(jane)
        self.user.send_follow_request(petra)
        self.user.send_follow_request(peter)
        jane.accept_request(self.user)
        petra.accept_request(self.user)
        peter.accept_request(self.user)
        no_of_user_followees = self.user.followees_count()
        response = self.client.get(self.url, follow=True)
        no_of_user_followees_in_context = len(response.context['followees'])
        self.assertEqual(no_of_user_followees_in_context, no_of_user_followees)
        self.assertTemplateUsed(response, 'followee.html')

    def test_followers_page_context_contains_right_no_of_followers_when_has_no_followers(self):
        self.client.login(username='johndoe', password='Password123')
        no_of_user_followees = self.user.followees_count()
        response = self.client.get(self.url, follow=True)
        no_of_user_followees_in_context = len(response.context['followees'])
        self.assertEqual(no_of_user_followees_in_context, no_of_user_followees)
        self.assertTemplateUsed(response, 'followee.html')

    def test_show_followers_with_invalid_id(self):
        self.client.login(username='johndoe', password='Password123')
        url = reverse('show_following', kwargs={'user_id':100000000000})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')

    

