from enum import Enum
from clubs.models import Notification

class NotificationType(Enum):
    FRIEND_REQUEST = "You have recieved a friend request from {user}"
    MEETING_SOON = "You have a meeting starting soon"
    CLUB_CREATED = "You have created the {club}."
    CLUB_ACCEPTED = "You have joined {club}"
    CLUB_REJECTED = "You have been rejected from {club}"
    CLUB_TRANSFERRED = "You have transferred {club} to {user}"
    CLUB_RECEIVED = "You have transferred {club} to {user}"

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
        Notification.objects.create(title= title.value.format(club=club_name), receiver=receiver)

    def _club_accepted(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        Notification.objects.create(title= title.value.format(club=club_name), receiver=receiver)

    def _club_rejected(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        Notification.objects.create(title= title.value.format(club=club_name), receiver=receiver)

    def _club_transferred(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        user_name = kwargs['user_name']
        Notification.objects.create(title= title.value.format(club=club_name, user=user_name), receiver=receiver)

    def _friend_request(self, title, receiver, **kwargs):
        user_name = kwargs['user_name']
        Notification.objects.create(title= title.value.format(user=user_name), receiver=receiver)

    def _meeting_soon(self, title, receiver, **kwargs):
        club_name = kwargs['club_name']
        Notification.objects.create(title= title.value.format(club=club_name), receiver=receiver)
