"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = 'x' * 30
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = 'x' * 31
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_may_contain_non_alphanumericals(self):
        self.user.username = '@john!doe'
        self._assert_user_is_valid()

    def test_username_may_contain_numbers(self):
        self.user.username = 'j0hndoe2'
        self._assert_user_is_valid()


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        second_user = User.objects.get(username='janedoe')
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_520_characters(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_520_characters(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()


    """ Tests for following/unfollowing User """

    def test_adding_follower_increases_the_number_of_followers(self):
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.user.add_follower(jane)
        self.assertEqual(self.user.followers_count(), 1)
        self.user.add_follower(petra)
        self.assertEqual(self.user.followers_count(), 2)
        self.user.add_follower(peter)
        self.assertEqual(self.user.followers_count(), 3)

    def test_following_users_increases_the_number_of_followees(self):
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.user.follow(jane)
        self.assertEqual(self.user.followees_count(), 1)
        self.user.follow(petra)
        self.assertEqual(self.user.followees_count(), 2)
        self.user.follow(peter)
        self.assertEqual(self.user.followees_count(), 3)

    def test_unfollowing_users_decreases_the_number_of_followees(self):
        jane = User.objects.get(username='janedoe')
        petra = User.objects.get(username='petrapickles')
        peter = User.objects.get(username='peterpickles')
        self.user.follow(jane)
        self.user.follow(petra)
        self.user.follow(peter)
        self.assertEqual(self.user.followees_count(), 3)
        self.user.unfollow(jane)
        self.assertEqual(self.user.followees_count(), 2)
        self.user.unfollow(petra)
        self.assertEqual(self.user.followees_count(), 1)
        self.user.unfollow(peter)
        self.assertEqual(self.user.followees_count(), 0)

    def test_toggle_follow_users(self):
        jane = User.objects.get(username='janedoe')
        self.user.toggle_follow(jane)
        self.assertTrue(self.user.is_following(jane))
        self.user.toggle_follow(jane)
        self.assertFalse(self.user.is_following(jane))

