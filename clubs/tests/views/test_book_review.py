from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Book
from clubs.tests.helpers import reverse_with_next

class BookListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_book.json',
                ]

    def setUp(self):
        self.url = reverse('book_list')
        self.user = User.objects.get(username='johndoe')
        self.book = Book.objects.get(isbn= "0195153448")

    def test_book_review_renders_correct_template(self):
        pass