from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Post
from clubs.tests.helpers import create_posts, reverse_with_next
from with_asserts.mixin import AssertHTMLMixin

class ShowUserTest(TestCase, AssertHTMLMixin):

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.target_user = User.objects.get(username='@janedoe')
        self.url = reverse('show_user', kwargs={'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.target_user.id}')

    def test_get_show_user_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "@janedoe")
        followable = response.context['followable']
        self.assertTrue(followable)
        follow_toggle_url = reverse('follow_toggle', kwargs={'user_id': self.target_user.id})
        query = f'.//form[@action="{follow_toggle_url}"]//button'
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertEquals(button.text, "Follow")
        self.user.toggle_follow(self.target_user)
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertEquals(button.text, "Unfollow")

    def test_get_show_user_with_own_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "@johndoe")
        followable = response.context['followable']
        self.assertFalse(followable)
        follow_toggle_url = reverse('follow_toggle', kwargs={'user_id': self.target_user.id})
        query = f'.//form[@action="{follow_toggle_url}"]//button'
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertIsNone(button)

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
