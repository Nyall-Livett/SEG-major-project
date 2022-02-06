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

        elif type == NotificationType.CLUB_ACCEPTED:
            return self._club_accepted

        elif type == NotificationType.CLUB_REJECTED:
            return self._club_rejected

        elif type == NotificationType.CLUB_TRANSFERRED:
            return self._club_transferred

        elif type == NotificationType.FRIEND_REQUEST:
            return self._friend_request

        elif type == NotificationType.MEETING_SOON:
            return self._meeting_soon


    def _create_club(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        description = "You have created the {club}.".format(club=club_name)
        Notification.objects.create(
            type=NotificationType.CLUB_CREATED,
            title = NotificationType.CLUB_CREATED.label,
            description= description, receiver=receiver
        )


    def _club_accepted(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        description = "You have been accepted into {club}.".format(club=club_name)
        Notification.objects.create(
            type=NotificationType.CLUB_ACCEPTED,
            title = NotificationType.CLUB_ACCEPTED.label,
            description= description, receiver=receiver
        )


    def _club_rejected(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        description = "You have been rejected from {club}.".format(club=club_name)
        Notification.objects.create(
            type=NotificationType.CLUB_REJECTED,
            title = NotificationType.CLUB_REJECTED.label,
            description= description, receiver=receiver
        )


    def _club_transferred(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        username = kwargs['username']
        description = "You have transferred {club} to {user}".format(club=club_name, user=username)
        Notification.objects.create(
            type=NotificationType.CLUB_TRANSFERRED,
            title = NotificationType.CLUB_TRANSFERRED.label,
            description= description, receiver=receiver
        )


    def _club_received(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        description = "You have gained leadership of {club}".format(club=club_name)
        Notification.objects.create(
            type=NotificationType.CLUB_RECEIVED,
            title = NotificationType.CLUB_RECEIVED.label,
            description= description, receiver=receiver
        )


    def _follow_request(self, title, receiver, **kwargs):
        username = kwargs['username']
        description = "You have received a follow request from {user}, click to accept or reject".format(user=username)
        Notification.objects.create(
            type=NotificationType.FOLLOW_REQUEST,
            title = NotificationType.FOLLOW_REQUEST.label,
            description= description, receiver=receiver
        )


    def _meeting_soon(self, title, receiver, **kwargs):
        club_name = kwargs['username']
        description = "You have transferred {club} to {user}".format(club=club_name, user=username)
        Notification.objects.create(
            type=NotificationType.FOLLOW_REQUEST,
            title = NotificationType.FOLLOW_REQUEST.label,
            description= description, receiver=receiver
        )
