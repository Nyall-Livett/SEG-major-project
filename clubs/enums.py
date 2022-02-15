from django.db import models

class NotificationType(models.IntegerChoices):
    FOLLOW_REQUEST = 0, "Follow request"
    MEETING_SOON = 1, "Meeting reminder"
    CLUB_CREATED = 2, "Club created"
    CLUB_JOINED = 3, "Club joined"
    CLUB_RECEIVED = 4, "Received club leadership"
    DEFAULT = 5, "New notification"

class MomentType(models.IntegerChoices):
    BECAME_FRIENDS = 0
    CLUB_CREATED = 1
    BOOK_RECOMMENDATION = 2
    READING_NEW_BOOK = 3
