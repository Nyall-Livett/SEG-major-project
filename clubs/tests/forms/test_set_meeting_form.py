"""Unit tests of the Meeting form."""
from django.test import TestCase
from clubs.forms import MeetingForm
from clubs.models import Meeting

class MeetingFormTestCase(TestCase):
    """Unit tests of the set up meeting form."""


    def setUp(self):
        self.form_input = {
            'date': '2022-01-27 11:00:00',
            'club': 'Book First',
            'URL': 'https://www.meetingbest.com/',
            'member_selected': 'Tom',
            'meeting_notes': 'The first meeting begins',
            'next_book': 'War and Peace'
        }

    # Test Form has the correct fields in the form
    def test_form_contains_required_fields(self):
        form = MeetingForm(self.form_input)
        self.assertIn('club', form.fields)
        self.assertIn('URL', form.fields)
        self.assertIn('member_selected', form.fields)
        self.assertIn('meeting_notes', form.fields)
        self.assertIn('next_book', form.fields)

    # Test the form accepts valid input
    def test_form_accepts_valid_input(self):
        form = MeetingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form rejects blank club
    def test_form_rejects_blank_name(self):
        self.form_input['club'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form rejects blank meeting notes
    def test_form_rejects_blank_notes(self):
        self.form_input['meeting_notes'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form error message for blank next_book
    def test_form_error_message_for_blank_book(self):
        self.form_input['next_book'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertEqual(form.errors["next_book"], ["This field is required."])

    # Test the form error message for blank club
    def test_form_error_message_for_blank_club(self):
        self.form_input['club'] = ''
        form = MeetingForm(data=self.form_input)
        self.assertEqual(form.errors["club"], ["This field is required."])