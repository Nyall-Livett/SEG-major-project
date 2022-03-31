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

        elif type == MomentType.BOOK_RATING:
            return self._book_rating


    def _became_friends(self, user, **kwargs):
        other_user = kwargs['other_user']
        if kwargs['body']:
            body = kwargs['body']
        else:
            body = "{other_user} started following you.".format(other_user=other_user.username)
        Moment.objects.create(
            type=MomentType.BECAME_FRIENDS,
            body = body,
            user = self.user,
            associated_user = other_user
        )

    def _create_club(self, user, **kwargs):
        club = kwargs['club']
        body = "{user} created {club}.".format(user=self.user.username, club=club.name)
        Moment.objects.create(
            type=MomentType.CLUB_CREATED,
            body = body,
            user = self.user,
            associated_club = club
        )

    def _book_rating(self, user, **kwargs):
        book = kwargs['book']
        rating = kwargs['rating']
        body = "{user} has rated {book} a {rating}.".format(user=self.user, book=book.name, rating=rating)
        Moment.objects.create(
            type=MomentType.BOOK_RATING,
            body = body,
            user = self.user,
            associated_book = book
        )
