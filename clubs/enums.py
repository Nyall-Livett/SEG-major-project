from django.db import models

class NotificationType(models.IntegerChoices):
    FOLLOW_REQUEST = 0, "Follow request"
    MEETING_SOON = 1, "Meeting reminder"
    CLUB_CREATED = 2, "Club created"
    CLUB_ACCEPTED = 3, "Club joined"
    CLUB_REJECTED = 4, "Club rejection"
    CLUB_TRANSFERRED = 5, "Club transfer"
    CLUB_RECEIVED = 6, "Received club"
    DEFAULT= 7, "New notification"
