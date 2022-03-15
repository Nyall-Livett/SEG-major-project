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

class AvatarIcon(models.TextChoices):
    BRUTUS = "brutus"
    BILL = "bill"
    GENIE = "genie"
    GRINCH = "grinch"
    JERRY = "jerry"
    KEIJI = "keiji"
    KERMIT = "kermit"
    KUROO = "kuroo"
    LION = "lion"
    MELODY = "melody"
    MERMAID = "mermaid"
    MORTY = "morty"
    TURTLE = "turtle"
    CHEBURASHKA = "cheburashka"
    AMETHYST = "amethyst"

    @classmethod
    def list(cls):
        return list(map(lambda x: (x.value), AvatarIcon))

class AvatarColor(models.TextChoices):
    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

    @classmethod
    def list(cls):
        return list(map(lambda x: (x.value), AvatarColor))
