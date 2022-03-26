from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Book
from clubs.tests.helpers import reverse_with_next

class ShowBookTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.book = Book.objects.get(isbn="0195153448")
        self.url = reverse('show_book', kwargs={'book_id': self.book.id})


    def test_show_book_url(self):
        self.assertEqual(self.url,f'/book/{self.book.id}')

    def test_get_show_book_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_book.html')
        self.assertContains(response, "0195153448")
        self.assertContains(response, "Classical Mythology")
        self.assertContains(response, "Mark P. O. Morford")
        self.assertContains(response, "Oxford University Press")


    def test_get_show_book_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_book', kwargs={'book_id': self.book.id+99999})
        response = self.client.get(url, follow=True)
        response_url = reverse('book_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'book_list.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
