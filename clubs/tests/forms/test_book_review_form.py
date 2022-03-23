from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import BookReviewForm
from clubs.models import Book, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class BookReviewTest(TestCase,  LogInTester):

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/default_book.json',
                ]

    def setUp(self):
        self.url = reverse('book_review')
        self.user = User.objects.get(username='johndoe')
        self.book = Book.objects.get(isbn= "0195153448")
        self.input = {'book': self.book, 'rating': 'like'}

    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_change_theme_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'book_review.html')

    def test_book_review_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_book_review_has_required_fields(self):
        form = BookReviewForm()
        self.assertIn('book', form.fields)
        self.assertIn('rating', form.fields)

    def test_valid_review_form(self):
        form = BookReviewForm(data=self.input)
        self.assertTrue(form.is_valid())

    def test_book_must_not_be_blank(self):
        self.input['book'] = ''
        form = BookReviewForm(data=self.input)
        self.assertFalse(form.is_valid())

    def test_rating_must_not_be_blank(self):
        self.input['rating'] = ''
        form = BookReviewForm(data=self.input)
        self.assertFalse(form.is_valid())

    def test_rating_must_be_like_dislike_neutral(self):
        self.input['rating'] = 'like'
        form = BookReviewForm(data=self.input)
        self.assertTrue(form.is_valid())
        self.input['rating'] = 'dislike'
        form = BookReviewForm(data=self.input)
        self.assertTrue(form.is_valid())
        self.input['rating'] = 'neutral'
        form = BookReviewForm(data=self.input)
        self.assertTrue(form.is_valid())
        self.input['rating'] = 'good'
        form = BookReviewForm(data=self.input)
        self.assertFalse(form.is_valid())

