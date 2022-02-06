"""Unit tests for the Book model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Book, User

class BookModelTestCase(TestCase):
    """Unit tests for the Book model."""

    fixtures = [
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/other_books.json'
    ]

    def setUp(self):
        self.book = Book.objects.get(isbn="0195153448")

    def test_valid_book(self):
        self._assert_book_is_valid()

    def test_isbn_cannot_be_blank(self):
        self.book.isbn = ''
        self._assert_book_is_invalid()

    def test_isbn_can_be_13_characters_long(self):
        self.book.isbn = 'x' * 13
        self._assert_book_is_valid()

    def test_isbn_cannot_be_over_13_characters_long(self):
        self.book.isbn = 'x' * 14
        self._assert_book_is_invalid()

    def test_isbn_must_be_unique(self):
        other_book = Book.objects.get(isbn="0002005018")
        self.book.isbn = other_book.isbn
        self._assert_book_is_invalid()

    def test_name_can_be_64_characters_long(self):
        self.book.name = 'x' * 64
        self._assert_book_is_valid()

    def test_name_cannot_be_over_644_characters_long(self):
        self.book.name = 'x' * 65
        self._assert_book_is_invalid()

    def test_name_cannot_be_blank(self):
        self.book.name = ''
        self._assert_book_is_invalid()

    def test_author_can_be_64_characters_long(self):
        self.book.author = 'x' * 64
        self._assert_book_is_valid()

    def test_author_cannot_be_over_64_characters_long(self):
        self.book.author = 'x' * 65
        self._assert_book_is_invalid()

    def test_author_cannot_be_blank(self):
        self.book.author = ''
        self._assert_book_is_invalid()

    def test_description_can_be_2048_characters_long(self):
        self.book.description = 'x' * 2048
        self._assert_book_is_valid()

    def test_name_cannot_be_over_2049_characters_long(self):
        self.book.description = 'x' * 2049
        self._assert_book_is_invalid()

    def test_publication_year_can_be_4_characters_long(self):
        self.book.publication_year = 'x' * 4
        self._assert_book_is_valid()

    def test_publication_year_cannot_be_over_4_characters_long(self):
        self.book.publication_year = 'x' * 5
        self._assert_book_is_invalid()

    def test_publisher_can_be_64_characters_long(self):
        self.book.publisher = 'x' * 64
        self._assert_book_is_valid()

    def test_publisher_cannot_be_over_64_characters_long(self):
        self.book.publisher = 'x' * 65
        self._assert_book_is_invalid()

    def test_image_url_s_field_must_be_url(self):
        self.book.image_url_s = 1234
        self._assert_book_is_invalid()

    def test_image_url_s_can_be_200_characters_long(self):
        self.book.image_url_s = "https://www.example.com/" + 'x' * 176
        self._assert_book_is_valid()

    def test_image_url_s_cannot_be_over_200_characters_long(self):
        self.book.image_url_s = 'x' * 201
        self._assert_book_is_invalid()

    def test_image_url_m_field_must_be_url(self):
        self.book.image_url_m = 1234
        self._assert_book_is_invalid()

    def test_image_url_m_can_be_200_characters_long(self):
        self.book.image_url_m =  "https://www.example.com/" + 'x' * 176
        self._assert_book_is_valid()

    def test_image_url_m_cannot_be_over_200_characters_long(self):
        self.book.image_url_m = 'x' * 201
        self._assert_book_is_invalid()

    def test_image_url_l_field_must_be_url(self):
        self.book.image_url_l = 1234
        self._assert_book_is_invalid()

    def test_image_url_l_can_be_200_characters_long(self):
        self.book.image_url_l = "https://www.example.com/" + 'x' * 176
        self._assert_book_is_valid()

    def test_image_url_l_cannot_be_over_200_characters_long(self):
        self.book.image_url_l = 'x' * 201
        self._assert_book_is_invalid()

    def _assert_book_is_valid(self):
        try:
            self.book.full_clean()
        except (ValidationError):
            self.fail('Test book should be valid')

    def _assert_book_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.book.full_clean()
