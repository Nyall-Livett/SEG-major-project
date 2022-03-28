from clubs.models import Notification
from clubs.enums import NotificationType


class CreateNotification:

    def notify(self, type, receiver, kwargs):
        notifier = self._get_notifier(type)
        notifier(type, receiver, **kwargs)

    """docstring forCreateNotification."""
    def _get_notifier(self, type):

        if type == NotificationType.CLUB_CREATED:
            return self._create_club

        elif type == NotificationType.CLUB_JOINED:
            return self._club_joined

        elif type == NotificationType.CLUB_RECEIVED:
            return self._club_received

        elif type == NotificationType.FOLLOW_REQUEST:
            return self._follow_request

<<<<<<< HEAD
=======
        elif type == NotificationType.MEETING_SOON:
            return self._meeting_soon
        
>>>>>>> Test-Fix-Refactor
        elif type == NotificationType.MEETING_CREATED:
            return self._meeting_created


    def _meeting_created(self, title, receiver, **kwargs):
        club = kwargs['club']
        description = "A meeting has been created in {club}.".format(club=club.name)
        Notification.objects.create(
            type = NotificationType.MEETING_CREATED,
            title = NotificationType.MEETING_CREATED.label,
            description = description,
            receiver = receiver,
            associated_club = club.id
        )

    def _create_club(self, title, receiver, **kwargs):
        club = kwargs['club']
        description = "You have created the {club}.".format(club=club.name)
        Notification.objects.create(
            type=NotificationType.CLUB_CREATED,
            title = NotificationType.CLUB_CREATED.label,
            description= description,
            receiver=receiver,
            associated_club = club.id
        )


    def _club_joined(self, title, receiver, **kwargs):
        club = kwargs['club']
        description = "You have been accepted into {club}.".format(club=club.name)
        Notification.objects.create(
            type=NotificationType.CLUB_JOINED,
            title = NotificationType.CLUB_JOINED.label,
            description= description,
            receiver=receiver,
            associated_club = club.id
        )

    def _club_received(self, title, receiver, **kwargs):
        club = kwargs['club']
        description = "You have gained leadership of {club}".format(club=club.name)
        Notification.objects.create(
            type=NotificationType.CLUB_RECEIVED,
            title = NotificationType.CLUB_RECEIVED.label,
            description= description,
            receiver=receiver,
            associated_club = club.id

        )


    def _follow_request(self, title, receiver, **kwargs):
        user = kwargs['user']
        description = "You have received a follow request from {user}, click to accept or reject".format(user=user.username)
        Notification.objects.create(
            type=NotificationType.FOLLOW_REQUEST,
            title = NotificationType.FOLLOW_REQUEST.label,
            description= description,
            receiver=receiver,
            associated_user = user.id
        )


    def _meeting_created(self, title, receiver, **kwargs):
        club = kwargs['club']
        description = "You have a meeting soon for the {club}".format(club=club.name)
        Notification.objects.create(
            type=NotificationType.MEETING_CREATED,
            title = NotificationType.MEETING_CREATED.label,
            description= description,
            receiver=receiver,
            associated_club = club.id
        )
