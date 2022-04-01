from django.test import TestCase
from django.urls import reverse
from clubs.enums import MomentType
from clubs.models import Moment, User, Club
from clubs.tests.helpers import LogInTester


class MomentTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_users.json'
        ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.club = Club.objects.get(pk=1)
        self.book = Club.objects.get(pk=1)
        self.url = reverse('create_moment')

    def test_moment_created_correctly(self):
        self.client.login(username=self.user.username, password='Password123')
        num = Moment.objects.all().count()
        self.assertEqual(num, 0)
        response = self.client.post(self.url, {'moment_body': '"This is a moment"'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        new_moment = Moment.objects.first()
        num_2 = Moment.objects.all().count()
        self.assertEqual(num_2,1)
        self.assertEqual(new_moment.type,MomentType.CUSTOM)
        self.assertEqual(new_moment.type, 0)
        saved_moment = Moment.objects.all()[0]
        self.assertEqual(saved_moment, new_moment)
