from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Post, User, Club

class PostTest(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.post = Post(
            author=self.user,
            club=self.club,
            title = "title",
            body="The quick brown fox jumps over the lazy dog."
        )

    def test_valid_message(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")

    def test_author_must_not_be_blank(self):
        self.post.author = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_club_must_not_be_blank(self):
        self.post.club = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_title_must_not_be_blank(self):
        self.post.title = ''
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_title_must_not_be_overlong(self):
        self.post.title = 'x' * 65
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_body_must_not_be_blank(self):
        self.post.body = ''
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_body_must_not_be_overlong(self):
        self.post.body = 'x' * 301
        with self.assertRaises(ValidationError):
            self.post.full_clean()
