from clubs.models import Moment
from clubs.enums import MomentType

class CreateMoment:

    def notify(self, type, user, kwargs):
        notifier = self._get_notifier(type)
        self.user = user
        notifier(user, **kwargs)

    def _get_notifier(self, type):

        if type == MomentType.BECAME_FRIENDS:
            return self._became_friends

        elif type == MomentType.CLUB_CREATED:
            return self._create_club

        elif type == MomentType.BOOK_RECOMMENDATION:
            return self._book_recommendation

        elif type == MomentType.READING_NEW_BOOK:
            return self._reading_new_book


    def _became_friends(self, user, **kwargs):
        other_user = kwargs['other_user']
        body = "{other_user} started following you.".format(other_user=other_user.username)
        Moment.objects.create(
            type=MomentType.BECAME_FRIENDS,
            body = body,
            user = self.user,
            associated_user = other_user.id
        )

    def _create_club(self, user, **kwargs):
        club = kwargs['club']
        body = "{user} created {club}.".format(user=self.user.username, club=club.name)
        Moment.objects.create(
            type=MomentType.CLUB_CREATED,
            body = body,
            user = self.user,
            associated_club = club.id
        )

    def _book_recommendation(self, user, **kwargs):
        book = kwargs['book']
        description = "{user} has recommended {book}.".format(user=self.user, book=book.name)
        Moment.objects.create(
            type=MomentType.BOOK_RECOMMENDATION,
            body = body,
            user = self.user
        )

    def _reading_new_book(self, user, **kwargs):
        club = kwargs['club']
        book = kwargs['book']
        description = "{user} started reading {book} in the {club}.".format(user=self.user, book=book.name, club=club.name)
        Moment.objects.create(
            type=MomentType.READING_NEW_BOOK,
            body = body,
            user = self.user
        )
