from django.db import models

class NotificationType(models.IntegerChoices):
    FOLLOW_REQUEST = 0, "Follow request"
    MEETING_SOON = 1, "Meeting reminder"
    CLUB_CREATED = 2, "Club created"
    CLUB_JOINED = 3, "Club joined"
    CLUB_RECEIVED = 4, "Received club leadership"
    DEFAULT = 5, "New notification"

class MomentType(models.IntegerChoices):
    CUSTOM = 0
    BECAME_FRIENDS = 1
    CLUB_CREATED = 2
    BOOK_RECOMMENDATION = 3
    READING_NEW_BOOK = 4

class AvatarIcon(models.IntegerChoices):
    BRUTUS = 0, "brutus"
    BILL = 1, "bill"
    GENIE = 2, "genie"
    GRINCH = 3, "grinch"
    JERRY = 4, "jerry"
    KEIJI = 5, "keiji"
    KERMIT = 6, "kermit"
    KUROO = 7, "kuroo"
    LION = 8, "lion"
    MELODY = 9, "melody"
    MERMAID = 10, "mermaid"
    MORTY = 11, "morty"
    TURTLE = 12, "turtle"
    CHEBURASHKA = 13, "cheburashka"
    AMETHYST = 14, "amethyst"

class AvatarColor(models.IntegerChoices):
    BLUE = 0, "#70bbfb"
    RED = 1, "#ff7d7d"
    YELLOW = 2, "#f1fc5a"
    GREEN = 3, "#55d634"
