"""Unit tests of the Club form form."""
from django.test import TestCase
from clubs.forms import ClubForm
from clubs.models import Club

class ClubFormTestCase(TestCase):
    """Unit tests of the create club form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.form_input = {
            'name': 'London Book Club',
            'description': 'Book club based in London',
            'theme': 'Horror',
            'maximum_members': 3
        }

    # Test Form has the correct fields in the form
    def test_form_contains_required_fields(self):
        form = ClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)

    # Test the form accepts valid input
    def test_form_accepts_valid_input(self):
        form = ClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Test the form rejects blank name
    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form rejects blank description
    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Test the form error message for duplicate name
    def test_form_error_message_for_duplicate_name(self):
        self.form_input['name'] = 'Oxford Book Club'
        form = ClubForm(data=self.form_input)
        self.assertEqual(form.errors["name"], ["Club with this Name already exists."])

    # Test the form error message for blank name
    def test_form_error_message_for_blank_name(self):
        self.form_input['name'] = ''
        form = ClubForm(data=self.form_input)
        self.assertEqual(form.errors["name"], ["This field is required."])

    # Test the form error message for blank name
    def test_form_error_message_for_blank_description(self):
        self.form_input['description'] = ''
        form = ClubForm(data=self.form_input)
        self.assertEqual(form.errors["description"], ["This field is required."])
