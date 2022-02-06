from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Book
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadBookTestCase(TestCase):

    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('upload_books')
        self.user = User.objects.get(username='johndoe')
        file = SimpleUploadedFile("file.txt", b'"0002005018";"Clara Callan";"Richard Bruce Wright";"2001";"HarperFlamingo Canada";"http://images.amazon.com/images/P/0002005018.01.THUMBZZZ.jpg";"http://images.amazon.com/images/P/0002005018.01.MZZZZZZZ.jpg";"http://images.amazon.com/images/P/0002005018.01.LZZZZZZZ.jpg"')
        self.input = {'file': file}

    def test_upload_books_url(self):
        self.assertEqual(self.url,'/upload_books/')
    # 
    # def test_valid_file(self):
    #     self.client.login(username=self.user, password='Password123')
    #     book_count_before = Book.objects.count()
    #     response = self.client.post(self.url, self.input, follow=True)
    #     book_count_after = Book.objects.count()
    #     self.assertEqual(book_count_before, book_count_after-1)
