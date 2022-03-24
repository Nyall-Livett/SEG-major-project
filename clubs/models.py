"""Models in the clubs app."""
from pickle import TRUE
from re import T
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import request
from libgravatar import Gravatar
from django.utils import timezone
from datetime import date, datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from clubs.enums import NotificationType, MomentType, AvatarColor, AvatarIcon
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File
from pathlib import Path
from django.core.files.base import ContentFile



import pytz

GENRE_CATEGORY_CHOICES = [
('Fiction', 'Fiction'),
('Juvenile Fiction', 'Juvenile Fiction'),
('Biography & Autobiography', 'Biography & Autobiography'),
('Humor', 'Humor'),
('History', 'History'),
('Religion', 'Religion'),
('Juvenile Nonfiction', 'Juvenile Nonfiction'),
('Social Science', 'Social Science'),
('Body, Mind & Spirit', 'Body, Mind & Spirit'),
('Business & Economics', 'Business & Economics'),
('Family & Relationships', 'Family & Relationships'),
('Self-Help', 'Self-Help'),
('Health & Fitness', 'Health & Fitness'),
('Cooking', 'Cooking'),
('Travel', 'Travel'),
('True Crime', 'True Crime'),
('Psychology', 'Psychology'),
('Literary Criticism', 'Literary Criticism'),
('Poetry', 'Poetry'),
('Science', 'Science'),
('Drama', 'Drama'),
('Computers', 'Computers'),
('Political Science', 'Political Science'),
('Nature', 'Nature'),
('Philosophy', 'Philosophy'),
('Detective and mystery stories', 'Detective and mystery stories'),
('Performing Arts', 'Performing Arts'),
('Reference', 'Reference'),
('Language Arts & Disciplines', 'Language Arts & Disciplines'),
('Comics & Graphic Novels', 'Comics & Graphic Novels'),
('Art', 'Art'),
('Pets', 'Pets'),
('Literary Collections', 'Literary Collections'),
('Sports & Recreation', 'Sports & Recreation'),
('Medical', 'Medical'),
('Education', 'Education'),
('Crafts & Hobbies', 'Crafts & Hobbies'),
('Adventure stories', 'Adventure stories'),
("Children's stories", "Children's stories"),
('American fiction', 'American fiction'),
('Music', 'Music'),
('Domestic fiction', 'Domestic fiction'),
('Animals', 'Animals'),
('Gardening', 'Gardening'),
('Horror tales', 'Horror tales'),
('Foreign Language Study', 'Foreign Language Study'),
('House & Home', 'House & Home'),
('Law', 'Law'),
('English fiction', 'English fiction'),
('England', 'England'),
('Friendship', 'Friendship'),
('Brothers and sisters', 'Brothers and sisters'),
('Adultery', 'Adultery'),
('Science fiction', 'Science fiction'),
('Technology & Engineering', 'Technology & Engineering'),
('Fantasy', 'Fantasy'),
('California', 'California'),
('Americans', 'Americans'),
('Cats', 'Cats'),
('Families', 'Families'),
('Intelligence service', 'Intelligence service'),
('Games & Activities', 'Games & Activities'),
('Adolescence', 'Adolescence'),
('Games', 'Games'),
('Fantasy fiction', 'Fantasy fiction'),
('Great Britain', 'Great Britain'),
('Middle West', 'Middle West'),
('Babysitters', 'Babysitters'),
('Actors', 'Actors'),
('Photography', 'Photography'),
('Christian life', 'Christian life'),
('African American men', 'African American men'),
('German fiction', 'German fiction'),
('Diary fiction', 'Diary fiction'),
('Bible', 'Bible'),
('Rapture (Christian eschatology)', 'Rapture (Christian eschatology)'),
('Dogs', 'Dogs'),
('Adventure and adventurers', 'Adventure and adventurers'),
('Architecture', 'Architecture'),
('Australia', 'Australia'),
('Authors, American', 'Authors, American'),
('British and Irish fiction (Fictional works by one author).', 'British and Irish fiction (Fictional works by one author).'),
('JUVENILE FICTION', 'JUVENILE FICTION'),
('Young Adult Fiction', 'Young Adult Fiction'),
('Conduct of life', 'Conduct of life'),
('Mathematics', 'Mathematics'),
('Dune (Imaginary place)', 'Dune (Imaginary place)'),
('Boys', 'Boys'),
('Crime', 'Crime'),
('Antiques & Collectibles', 'Antiques & Collectibles'),
('London (England)', 'London (England)'),
('American literature', 'American literature'),
('American wit and humor', 'American wit and humor'),
('City and town life', 'City and town life'),
('African Americans', 'African Americans'),
('Fathers and sons', 'Fathers and sons'),
('Child psychologists', 'Child psychologists'),
('Christmas stories', 'Christmas stories'),
('United States', 'United States'),
('Abortion', 'Abortion'),
('Man-woman relationships', 'Man-woman relationships'),
('American poetry', 'American poetry'),
('HISTORY', 'HISTORY'),
('English language', 'English language'),
('France', 'France'),
('Businessmen', 'Businessmen'),
('British', 'British'),
('Dent, Arthur (Fictitious character)', 'Dent, Arthur (Fictitious character)'),
('Blake, Anita (Fictitious character)', 'Blake, Anita (Fictitious character)'),
('Interpersonal relations', 'Interpersonal relations'),
('Boston (Mass.)', 'Boston (Mass.)'),
('Interplanetary voyages', 'Interplanetary voyages'),
('Romance fiction', 'Romance fiction'),
('Fairy tales', 'Fairy tales'),
('Businesswomen', 'Businesswomen'),
('Murder', 'Murder'),
('Humorous stories', 'Humorous stories'),
('Canada', 'Canada'),
('French fiction', 'French fiction'),
('Geishas', 'Geishas'),
('Children', 'Children'),
('Chocolate', 'Chocolate'),
('Artificial intelligence', 'Artificial intelligence'),
('Design', 'Design'),
('Dragons', 'Dragons'),
('Arctic regions', 'Arctic regions'),
("Children's stories, American", "Children's stories, American"),
('Ghost stories', 'Ghost stories'),
('Africa', 'Africa'),
('Assassins', 'Assassins'),
('Bears', 'Bears'),
('Character', 'Character'),
('Brothers', 'Brothers'),
('Horror stories.', 'Horror stories.'),
('Authors, English', 'Authors, English'),
('African American women', 'African American women'),
('BIOGRAPHY & AUTOBIOGRAPHY', 'BIOGRAPHY & AUTOBIOGRAPHY'),
('Fantasy fiction, American', 'Fantasy fiction, American'),
('Life on other planets', 'Life on other planets'),
('Arthurian romances', 'Arthurian romances'),
('Death', 'Death'),
('Artists', 'Artists'),
('American drama', 'American drama'),
('Books and reading', 'Books and reading'),
('Historical fiction', 'Historical fiction'),
('Dinosaurs', 'Dinosaurs'),
('Curiosities and wonders', 'Curiosities and wonders'),
('Cousins', 'Cousins'),
('Transportation', 'Transportation'),
('Fiction in English', 'Fiction in English'),
("Children's stories, English", "Children's stories, English"),
('China', 'China'),
('Extraterrestrial beings', 'Extraterrestrial beings'),
('Amsterdam (Netherlands)', 'Amsterdam (Netherlands)'),
('Audiobooks', 'Audiobooks'),
("Children's stories, American.", "Children's stories, American."),
('Indians of North America', 'Indians of North America'),
('Country life', 'Country life'),
('Angels', 'Angels'),
('Trials (Murder)', 'Trials (Murder)'),
('Egypt', 'Egypt'),
('Science fiction, American', 'Science fiction, American'),
("Children's literature", "Children's literature"),
('Christian fiction', 'Christian fiction'),
('Motion picture actors and actresses', 'Motion picture actors and actresses'),
('Love stories', 'Love stories'),
('Baggins, Frodo (Fictitious character)', 'Baggins, Frodo (Fictitious character)'),
('Cancer', 'Cancer'),
('Materia medica', 'Materia medica'),
('Blind', 'Blind'),
('Aunts', 'Aunts'),
('Bildungsromans', 'Bildungsromans'),
('Covenant, Thomas (Fictitious character)', 'Covenant, Thomas (Fictitious character)'),
('Crisis management in government', 'Crisis management in government'),
('Community colleges', 'Community colleges'),
('Boarding schools', 'Boarding schools'),
('Canadian fiction', 'Canadian fiction'),
('Frontier and pioneer life', 'Frontier and pioneer life'),
('American wit and humor, Pictorial', 'American wit and humor, Pictorial'),
('Comic books, strips, etc', 'Comic books, strips, etc'),
('Criminals', 'Criminals'),
('Divorce', 'Divorce'),
('Cornwall (England : County)', 'Cornwall (England : County)'),
('Chicago (Ill.)', 'Chicago (Ill.)'),
('Schools', 'Schools'),
('Miscellaneous 1', 'Miscellaneous 1'),
('Miscellaneous 2', 'Miscellaneous 2'),
('Miscellaneous 3', 'Miscellaneous 3'),
('Miscellaneous 4', 'Miscellaneous 4'),
('Miscellaneous 5', 'Miscellaneous 5'),
('Miscellaneous 6', 'Miscellaneous 6'),
('Miscellaneous 7', 'Miscellaneous 7'),
('Miscellaneous 8', 'Miscellaneous 8'),
('Miscellaneous 9', 'Miscellaneous 9'),
('Miscellaneous 10', 'Miscellaneous 10'),
]

# default values are used for any existing instances of books.
class Book(models.Model):
    """Book model"""
    isbn = models.CharField(max_length=13, unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=2048, blank=True)
    author = models.CharField(max_length=64, blank=False)
    publication_year = models.CharField(max_length=4, blank=True)
    publisher = models.CharField(max_length=64, blank=True)
    image_url_s = models.URLField(max_length=200, blank=True)
    image_url_m = models.URLField(max_length=200, blank=True)
    image_url_l = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=64, blank=True)
    grouped_category =  models.CharField(max_length=64, blank=True)

    class Meta:
        """Model options."""
        ordering = ['isbn']

    def __str__(self):
        return self.name

class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name="followees")
    follow_requests = models.ManyToManyField('self', symmetrical=False, related_name='sent_requests')
    favourite_book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.SET_NULL, related_name='fav_book')
    favourite_character = models.CharField(max_length=50, blank=True)
    favourite_genre = models.CharField(max_length=100, choices=GENRE_CATEGORY_CHOICES, default='Fiction')
    favourite_author = models.CharField(max_length=50, blank=True)
    want_to_read_next = models.ForeignKey(Book, blank=True, null=True, on_delete=models.SET_NULL, related_name='next_read')
    using_gravatar = models.BooleanField(default=False)

    class Meta:
        """Model options."""
        ordering = ['last_name', 'first_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=50)

    def future_meetings(self):
        utc=pytz.UTC
        list = []
        for i in Meeting.objects.all():
            if i.date.replace(tzinfo=utc) > datetime.now().replace(tzinfo=utc):
                list.append(i)

        return list

    def previous_meetings(self):
        utc=pytz.UTC
        list = []
        for i in Meeting.objects.all():
            if i.date.replace(tzinfo=utc) <= datetime.now().replace(tzinfo=utc):
                list.append(i)
        return list

    def now(self):
        utc=pytz.UTC
        return datetime.now().replace(tzinfo=utc)


    def notification_count(self):
        return self.notification_set.filter(read=False).count()

    def get_unread_notifications(self):
        return self.notification_set.filter(read=False)

    def notifications_not_acted_upon_count(self):
        return self.notification_set.filter(acted_upon=False).count()

    def clubBooks(self):
        list = []
        for i in Book.objects.all():
                list.append(i)
        return len(list) > 0

    """ methods relating to follow system """
    def add_follower(self, user):
        """ add other users as followers to self """
        self.followers.add(user)

    def follow(self, user):
        """ follow user """
        self.followees.add(user)

    def unfollow(self, user):
        """ unfollow user self is following """
        self.followees.remove(user)

    def followers_count(self):
        """ number of followers self has """
        return self.followers.count()

    def followees_count(self):
        """ number of users self follows """
        return self.followees.count()

    def is_following(self, user):
        """ returns if self follows a given user """
        return user in self.followees.all()

    def toggle_follow(self, user):
        """ unfollows if self follows the user, follows if self does not follow the user """
        if self.is_following(user):
            self.unfollow(user)
        else:
            self.follow(user)

    """ methods relating to follow requests """
    def send_follow_request(self, user):
        """ send follow requests to a user """
        self.sent_requests.add(user)

    def is_request_sent(self, user):
        """ returns if a follow request to a user has already been sent """
        return user in self.sent_requests.all()

    def has_request(self, user):
        """ returns if a follow request has been sent by a user """
        return user in self.follow_requests.all()

    def accept_request(self, user):
        """ accepts a follow request from a user """
        if self.has_request(user):
            self.follow_requests.remove(user)
            self.add_follower(user)

    def reject_request(self, user):
        """ rejects a follow request from a user """
        if self.has_request(user):
            self.follow_requests.remove(user)


class Club(models.Model):
    """Club model"""
    name = models.CharField(max_length=64, unique=True, blank=False)
    description = models.CharField(max_length=2048, blank=False)
    leader = models.ForeignKey(User, related_name="leader_of", on_delete=models.PROTECT)
    members = models.ManyToManyField(User, symmetrical=True, related_name="clubs")
    applicants = models.ManyToManyField(User,blank=True, related_name="applicants" )
    theme = models.CharField(max_length=100, choices=GENRE_CATEGORY_CHOICES, default='Fiction')
    maximum_members = models.IntegerField(blank=False, default=2, validators=[MinValueValidator(2), MaxValueValidator(64)])
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    formats = {
        'JPEG': 'jpeg',
        'JPG': 'jpeg',
        'PNG': 'png'
    }

    #  Override the delete method to delete the image from S3
    def delete(self):
        if self.image != None:
            self.image.delete(save=False)
        if self.thumbnail != None:
            self.thumbnail.delete(save=False)
        super().delete()


    class Meta:
        """Model options."""
        ordering = ['-id']

    def add_or_remove_member(self, user):
        if user not in self.members.all():
            user.clubs.add(self)
        else:
            user.clubs.remove(self)

    def applicant_manager(self, user):
        if user not in self.applicants.all():
            user.applicants.add(self)

    def acceptmembership(self, user):
        user.applicants.remove(self)
        user.clubs.add(self)

    def rejectmembership(self,user):
        user.applicants.remove(self)

    def grant_leadership(self, user):
        self.leader = user
        self.save()

    def member_count(self):
        return f"{self.members.count()}/{self.maximum_members}"

    def __str__(self):
        return self.name

    def is_member(self,request):
        for i in self.members.all():
            if request == i:
                return True
        return False


    def crop_image(self, image, height, width, x, y):
        # Open the image in pillow
        originalImage = Image.open(self.image)

        # Get crop dimensions
        pLeft, pRight = x.split(',')
        pTop, pBottom = y.split(',')
        heightSF = originalImage.height / int(float(height))
        widthSF = originalImage.width / int(float(width))
        size = 250, 250

        left = max(1, min((int(pLeft) * widthSF), originalImage.width- 1))
        right = max(1, min((int(pRight) * widthSF), originalImage.width- 1))
        top = max(1, min((int(pTop) * heightSF), originalImage.height- 1))
        bottom = max(1, min((int(pBottom) * heightSF), originalImage.height- 1))


        img_filename = f'{self.name}_pp'
        imCrop = originalImage.crop((left, top, right, bottom))
        buffer = BytesIO()
        imCrop.thumbnail(size, Image.ANTIALIAS)
        imCrop.save(buffer, format=self.formats[image.format])


        data = buffer.getvalue()
        self.image.save(img_filename, ContentFile(data))

        self.create_thumbnail(imCrop, self.formats[image.format] )

    def create_thumbnail(self, imCrop, format):
        thumbnail_size = 50, 50
        buffer = BytesIO()
        imCrop.thumbnail(thumbnail_size, Image.ANTIALIAS)
        imCrop.save(buffer, format=format)

        data = buffer.getvalue()
        img_filename = f'{self.name}_tn'
        self.thumbnail.save(img_filename, ContentFile(data))



class Notification(models.Model):
    """Notification model."""
    title = models.CharField(max_length=128, blank=False)
    type = models.IntegerField(blank=False, default = NotificationType.DEFAULT, choices = NotificationType.choices)
    description = models.CharField(max_length=256, blank=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    acted_upon = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
    associated_user = models.IntegerField(blank=True, null=True)
    associated_club = models.IntegerField(blank=True, null=True)

class Moment(models.Model):
    """docstring for Moments."""

    body = models.CharField(blank=False, max_length=128)
    type = models.IntegerField(blank=False, choices = MomentType.choices)
    likes = models.IntegerField(blank=False, default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, blank=False)
    associated_user = models.ForeignKey(User, blank=True, null=True, related_name="associated_user", on_delete=models.CASCADE)
    associated_club = models.ForeignKey(Club, blank=True, null=True, related_name="associated_club", on_delete=models.CASCADE)


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length = 64, blank=False)
    body = models.CharField(max_length = 300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(Club,on_delete=models.CASCADE, related_name="club")
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author")

    class Meta:
        """Model options."""
        ordering = ['-created_at']

class Meeting(models.Model):
    """Meeting model"""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="meetings")
    date = models.DateTimeField("date", default=timezone.now)
    location = models.CharField(max_length=100, blank=True)
    URL = models.CharField(max_length=300, blank=True)
    passcode = models.CharField(blank=True, null=True, max_length=100)
    chosen_member = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.SET_NULL, related_name="book")
    next_book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.SET_NULL, related_name="next_book")
    notes = models.CharField(max_length=300, blank=True)

    def add_meeting(self, meeting):
        if meeting not in self.meeting.all():
            meeting.meeting_members.add(self)

class BooksRead(models.Model):
    """Book Read model - books read by a user with rating"""
    RATINGS = [
        ('like', 'like'),
        ('neutral', 'neutral'),
        ('dislike', 'dislike')
    ]
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=False, null=False, on_delete=models.CASCADE, related_name="reviewing")
    rating = models.CharField(max_length=30, choices=RATINGS)

    class Meta:
        unique_together = ['reviewer', 'book']

class CustomAvatar(models.Model):
    color = models.CharField(blank=False, null=True, max_length=28, choices = AvatarColor.choices)
    icon = models.CharField(blank=False, null=True, max_length=28, choices = AvatarIcon.choices)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
