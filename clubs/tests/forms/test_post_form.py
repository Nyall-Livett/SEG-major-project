from django.test import TestCase
from clubs.models import User, Club
from clubs.forms import PostForm

class PostFormTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.input = {'title': 'x'*64, 'body': 'x'*300 }

    def test_post_form_has_necessary_fields(self):
        form = PostForm()
        self.assertIn('title', form.fields)
        self.assertIn('body', form.fields)

    def test_valid_post_form(self):
        form = PostForm(data=self.input)
        self.assertTrue(form.is_valid())

    def test_title_must_not_be_blank(self):
        self.input['title'] = ''
        form = PostForm(data=self.input)
        self.assertFalse(form.is_valid())

    def test_title_must_not_be_longer_than_64_characters(self):
        self.input['title'] = 'x' * 65
        form = PostForm(data=self.input)
        self.assertFalse(form.is_valid())

    def test_body_must_not_be_blank(self):
        self.input['body'] = ''
        form = PostForm(data=self.input)
        self.assertFalse(form.is_valid())

    def test_body_must_not_be_longer_than_300_characters(self):
        self.input['title'] = 'x' * 301
        form = PostForm(data=self.input)
        self.assertFalse(form.is_valid())
