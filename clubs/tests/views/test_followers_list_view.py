from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class ShowFollowersTest(TestCase):   

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.url = reverse('show_followers', kwargs={'user_id':self.user.id})

    def test_followers_list_url(self):
        self.assertEqual(self.url, f'/show_followers/{self.user.id}')

    def test_followers_page_context_contains_right_no_of_followers_when_has_followers(self):
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.client.login(username='johndoe', password='Password123')
        jane.send_follow_request(self.user)
        petra.send_follow_request(self.user)
        peter.send_follow_request(self.user)
        self.user.accept_request(jane)
        self.user.accept_request(petra)
        self.user.accept_request(peter)
        no_of_user_followers = self.user.followers_count()
        response = self.client.get(self.url, follow=True)
        no_of_user_followers_in_context = len(response.context['followers'])
        self.assertEqual(no_of_user_followers_in_context, no_of_user_followers)
        self.assertTemplateUsed(response, 'followers.html')

    def test_followers_page_context_contains_right_no_of_followers_when_has_no_followers(self):
        self.client.login(username='johndoe', password='Password123')
        no_of_user_followers = self.user.followers_count()
        response = self.client.get(self.url, follow=True)
        no_of_user_followers_in_context = len(response.context['followers'])
        self.assertEqual(no_of_user_followers_in_context, no_of_user_followers)
        self.assertTemplateUsed(response, 'followers.html')

    def test_show_followers_with_invalid_id(self):
        self.client.login(username='johndoe', password='Password123')
        url = reverse('show_followers', kwargs={'user_id':100000000000})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')

    

