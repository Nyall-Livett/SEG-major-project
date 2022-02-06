from django.test import TestCase
from clubs.models import User, Book
from clubs.forms import UploadBooksForm
from django.core.files.uploadedfile import SimpleUploadedFile


class UploadBooksFormTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        file = SimpleUploadedFile("file.txt", b'filecontentstring')
        self.input = {'file': file}

    def test_upload_books_form_has_necessary_fields(self):
        form = UploadBooksForm()
        self.assertIn('file', form.fields)

    # def test_valid_upload_books_form(self):
    #     form = UploadBooksForm(data=self.input)
    #     self.assertTrue(form.is_valid())

    def test_file_must_not_be_blank(self):
        self.input['file'] = ""
        form = UploadBooksForm(data=self.input)
        self.assertFalse(form.is_valid())
