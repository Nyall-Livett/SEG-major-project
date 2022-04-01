from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Book
from clubs.tests.helpers import LogInTester, reverse_with_next

class CreateBookTestCase(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.url = reverse('book')
        self.default_user = User.objects.get(username='johndoe')
        self.form_input = {
            'isbn': '0195153448',
            'name': 'Classical Mythology',
            'description': 'Book about Mythology',
            'author': 'Mark P. O. Morford',
            'publication_year': '2002',
            'publisher': 'Oxford University Press',
            'image_url_s':'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg',
            'image_url_m':'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg',
            'image_url_l':'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg',
        }

    def test_log_in_url(self):
        self.assertEqual(self.url,'/book/')

    def test_redirect_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_new_book_successful(self):
        self.client.login(username=self.default_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        count_before = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        count_after = Book.objects.count()
        self.assertEqual(count_before, count_after-1)
