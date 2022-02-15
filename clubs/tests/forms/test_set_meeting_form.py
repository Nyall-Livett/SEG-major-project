"""Unit tests of the Meeting form."""
from django.test import TestCase
from clubs.forms import MeetingForm
from clubs.models import Meeting, User, Book, Club

class MeetingFormTestCase(TestCase):
    """Unit tests of the set up meeting form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/default_club.json',

        ]


    def setUp(self):
        #self.url = reverse('set_meeting')
        self.default_user = User.objects.get(username='johndoe')
        #self.default_club = Club.objects.get(name='Oxford Book Club')
        #self.default_book = Book.objects.get(isbn= "0195153448")


        self.form_input = {
            #"date": "2022-02-27 11:00:00",
            "date": "2022-02-27 11:00:00",
            "URL": "www.aaa.com",
            "club":1,
            "notes": "This is a note.",
            "book":1,
            "members":[1]
        }


    # Test Form has the correct fields in the form
    def test_form_contains_required_fields(self):
        form = MeetingForm(self.form_input)
        self.assertIn('club', form.fields)
        #self.assertIn('members', form.fields)
        #self.assertIn('book', form.fields)

    # Test the form accepts valid input
    def test_form_accepts_valid_input(self):
        #print()
        form = MeetingForm(data=self.form_input)
        print(form.errors)
        self.assertTrue(form.is_valid())

    # Test the form rejects blank club
    def test_form_rejects_blank_name(self):
        self.form_input['club'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form rejects blank meeting notes
    def test_form_accepts_blank_notes(self):
        self.form_input['notes'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form error message for blank next_book
    def test_form_error_message_for_blank_book(self):
        self.form_input['book'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertEqual(form.errors["book"], ["This field is required."])

    # Test the form error message for blank club
    def test_form_error_message_for_blank_club(self):
        self.form_input['club'] = 0
        form = MeetingForm(data=self.form_input)
        self.assertEqual(form.errors["club"], ["Select a valid choice. That choice is not one of the available choices."])
