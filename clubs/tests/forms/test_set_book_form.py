from django import forms
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import BookForm, BookReviewForm, MeetingForm
from clubs.models import Book, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class SetBookTestCase(TestCase ,LogInTester):
    """Unit tests of the set up meeting form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',

        ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.book = Book.objects.get(isbn= "0195153448")
        self.url = reverse('book')
        self.form_input = {
            'isbn': '0195153431',
            'name': 'Holographic universe',
            'description': 'This book is about vision...',
            'author': 'janedoe',
            'publication_year': '2002',
            'publisher': 'London Publisher',
            'image_url_s': 'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg',
            'image_url_m': 'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg',
            'image_url_l': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg',
            'category': 'Humor',
            'grouped_category': 'Humor',
        }
       
    def test_set_book_uses_correct_template(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'set_book.html')

    
    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_set_book_redirects_when_user_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_set_book_has_required_fields(self):
        form = BookForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('isbn', form.fields)
        self.assertIn('author', form.fields)
        self.assertIn('publisher', form.fields)
        self.assertIn('publication_year', form.fields)
        self.assertIn('image_url_s', form.fields)
        self.assertIn('image_url_m', form.fields)

    def test_valid_set_book_form(self):
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_isbn_must_not_be_blank(self):
        self.form_input['isbn'] = ''
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_must_not_be_blank(self):
        self.form_input['name'] = ''
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_author_must_not_be_blank(self):
        self.form_input['author'] = ''
        form = BookForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_book_description_can_be_blank(self):
        self.form_input['description'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_publication_year_can_be_blank(self):
        self.form_input['publication_year'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_publisher_can_be_blank(self):
        self.form_input['publisher'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_image_url_s_can_be_blank(self):
        self.form_input['image_url_s'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_image_url_m_can_be_blank(self):
        self.form_input['image_url_m'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_image_url_l_can_be_blank(self):
        self.form_input['image_url_l'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_category_can_be_blank(self):
        self.form_input['category'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_grouped_category_can_be_blank(self):
        self.form_input['grouped_category'] = ''
        form = BookForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_must_save_correctly(self):
        form = BookForm(data=self.form_input)
        before_count = Book.objects.count()
        form.save()
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count+1)
        book = Book.objects.get(isbn='0195153431')
        self.assertEqual(book.name, 'Holographic universe')
        self.assertEqual(book.description, 'This book is about vision...')
        self.assertEqual(book.author, 'janedoe')
        self.assertEqual(book.publication_year, '2002')
        self.assertEqual(book.publisher, 'London Publisher')
        self.assertEqual(book.image_url_s, 'http://images.amazon.com/images/P/0195153448.01.THUMBZZZ.jpg')
        self.assertEqual(book.image_url_m, 'http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg')
        self.assertEqual(book.image_url_l, 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg')
       
      

