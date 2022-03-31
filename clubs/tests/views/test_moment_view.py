from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from clubs.enums import MomentType
from clubs.models import Moment, User, Club
from clubs.tests.helpers import LogInTester, isUrlLegit


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
        self.data = {'body': 'sdfsdfsdfs'}

    # def test_moment_created_correctly(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     num = Moment.objects.all().count()
    #     self.assertEqual(num,0)
    #     new_moment = Moment.objects.create(body = 'New moment', type = MomentType.CUSTOM, user = self.user) 
    #     new_moment.full_clean()
    #     new_moment.save()
    #     num_2 = Moment.objects.all().count()
    #     self.assertEqual(num_2,1)
    #     self.assertEqual(new_moment.type,MomentType.CUSTOM)
    #     self.assertEqual(new_moment.type, 0)
    #     saved_moment = Moment.objects.all()[0]
    #     self.assertEqual(saved_moment, new_moment)
    #     form_input = {
    #         'moment_body': 'This is a test moment'
    #     }
    #     response = self.client.post(self.url, form_input, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        
    # def test_new_moment_posted(self):
    #     form_input = {
    #         'moment_body': 'This is a test moment'
    #     }
    #     self.client.login(username=self.user.username, password="Password123")
    #     moment_count_before = Moment.objects.count()
    #     response = self.client.post(self.url, form_input, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
    #     moment_count_after = Moment.objects.count()
    #     self.assertEqual(moment_count_after, moment_count_before + 1)
    #     self.assertEqual(response.status_code, 200)


