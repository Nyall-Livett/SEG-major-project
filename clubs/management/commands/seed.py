from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
import random
from clubs.models import User, Post, Club, Book, Meeting

class Command(BaseCommand):
    """The database seeder."""

    PASSWORD = "Password123"
    CLUB_COUNT = 3
    USER_COUNT = 10
    POST_COUNT_PER_CLUB = 21

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.seed_users()
        print()
        self.seed_clubs()
        print()
        # self.club_list = list(Club.objects.all())
        # for club in self.club_list:
        #     print()
        #     print(f'Seeding {club.name} Posts')
        #     self.seed_posts(club = club)
        #     print()
        print()
        print('Users, Clubs and Posts seeding complete.')

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
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            bio = bio,
            username = username,
            password=Command.PASSWORD,
        )

    def _create_club(self):
        name = self.faker.first_name()
        leader = random.choice(User.objects.all())
        Club.objects.create(
            name = self._club_name(name),
            description = self.faker.text(max_nb_chars=2048),
            theme = self.faker.text(max_nb_chars=512),
            maximum_members = 3,
            leader = leader
        )

    def seed_clubs(self):
        club_count = Club.objects.all().count()
        seed_try = club_count
        print(f'Clubs seeded: {club_count}',  end='\r')
        while seed_try < Command.CLUB_COUNT:
            try:
                club = self._create_club()
                club_count += 1
                print(f'Clubs seeded: {club_count}',  end='\r')
            except (IntegrityError):
                continue
            seed_try += 1

    # def seed_posts(self,club):
    #     post_count = Post.objects.all().count()
    #     seed_try = post_count
    #     print(f'Posts seeded: {post_count}',  end='\r')
    #     while seed_try < Command.POST_COUNT_PER_CLUB:
    #         try:
    #             club = self._create_post(club)
    #             club_count += 1
    #             print(f'Posts seeded: {post_count}',  end='\r')
    #         except (IntegrityError):
    #             continue
    #         seed_try += 1
    #
    # def _create_post(self,club):
    #     title = self.faker.text(max_nb_chars=64)
    #     body = self.faker.text(max_nb_chars=300)
    #     author = random.choice(club.members.all())
    #     post = Post.objects.create(
    #         title = title,
    #         body = body,
    #         club = club,
    #         author = author,
    #     )

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _club_name(self, name):
        name = f'{name} Book Club'
        return name
