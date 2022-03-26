from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
import random
from clubs.models import User, Post, Club, Book
import os, csv
from ...helpers import generate_favourite_ratings
from clubs.factories.notification_factory import CreateNotification
from clubs.factories.moment_factory import CreateMoment
from clubs.enums import NotificationType, MomentType

class Command(BaseCommand):
    """The database seeder. Password is Password123 for all users seeded"""
    
    # Hash of Password123
    PASSWORD = "pbkdf2_sha256$260000$ZWkUBTmqpvVHC80qObjXY8$HCDKrbBS2UAj+rvmYw0Ba2yMN3SPJ3QDr1F8GjF6n7o="
    CLUB_COUNT = 4
    USER_COUNT = 8
    POST_COUNT_PER_CLUB = 4

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        #print('Seeding books... (It takes a few minutes.)')
        #self.seed_books()
        #print('Book seeding complete')
        self.seed_users()
        print()
        self.seed_clubs()
        print()
        self.add_users_to_clubs()
        self.club_list = list(Club.objects.all())
        for club in self.club_list:
            print()
            # print(f'Seeding {club.name} Posts...')
            self.seed_posts(club=club)
            print()
        print()
        print('Users, Clubs and Posts seeding complete.')

        #print()
        #self.seed_meetings()
        #print('Meetings seeding complete')

        print()
        self.add_followers_for_users()
        print('Followers added to all users')

        print()
        self.add_follow_request_for_users()
        print('Follow requests has been added for all users')

        # self.seed_books()
        # print('Book seeding complete')


    def add_follow_request_for_users(self):
        users = list(User.objects.all())
        no_of_follow_requests_to_add = User.objects.count() // 3
        if(no_of_follow_requests_to_add == 0):
            return
        
        for user in users:
            follow_requests_added = 0
            while(follow_requests_added != no_of_follow_requests_to_add):
                following_request_user = random.choice(users)
                while(not self._is_user_safe_to_add_as_follow_request):
                    following_request_user = random.choice(users)
                user.follow_requests.add(following_request_user)
                notifier = CreateNotification()
                notifier.notify(NotificationType.FOLLOW_REQUEST, user, {'user': following_request_user})
                follow_requests_added += 1


    def add_followers_for_users(self):
        users = list(User.objects.all())
        no_of_followers_to_add = User.objects.count() // 3
        if(no_of_followers_to_add == 0):
            return

        for user in users:
            followers_added = 0
            while(followers_added != no_of_followers_to_add):
                following_user = random.choice(users)
                while(not self._is_user_safe_to_add_as_follower(main_user=user, following_user=following_user)):
                    following_user = random.choice(users)
                user.add_follower(following_user)
                moment_notifier = CreateMoment()
                moment_notifier.notify(MomentType.BECAME_FRIENDS, user, {'other_user': following_user})
                followers_added += 1

    def _is_user_safe_to_add_as_follower(self, main_user, following_user):
        return (following_user != main_user and 
                not following_user.is_superuser and 
                not following_user in main_user.followers.all()) 

    def _is_user_safe_to_add_as_follow_request(self, main_user, following_request_user):
        return (self._is_user_safe_to_add_as_follower(main_user=main_user, following_user=following_request_user)
                and following_request_user not in main_user.follow_requests.all())

    def seed_users(self):
        user_count = User.objects.all().count()
        seed_try = user_count
        print(f'Users seeded: {user_count}',  end='\r')
        while seed_try < Command.USER_COUNT:
            try:
                self._create_user()
                user_count += 1
                print(f'Users seeded: {user_count}',  end='\r')
            except (IntegrityError):
                continue
            seed_try += 1

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = f'@{first_name}{last_name}'
        email = self._email(first_name,last_name)
        bio = self.faker.text(max_nb_chars=520)
        # favourite_book = self._favourite_book()
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            bio = bio,
            username = username,
            password=Command.PASSWORD,
        )
        # generate_favourite_ratings(favourite_book,user.id)

    def _create_club(self):
        name = self.faker.first_name()
        leader = random.choice(User.objects.all())
        while(leader.is_superuser):
            leader = random.choice(User.objects.all())

        club = Club.objects.create(
            name = self._club_name(name),
            description = self.faker.text(max_nb_chars=2048),
            theme = self.faker.text(max_nb_chars=512),
            maximum_members = 2,
            leader = leader
        )
        club.add_or_remove_member(leader)
        notifier = CreateNotification()
        notifier.notify(NotificationType.CLUB_CREATED, leader, {'club': club})
        moment_notifier = CreateMoment()
        moment_notifier.notify(MomentType.CLUB_CREATED, leader, {'club': club})

    def seed_clubs(self):
        club_count = Club.objects.all().count()
        seed_try = club_count
        print(f'Clubs seeded: {club_count}',  end='\r')
        while seed_try < Command.CLUB_COUNT:
            try:
                self._create_club()
                club_count += 1
                print(f'Clubs seeded: {club_count}',  end='\r')
            except (IntegrityError):
                continue
            seed_try += 1

    def add_users_to_clubs(self):
        user_list = list(User.objects.all())
        for user in user_list:
            club_list = list(Club.objects.all().exclude(leader=user))
            if (len(club_list)== 0):
                continue
            club = random.choice(club_list)
            club.add_or_remove_member(user)
            if(club.members.count()==club.maximum_members):
                club_list.remove(club)

    def seed_posts(self,club):
        post_count = Post.objects.all().filter(club=club).count()
        seed_try = post_count
        print(f'{club.name} Posts seeded: {post_count}',  end='\r')
        while seed_try < Command.POST_COUNT_PER_CLUB:
            try:
                self._create_post(club)
                post_count += 1
                print(f'{club.name} Posts seeded: {post_count}',  end='\r')
            except (IntegrityError):
                continue
            seed_try += 1

    def _create_post(self,club):
        title = self.faker.text(max_nb_chars=64)
        body = self.faker.text(max_nb_chars=300)
        author = random.choice(list(club.members.all()))
        post = Post.objects.create(
            title = title,
            body = body,
            club = club,
            author = author,
        )

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _club_name(self, name):
        name = f'{name} Book Club'
        return name

    def _favourite_book(self):
        favourite_book = random.choice(Book.objects.all())
        return favourite_book

    def seed_books(self):
        csv_file = os.getcwd()+ '/clubs/book_database/BX_Books_formatted.csv'
        with open(csv_file, encoding ='ISO-8859-1') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            for book in csv_reader:
                print("The first line of book seeder")
                print(book[0])
                if(book[0] != 'ISBN'):
                    try:
                        try:
                            _, created = Book.objects.update_or_create(
                                isbn = book[0].strip('"'),
                                name = book[1].strip('"'),
                                author = book[2].strip('"'),
                                publication_year = book[3].strip('"'),
                                publisher = book[4].strip('"'),
                                image_url_s = book[5].strip('"'),
                                image_url_m = book[6].strip('"'),
                                image_url_l = book[7].strip('"'),
                                category = book[8].strip('"').strip("'[]"),
                                grouped_category = book[9].strip('"').strip("'[]"),
                                description = book[10].strip('"')
                            )
                        except IndexError:
                            _, created = Book.objects.update_or_create(
                                isbn = book[0].strip('"'),
                                name = book[1].strip('"'),
                                author = book[2].strip('"'),
                                publication_year = book[3].strip('"'),
                                publisher = book[4].strip('"'),
                                image_url_s = book[5].strip('"'),
                                image_url_m = book[6].strip('"'),
                                image_url_l = book[7].strip('"'),
                            )
                    except IndexError:
                        messages.add_message(self.request, messages.WARNING, f"{book[0]} could not be added to the system.")
