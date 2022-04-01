from django import forms
from django.test import TestCase
from django.urls import reverse
from clubs.forms import  MeetingForm
from clubs.models import Book, User, Club
from clubs.tests.helpers import LogInTester, reverse_with_next

class MeetingFormTestCase(TestCase ,LogInTester):
    """Unit tests of the set up meeting form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',

        ]


    def setUp(self):
        self.default_user = User.objects.get(username='johndoe')
        self.default_club = Club.objects.get(name='Oxford Book Club')
        self.default_book = Book.objects.get(isbn= "0195153448")
        self.url = reverse('set_meeting' , kwargs={'club_id': self.default_club.id})


        self.form_input = {
            #"date": "2022-02-27 11:00:00",
            "start": "2022-02-27 11:00:00",
            "finish": "2022-02-27 12:00:00",
            "location": "Online",
            "URL": "www.aaa.com",
            "club":1,
            "notes": "This is a note.",
            "book":1,
            "next_book":1,
            "chosen_member":1
        }


    def test_get_access_for_unauthenticated(self):
        self.assertFalse(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)


    # Test Form has the correct fields in the form
    def test_form_contains_required_fields(self):
        form = MeetingForm()
        self.assertIn('start', form.fields)
        self.assertIn('finish', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('notes', form.fields)
        self.assertIn('book', form.fields)
        notes_widget = form.fields['notes'].widget
        self.assertTrue(isinstance(notes_widget, forms.Textarea))

    # Test the form accepts valid input
    def test_form_accepts_valid_input(self):
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form rejects blank club
    def test_form_rejects_blank_club(self):
        self.form_input['club'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form accepts blank meeting notes
    def test_form_accepts_blank_notes(self):
        self.form_input['notes'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form accepts blank meeting location
    def test_location_can_not_be_blank(self):
        self.form_input['location'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form accepts blank meeting URL
    def test_form_accepts_blank_URL(self):
        self.form_input['URL'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form accepts blank meeting book
    def test_form_accepts_blank_book(self):
        self.form_input['book'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form accepts blank meeting next_book
    def test_form_accepts_blank_next_book(self):
        self.form_input['next_book'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form accepts blank book
    def test_form_accepts_blank_book(self):
        self.form_input['book'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
