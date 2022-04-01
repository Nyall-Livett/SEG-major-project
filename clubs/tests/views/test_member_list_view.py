from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User
from clubs.tests.helpers import LogInTester

class MemberListTest(TestCase, LogInTester):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_club.json',
                'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.url = reverse('member_list' , kwargs={'club_id': self.club.id})

    def test_member_list_url(self):
        self.assertEqual(self.url,f'/member_list/{self.club.id}')

    def test_correct_template_used(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'member_list.html')

    