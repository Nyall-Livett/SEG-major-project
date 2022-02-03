from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.forms import PostForm
from clubs.models import User, Club, Post
from clubs.tests.helpers import create_posts, reverse_with_next

class ClubForumViewTestCase(TestCase):
    """Tests of the club forum view."""

    fixtures = ['clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.url = reverse('club_forum', kwargs = {'club_id' : self.club.id})

    def test_club_forum_url(self):
        self.assertEqual(self.url,f'/forum/{self.club.id}')

    def test_get_club_forum(self):
        self.client.login(username=self.user.username, password='Password123')
        self.club.add_or_remove_member(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_get_club_forum_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_club_forum_when_is_not_a_memer(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_forum_contains_posts_by_club_members(self):
        self.client.login(username=self.user.username, password='Password123')
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.club.add_or_remove_member(self.user)
        self.club.add_or_remove_member(jane)
        self.club.add_or_remove_member(petra)
        create_posts(self.user, self.club, 100, 103)
        create_posts(jane, self.club, 200, 203)
        create_posts(petra, self.club, 300, 303)
        create_posts(peter, self.club, 400, 403)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertContains(response, f'Post__title{count}')
            self.assertContains(response, f'Post__body{count}')
        for count in range(200, 203):
            self.assertContains(response, f'Post__title{count}')
            self.assertContains(response, f'Post__body{count}')
        for count in range(300, 303):
            self.assertContains(response, f'Post__title{count}')
            self.assertContains(response, f'Post__body{count}')
        for count in range(400, 403):
            self.assertNotContains(response, f'Post__title{count}')
            self.assertNotContains(response, f'Post__body{count}')
        self.assertFalse(response.context['is_paginated'])

    def test_club_forum_with_pagination(self):
        self.client.login(username=self.user.username, password='Password123')
        jane = User.objects.get(username='janedoe')
        self.club.add_or_remove_member(self.user)
        self.club.add_or_remove_member(jane)
        create_posts(self.user,self.club, 100, 100+settings.POSTS_PER_PAGE+2)
        create_posts(jane, self.club, 100, 100+settings.POSTS_PER_PAGE+2)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_one_url = self.url + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_two_url = self.url + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_three_url = self.url + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(len(response.context['posts']), 4)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())
