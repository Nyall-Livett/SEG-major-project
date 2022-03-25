from django.test import TestCase
from django.urls import reverse
from clubs.tests.helpers import LogInTester
from clubs.models import User, Club, Meeting, Book
from ...helpers import *

class NBasedRecommendationsViewTestCase(TestCase,LogInTester):
    """Test of Neighbourhood-based recommendations view"""

    fixtures = ['clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/default_club.json',
        'clubs/tests/fixtures/other_meetings.json',
        'clubs/tests/fixtures/default_book.json',
        'clubs/tests/fixtures/other_books.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/recommendations_books'
        ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.other_user = User.objects.get(username='janedoe')
        self.club = Club.objects.get(name = "Oxford Book Club")
        self.meeting = Meeting.objects.get(pk=2)
        self.book = Book.objects.get(isbn = "0195153448")
        self.book_read = Book.objects.get(isbn = "0002005018")
        self.dashboard_url = reverse('dashboard')
        self.book_review_url = reverse('book_review')
        self.sign_up_url = reverse('sign_up')
        self.delete_account_url = reverse('delete_account',kwargs={'user_id': self.other_user.id})
        self.start_meeting_url = reverse('start_meeting', kwargs={'pk': self.meeting.pk})
        # self.profile_url = reverse('profile')

    def test_urls(self):
        self.assertEqual(self.dashboard_url,f'/dashboard/')
        self.assertEqual(self.sign_up_url,f'/sign_up/')
        self.assertEqual(self.book_review_url,f'/book_review')
        # self.assertEqual(self.profile_url,f'/profile/')
        self.assertEqual(self.delete_account_url,f'/delete_account/{self.other_user.id}')
        self.assertEqual(self.start_meeting_url,f'/start_meeting/{self.meeting.pk}/')

    def test_drop_specfic_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_count_before = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_after = get_ratings_count(self.user.id)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    def test_generate_ratings(self):
        book_1 = Book.objects.get(pk=3)
        book_2 = Book.objects.get(pk=4)
        self.client.login(username='johndoe', password='Password123')
        rating_count_before = get_ratings_count(self.user.id)
        self.assertTrue(self._is_logged_in())
        generate_ratings(self.book,self.user.id,'like')
        generate_ratings(book_1,self.user.id,'dislike')
        generate_ratings(book_2,self.user.id,'neutral')
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after-3)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)


    def test_generate_favourite_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        rating_count_before = get_ratings_count(self.user.id)
        self.assertTrue(self._is_logged_in())
        generate_favourite_ratings(self.book,self.user.id)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after-1)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    def test_generate_duplicated_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_at_first = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_before = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)
        amount = rating_count_after - rating_at_first
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_at_first,rating_after_drop)

    def test_access_dashboard_with_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_at_first = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.dashboard_url)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)
        amount = rating_count_after - rating_at_first
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_at_first,rating_after_drop)

    def test_access_dashboard_without_books(self):
        Book.objects.all().delete()
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.dashboard_url)
        recommendations = response.context['recommendations']
        self.assertIsNone(recommendations)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)

    def test_access_dashboard_without_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        delete_ratings(self.user.id)
        self.assertFalse(contain_ratings(self.user.id))
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.dashboard_url)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after-1)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    def test_access_start_meeting_with_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_at_first = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.start_meeting_url)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)
        amount = rating_count_after - rating_at_first
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_at_first,rating_after_drop)

    def test_access_start_meeting_without_books(self):
        Book.objects.all().delete()
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.start_meeting_url)
        recommendations = response.context['recommendations']
        self.assertIsNone(recommendations)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)

    def test_access_start_meeting_without_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        delete_ratings(self.user.id)
        self.assertFalse(contain_ratings(self.user.id))
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.get(self.start_meeting_url)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after-1)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    def test_add_book_read_will_generate_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        form_input = {'book': self.book_read.id,'rating': 'neutral'}
        rating_at_first = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.post(self.book_review_url, form_input, follow=True)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after-1)
        amount = rating_count_after - rating_at_first
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_at_first,rating_after_drop)

    def test_add_book_read_will_not_generate_duplicated_ratings(self):
        self.client.login(username='johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        form_input = {'book': self.book_read.id,'rating': 'neutral'}
        rating_at_first = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'like')
        generate_ratings(self.book_read,self.user.id,'neutral')
        rating_count_before = get_ratings_count(self.user.id)
        response = self.client.post(self.book_review_url, form_input, follow=True)
        rating_count_after = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_count_after)
        amount = rating_count_after - rating_at_first
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_at_first,rating_after_drop)

    def test_delete_accounts_will_delete_ratings(self):
        self.client.login(username=self.other_user, password='Password123')
        self.assertTrue(self._is_logged_in())
        generate_ratings(self.book,self.other_user.id,'like')
        self.assertTrue(contain_ratings(self.other_user.id))
        response = self.client.post(self.delete_account_url, follow=True)
        rating_count_after = get_ratings_count(self.other_user.id)
        self.assertEqual(0,rating_count_after)

    def test_dashboard_show_recommendations(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_count_before = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'neutral')
        response = self.client.get(self.dashboard_url)
        book_1 = Book.objects.get(pk=3)
        book_2 = Book.objects.get(pk=4)
        book_3 = Book.objects.get(pk=5)
        book_4 = Book.objects.get(pk=6)
        book_5 = Book.objects.get(pk=7)
        self.assertContains(response, f'{book_1.name}')
        self.assertContains(response, f'{book_2.name}')
        self.assertContains(response, f'{book_3.name}')
        self.assertContains(response, f'{book_4.name}')
        self.assertContains(response, f'{book_5.name}')
        rating_count_after = get_ratings_count(self.user.id)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    def test_start_meeting_show_recommendations(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        rating_count_before = get_ratings_count(self.user.id)
        generate_ratings(self.book,self.user.id,'neutral')
        response = self.client.get(self.start_meeting_url)
        book_1 = Book.objects.get(pk=3)
        book_2 = Book.objects.get(pk=4)
        book_3 = Book.objects.get(pk=5)
        book_4 = Book.objects.get(pk=6)
        book_5 = Book.objects.get(pk=7)
        self.assertContains(response, f'{book_1.name}')
        self.assertContains(response, f'{book_2.name}')
        self.assertContains(response, f'{book_3.name}')
        self.assertContains(response, f'{book_4.name}')
        self.assertContains(response, f'{book_5.name}')
        rating_count_after = get_ratings_count(self.user.id)
        amount = rating_count_after - rating_count_before
        drop_specific_amount_ratings(amount)
        rating_after_drop = get_ratings_count(self.user.id)
        self.assertEqual(rating_count_before,rating_after_drop)

    # def test_sign_up_will_generate_ratings(self):
    #     # self.client.login(username='johndoe', password='Password123')
    #     # self.assertTrue(self._is_logged_in())
    #     self.assertFalse(contain_ratings(self.user.id))
    #     form_input = {
    #         'first_name': 'Jane',
    #         'last_name': 'Doe',
    #         'username': 'janedoe',
    #         'email': 'janedoe@example.org',
    #         'bio': 'My bio',
    #         'new_password': 'Password123',
    #         'password_confirmation': 'Password123'
    #     }
    #     rating_count_before = get_ratings_count(self.user.id)
    #     response = self.client.post(self.sign_up_url,form_input, follow=False)
    #     rating_count_after = get_ratings_count(self.user.id)
    #     self.assertEqual(rating_count_before,rating_count_after-1)
    #     delete_ratings(self.user.id)
    #     rating_after_delete = get_ratings_count(self.user.id)
    #     self.assertEqual(0,rating_after_delete)

    # def test_update_favourite_book_will_generate_ratings(self):
    #     self.client.login(username='johndoe', password='Password123')
    #     self.assertTrue(self._is_logged_in())
    #     generate_ratings(self.book,self.user.id,'like')
    #     form_input = {
    #         'first_name': 'John2',
    #         'last_name': 'Doe2',
    #         'username': 'johndoe2',
    #         'email': 'johndoe2@example.org',
    #         'bio': 'New bio',
    #         'favourite_book':self.book_read.id
    #     }
    #     rating_count_before = get_ratings_count(self.user.id)
    #     self.client.post(self.profile_url,form_input, follow=True)
    #     rating_count_after = get_ratings_count(self.user.id)
    #     self.assertEqual(rating_count_before,rating_count_after-1)
    #     delete_ratings(self.user.id)
    #     rating_after_delete = get_ratings_count(self.user.id)
    #     self.assertEqual(0,rating_after_delete)
