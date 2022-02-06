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

    def test_book_list_url(self):
        self.assertEqual(self.url,'/books/')

    def test_get_book_list(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_books(settings.BOOKS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertEqual(len(response.context['books']), settings.BOOKS_PER_PAGE)
        self.assertFalse(response.context['is_paginated'])
        for book_id in range(settings.BOOKS_PER_PAGE-1):
            self.assertContains(response, f'isbn{book_id}')
            self.assertContains(response, f'name{book_id}')
            self.assertContains(response, f'author{book_id}')
            self.assertContains(response, f'http://images.com/image/s/{book_id}.jpg')

    def test_get_book_list_with_pagination(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_books(settings.BOOKS_PER_PAGE*2+3-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertEqual(len(response.context['books']), settings.BOOKS_PER_PAGE)
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_one_url = reverse('book_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertEqual(len(response.context['books']), settings.BOOKS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_two_url = reverse('book_list') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertEqual(len(response.context['books']), settings.BOOKS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_three_url = reverse('book_list') + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_list.html')
        self.assertEqual(len(response.context['books']), 3)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())


    def test_get_book_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_books(self, book_count=10):
        for book_id in range(book_count):
            Book.objects.create(
                isbn = f'isbn{book_id}',
                name = f'name{book_id}',
                author = f'author{book_id}',
                publication_year = f'pub year{book_id}',
                publisher = f'pub{book_id}',
                image_url_s = f'http://images.com/image/s/{book_id}.jpg',
                image_url_m = f'http://images.com/image/m/{book_id}.jpg',
                image_url_l = f'http://images.com/image/l/{book_id}.jpg',
            )
