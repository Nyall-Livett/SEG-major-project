from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import LogInTester

class PendingRequest(TestCase, LogInTester):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe')
        self.club = Club.objects.get(name='Oxford Book Club')
        self.applicant = User.objects.get(username = 'janedoe')
        self.url = reverse('pending_requests', kwargs={'club_id': self.club.id})

    def test_correct_template_used(self):
        self.client.login(username=self.user, password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pending_requests.html')

    def test_club_applicants_increases_when_applying(self):
        self.client.login(username=self.applicant, password='Password123')
        before_count = self.club.applicants.all().count()
        Club.applicant_manager(self.club, self.applicant)
        after_count = self.club.applicants.all().count()
        self.assertEqual(before_count+1, after_count)

    def test_accept_club_applicant(self):
        self.client.login(username=self.user, password='Password123')
        self.client.login(username=self.applicant, password='Password123')
        applicants_before = self.club.applicants.all().count()
        Club.applicant_manager(self.club, self.applicant)
        applicants_after = self.club.applicants.all().count()
        self.assertEqual(applicants_before+1, applicants_after)
        members_before = self.club.members.all().count()
        self.club.acceptmembership(self.applicant)
        applicants_after_acceptance = self.club.applicants.all().count()
        members_after = self.club.members.all().count()
        self.assertEqual(applicants_after_acceptance, applicants_after-1)
        self.assertEqual(members_before+1, members_after)
        joined = self.applicant in self.club.members.all()
        self.assertTrue(joined)
        is_member = self.club.is_member(self.applicant)
        self.assertTrue(is_member)

    def test_reject_membership(self):
        self.client.login(username=self.user, password='Password123')
        self.client.login(username=self.applicant, password='Password123')
        applicants_before = self.club.applicants.all().count()
        Club.applicant_manager(self.club, self.applicant)
        applicants_after = self.club.applicants.all().count()
        self.assertEqual(applicants_before+1, applicants_after)
        members_before = self.club.members.all().count()
        self.club.rejectmembership(self.applicant)
        applicants_after_rejection = self.club.applicants.all().count()
        members_after = self.club.members.all().count()
        self.assertEqual(applicants_after_rejection, applicants_after-1)
        members_after = self.club.members.all().count()
        self.assertEqual(members_before, members_after)
        joined = self.applicant in self.club.members.all()
        self.assertFalse(joined)
        is_member = self.club.is_member(self.applicant)
        self.assertFalse(is_member)

    
    