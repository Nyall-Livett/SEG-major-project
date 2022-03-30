# Generated by Django 3.2.5 on 2022-03-29 14:10

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.CharField(blank=True, max_length=520)),
                ('city', models.CharField(max_length=200)),
                ('favourite_character', models.CharField(blank=True, max_length=50)),
                ('favourite_genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Juvenile Fiction', 'Juvenile Fiction'), ('Biography & Autobiography', 'Biography & Autobiography'), ('Humor', 'Humor'), ('History', 'History'), ('Religion', 'Religion'), ('Juvenile Nonfiction', 'Juvenile Nonfiction'), ('Social Science', 'Social Science'), ('Body, Mind & Spirit', 'Body, Mind & Spirit'), ('Business & Economics', 'Business & Economics'), ('Family & Relationships', 'Family & Relationships'), ('Self-Help', 'Self-Help'), ('Health & Fitness', 'Health & Fitness'), ('Cooking', 'Cooking'), ('Travel', 'Travel'), ('True Crime', 'True Crime'), ('Psychology', 'Psychology'), ('Literary Criticism', 'Literary Criticism'), ('Poetry', 'Poetry'), ('Science', 'Science'), ('Drama', 'Drama'), ('Computers', 'Computers'), ('Political Science', 'Political Science'), ('Nature', 'Nature'), ('Philosophy', 'Philosophy'), ('Detective and mystery stories', 'Detective and mystery stories'), ('Performing Arts', 'Performing Arts'), ('Reference', 'Reference'), ('Language Arts & Disciplines', 'Language Arts & Disciplines'), ('Comics & Graphic Novels', 'Comics & Graphic Novels'), ('Art', 'Art'), ('Pets', 'Pets'), ('Literary Collections', 'Literary Collections'), ('Sports & Recreation', 'Sports & Recreation'), ('Medical', 'Medical'), ('Education', 'Education'), ('Crafts & Hobbies', 'Crafts & Hobbies'), ('Adventure stories', 'Adventure stories'), ("Children's stories", "Children's stories"), ('American fiction', 'American fiction'), ('Music', 'Music'), ('Domestic fiction', 'Domestic fiction'), ('Animals', 'Animals'), ('Gardening', 'Gardening'), ('Horror tales', 'Horror tales'), ('Foreign Language Study', 'Foreign Language Study'), ('House & Home', 'House & Home'), ('Law', 'Law'), ('English fiction', 'English fiction'), ('England', 'England'), ('Friendship', 'Friendship'), ('Brothers and sisters', 'Brothers and sisters'), ('Adultery', 'Adultery'), ('Science fiction', 'Science fiction'), ('Technology & Engineering', 'Technology & Engineering'), ('Fantasy', 'Fantasy'), ('California', 'California'), ('Americans', 'Americans'), ('Cats', 'Cats'), ('Families', 'Families'), ('Intelligence service', 'Intelligence service'), ('Games & Activities', 'Games & Activities'), ('Adolescence', 'Adolescence'), ('Games', 'Games'), ('Fantasy fiction', 'Fantasy fiction'), ('Great Britain', 'Great Britain'), ('Middle West', 'Middle West'), ('Babysitters', 'Babysitters'), ('Actors', 'Actors'), ('Photography', 'Photography'), ('Christian life', 'Christian life'), ('African American men', 'African American men'), ('German fiction', 'German fiction'), ('Diary fiction', 'Diary fiction'), ('Bible', 'Bible'), ('Rapture (Christian eschatology)', 'Rapture (Christian eschatology)'), ('Dogs', 'Dogs'), ('Adventure and adventurers', 'Adventure and adventurers'), ('Architecture', 'Architecture'), ('Australia', 'Australia'), ('Authors, American', 'Authors, American'), ('British and Irish fiction (Fictional works by one author).', 'British and Irish fiction (Fictional works by one author).'), ('JUVENILE FICTION', 'JUVENILE FICTION'), ('Young Adult Fiction', 'Young Adult Fiction'), ('Conduct of life', 'Conduct of life'), ('Mathematics', 'Mathematics'), ('Dune (Imaginary place)', 'Dune (Imaginary place)'), ('Boys', 'Boys'), ('Crime', 'Crime'), ('Antiques & Collectibles', 'Antiques & Collectibles'), ('London (England)', 'London (England)'), ('American literature', 'American literature'), ('American wit and humor', 'American wit and humor'), ('City and town life', 'City and town life'), ('African Americans', 'African Americans'), ('Fathers and sons', 'Fathers and sons'), ('Child psychologists', 'Child psychologists'), ('Christmas stories', 'Christmas stories'), ('United States', 'United States'), ('Abortion', 'Abortion'), ('Man-woman relationships', 'Man-woman relationships'), ('American poetry', 'American poetry'), ('HISTORY', 'HISTORY'), ('English language', 'English language'), ('France', 'France'), ('Businessmen', 'Businessmen'), ('British', 'British'), ('Dent, Arthur (Fictitious character)', 'Dent, Arthur (Fictitious character)'), ('Blake, Anita (Fictitious character)', 'Blake, Anita (Fictitious character)'), ('Interpersonal relations', 'Interpersonal relations'), ('Boston (Mass.)', 'Boston (Mass.)'), ('Interplanetary voyages', 'Interplanetary voyages'), ('Romance fiction', 'Romance fiction'), ('Fairy tales', 'Fairy tales'), ('Businesswomen', 'Businesswomen'), ('Murder', 'Murder'), ('Humorous stories', 'Humorous stories'), ('Canada', 'Canada'), ('French fiction', 'French fiction'), ('Geishas', 'Geishas'), ('Children', 'Children'), ('Chocolate', 'Chocolate'), ('Artificial intelligence', 'Artificial intelligence'), ('Design', 'Design'), ('Dragons', 'Dragons'), ('Arctic regions', 'Arctic regions'), ("Children's stories, American", "Children's stories, American"), ('Ghost stories', 'Ghost stories'), ('Africa', 'Africa'), ('Assassins', 'Assassins'), ('Bears', 'Bears'), ('Character', 'Character'), ('Brothers', 'Brothers'), ('Horror stories.', 'Horror stories.'), ('Authors, English', 'Authors, English'), ('African American women', 'African American women'), ('BIOGRAPHY & AUTOBIOGRAPHY', 'BIOGRAPHY & AUTOBIOGRAPHY'), ('Fantasy fiction, American', 'Fantasy fiction, American'), ('Life on other planets', 'Life on other planets'), ('Arthurian romances', 'Arthurian romances'), ('Death', 'Death'), ('Artists', 'Artists'), ('American drama', 'American drama'), ('Books and reading', 'Books and reading'), ('Historical fiction', 'Historical fiction'), ('Dinosaurs', 'Dinosaurs'), ('Curiosities and wonders', 'Curiosities and wonders'), ('Cousins', 'Cousins'), ('Transportation', 'Transportation'), ('Fiction in English', 'Fiction in English'), ("Children's stories, English", "Children's stories, English"), ('China', 'China'), ('Extraterrestrial beings', 'Extraterrestrial beings'), ('Amsterdam (Netherlands)', 'Amsterdam (Netherlands)'), ('Audiobooks', 'Audiobooks'), ("Children's stories, American.", "Children's stories, American."), ('Indians of North America', 'Indians of North America'), ('Country life', 'Country life'), ('Angels', 'Angels'), ('Trials (Murder)', 'Trials (Murder)'), ('Egypt', 'Egypt'), ('Science fiction, American', 'Science fiction, American'), ("Children's literature", "Children's literature"), ('Christian fiction', 'Christian fiction'), ('Motion picture actors and actresses', 'Motion picture actors and actresses'), ('Love stories', 'Love stories'), ('Baggins, Frodo (Fictitious character)', 'Baggins, Frodo (Fictitious character)'), ('Cancer', 'Cancer'), ('Materia medica', 'Materia medica'), ('Blind', 'Blind'), ('Aunts', 'Aunts'), ('Bildungsromans', 'Bildungsromans'), ('Covenant, Thomas (Fictitious character)', 'Covenant, Thomas (Fictitious character)'), ('Crisis management in government', 'Crisis management in government'), ('Community colleges', 'Community colleges'), ('Boarding schools', 'Boarding schools'), ('Canadian fiction', 'Canadian fiction'), ('Frontier and pioneer life', 'Frontier and pioneer life'), ('American wit and humor, Pictorial', 'American wit and humor, Pictorial'), ('Comic books, strips, etc', 'Comic books, strips, etc'), ('Criminals', 'Criminals'), ('Divorce', 'Divorce'), ('Cornwall (England : County)', 'Cornwall (England : County)'), ('Chicago (Ill.)', 'Chicago (Ill.)'), ('Schools', 'Schools'), ('Miscellaneous 1', 'Miscellaneous 1'), ('Miscellaneous 2', 'Miscellaneous 2'), ('Miscellaneous 3', 'Miscellaneous 3'), ('Miscellaneous 4', 'Miscellaneous 4'), ('Miscellaneous 5', 'Miscellaneous 5'), ('Miscellaneous 6', 'Miscellaneous 6'), ('Miscellaneous 7', 'Miscellaneous 7'), ('Miscellaneous 8', 'Miscellaneous 8'), ('Miscellaneous 9', 'Miscellaneous 9'), ('Miscellaneous 10', 'Miscellaneous 10')], default='Fiction', max_length=100)),
                ('favourite_author', models.CharField(blank=True, max_length=50)),
                ('using_gravatar', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=2048)),
                ('author', models.CharField(max_length=64)),
                ('publication_year', models.CharField(blank=True, max_length=4)),
                ('publisher', models.CharField(blank=True, max_length=64)),
                ('image_url_s', models.URLField(blank=True)),
                ('image_url_m', models.URLField(blank=True)),
                ('image_url_l', models.URLField(blank=True)),
                ('category', models.CharField(blank=True, max_length=64)),
                ('grouped_category', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'ordering': ['isbn'],
            },
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=2048)),
                ('city', models.CharField(max_length=200)),
                ('theme', models.CharField(choices=[('Fiction', 'Fiction'), ('Juvenile Fiction', 'Juvenile Fiction'), ('Biography & Autobiography', 'Biography & Autobiography'), ('Humor', 'Humor'), ('History', 'History'), ('Religion', 'Religion'), ('Juvenile Nonfiction', 'Juvenile Nonfiction'), ('Social Science', 'Social Science'), ('Body, Mind & Spirit', 'Body, Mind & Spirit'), ('Business & Economics', 'Business & Economics'), ('Family & Relationships', 'Family & Relationships'), ('Self-Help', 'Self-Help'), ('Health & Fitness', 'Health & Fitness'), ('Cooking', 'Cooking'), ('Travel', 'Travel'), ('True Crime', 'True Crime'), ('Psychology', 'Psychology'), ('Literary Criticism', 'Literary Criticism'), ('Poetry', 'Poetry'), ('Science', 'Science'), ('Drama', 'Drama'), ('Computers', 'Computers'), ('Political Science', 'Political Science'), ('Nature', 'Nature'), ('Philosophy', 'Philosophy'), ('Detective and mystery stories', 'Detective and mystery stories'), ('Performing Arts', 'Performing Arts'), ('Reference', 'Reference'), ('Language Arts & Disciplines', 'Language Arts & Disciplines'), ('Comics & Graphic Novels', 'Comics & Graphic Novels'), ('Art', 'Art'), ('Pets', 'Pets'), ('Literary Collections', 'Literary Collections'), ('Sports & Recreation', 'Sports & Recreation'), ('Medical', 'Medical'), ('Education', 'Education'), ('Crafts & Hobbies', 'Crafts & Hobbies'), ('Adventure stories', 'Adventure stories'), ("Children's stories", "Children's stories"), ('American fiction', 'American fiction'), ('Music', 'Music'), ('Domestic fiction', 'Domestic fiction'), ('Animals', 'Animals'), ('Gardening', 'Gardening'), ('Horror tales', 'Horror tales'), ('Foreign Language Study', 'Foreign Language Study'), ('House & Home', 'House & Home'), ('Law', 'Law'), ('English fiction', 'English fiction'), ('England', 'England'), ('Friendship', 'Friendship'), ('Brothers and sisters', 'Brothers and sisters'), ('Adultery', 'Adultery'), ('Science fiction', 'Science fiction'), ('Technology & Engineering', 'Technology & Engineering'), ('Fantasy', 'Fantasy'), ('California', 'California'), ('Americans', 'Americans'), ('Cats', 'Cats'), ('Families', 'Families'), ('Intelligence service', 'Intelligence service'), ('Games & Activities', 'Games & Activities'), ('Adolescence', 'Adolescence'), ('Games', 'Games'), ('Fantasy fiction', 'Fantasy fiction'), ('Great Britain', 'Great Britain'), ('Middle West', 'Middle West'), ('Babysitters', 'Babysitters'), ('Actors', 'Actors'), ('Photography', 'Photography'), ('Christian life', 'Christian life'), ('African American men', 'African American men'), ('German fiction', 'German fiction'), ('Diary fiction', 'Diary fiction'), ('Bible', 'Bible'), ('Rapture (Christian eschatology)', 'Rapture (Christian eschatology)'), ('Dogs', 'Dogs'), ('Adventure and adventurers', 'Adventure and adventurers'), ('Architecture', 'Architecture'), ('Australia', 'Australia'), ('Authors, American', 'Authors, American'), ('British and Irish fiction (Fictional works by one author).', 'British and Irish fiction (Fictional works by one author).'), ('JUVENILE FICTION', 'JUVENILE FICTION'), ('Young Adult Fiction', 'Young Adult Fiction'), ('Conduct of life', 'Conduct of life'), ('Mathematics', 'Mathematics'), ('Dune (Imaginary place)', 'Dune (Imaginary place)'), ('Boys', 'Boys'), ('Crime', 'Crime'), ('Antiques & Collectibles', 'Antiques & Collectibles'), ('London (England)', 'London (England)'), ('American literature', 'American literature'), ('American wit and humor', 'American wit and humor'), ('City and town life', 'City and town life'), ('African Americans', 'African Americans'), ('Fathers and sons', 'Fathers and sons'), ('Child psychologists', 'Child psychologists'), ('Christmas stories', 'Christmas stories'), ('United States', 'United States'), ('Abortion', 'Abortion'), ('Man-woman relationships', 'Man-woman relationships'), ('American poetry', 'American poetry'), ('HISTORY', 'HISTORY'), ('English language', 'English language'), ('France', 'France'), ('Businessmen', 'Businessmen'), ('British', 'British'), ('Dent, Arthur (Fictitious character)', 'Dent, Arthur (Fictitious character)'), ('Blake, Anita (Fictitious character)', 'Blake, Anita (Fictitious character)'), ('Interpersonal relations', 'Interpersonal relations'), ('Boston (Mass.)', 'Boston (Mass.)'), ('Interplanetary voyages', 'Interplanetary voyages'), ('Romance fiction', 'Romance fiction'), ('Fairy tales', 'Fairy tales'), ('Businesswomen', 'Businesswomen'), ('Murder', 'Murder'), ('Humorous stories', 'Humorous stories'), ('Canada', 'Canada'), ('French fiction', 'French fiction'), ('Geishas', 'Geishas'), ('Children', 'Children'), ('Chocolate', 'Chocolate'), ('Artificial intelligence', 'Artificial intelligence'), ('Design', 'Design'), ('Dragons', 'Dragons'), ('Arctic regions', 'Arctic regions'), ("Children's stories, American", "Children's stories, American"), ('Ghost stories', 'Ghost stories'), ('Africa', 'Africa'), ('Assassins', 'Assassins'), ('Bears', 'Bears'), ('Character', 'Character'), ('Brothers', 'Brothers'), ('Horror stories.', 'Horror stories.'), ('Authors, English', 'Authors, English'), ('African American women', 'African American women'), ('BIOGRAPHY & AUTOBIOGRAPHY', 'BIOGRAPHY & AUTOBIOGRAPHY'), ('Fantasy fiction, American', 'Fantasy fiction, American'), ('Life on other planets', 'Life on other planets'), ('Arthurian romances', 'Arthurian romances'), ('Death', 'Death'), ('Artists', 'Artists'), ('American drama', 'American drama'), ('Books and reading', 'Books and reading'), ('Historical fiction', 'Historical fiction'), ('Dinosaurs', 'Dinosaurs'), ('Curiosities and wonders', 'Curiosities and wonders'), ('Cousins', 'Cousins'), ('Transportation', 'Transportation'), ('Fiction in English', 'Fiction in English'), ("Children's stories, English", "Children's stories, English"), ('China', 'China'), ('Extraterrestrial beings', 'Extraterrestrial beings'), ('Amsterdam (Netherlands)', 'Amsterdam (Netherlands)'), ('Audiobooks', 'Audiobooks'), ("Children's stories, American.", "Children's stories, American."), ('Indians of North America', 'Indians of North America'), ('Country life', 'Country life'), ('Angels', 'Angels'), ('Trials (Murder)', 'Trials (Murder)'), ('Egypt', 'Egypt'), ('Science fiction, American', 'Science fiction, American'), ("Children's literature", "Children's literature"), ('Christian fiction', 'Christian fiction'), ('Motion picture actors and actresses', 'Motion picture actors and actresses'), ('Love stories', 'Love stories'), ('Baggins, Frodo (Fictitious character)', 'Baggins, Frodo (Fictitious character)'), ('Cancer', 'Cancer'), ('Materia medica', 'Materia medica'), ('Blind', 'Blind'), ('Aunts', 'Aunts'), ('Bildungsromans', 'Bildungsromans'), ('Covenant, Thomas (Fictitious character)', 'Covenant, Thomas (Fictitious character)'), ('Crisis management in government', 'Crisis management in government'), ('Community colleges', 'Community colleges'), ('Boarding schools', 'Boarding schools'), ('Canadian fiction', 'Canadian fiction'), ('Frontier and pioneer life', 'Frontier and pioneer life'), ('American wit and humor, Pictorial', 'American wit and humor, Pictorial'), ('Comic books, strips, etc', 'Comic books, strips, etc'), ('Criminals', 'Criminals'), ('Divorce', 'Divorce'), ('Cornwall (England : County)', 'Cornwall (England : County)'), ('Chicago (Ill.)', 'Chicago (Ill.)'), ('Schools', 'Schools'), ('Miscellaneous 1', 'Miscellaneous 1'), ('Miscellaneous 2', 'Miscellaneous 2'), ('Miscellaneous 3', 'Miscellaneous 3'), ('Miscellaneous 4', 'Miscellaneous 4'), ('Miscellaneous 5', 'Miscellaneous 5'), ('Miscellaneous 6', 'Miscellaneous 6'), ('Miscellaneous 7', 'Miscellaneous 7'), ('Miscellaneous 8', 'Miscellaneous 8'), ('Miscellaneous 9', 'Miscellaneous 9'), ('Miscellaneous 10', 'Miscellaneous 10')], default='Fiction', max_length=100)),
                ('maximum_members', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(64)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')),
                ('applicants', models.ManyToManyField(blank=True, related_name='applicants', to=settings.AUTH_USER_MODEL)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='leader_of', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='clubs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('body', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club', to='clubs.club')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('type', models.IntegerField(choices=[(0, 'Follow request'), (1, 'Meeting scheduled'), (2, 'Club created'), (3, 'Club joined'), (4, 'Received club leadership'), (5, 'New notification')], default=5)),
                ('description', models.CharField(max_length=256)),
                ('read', models.BooleanField(default=False)),
                ('acted_upon', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('associated_user', models.IntegerField(blank=True, null=True)),
                ('associated_club', models.IntegerField(blank=True, null=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=128)),
                ('type', models.IntegerField(choices=[(0, 'Custom'), (1, 'Became Friends'), (2, 'Club Created'), (3, 'Book Rating')])),
                ('likes', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('associated_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associated_book', to='clubs.book')),
                ('associated_club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associated_club', to='clubs.club')),
                ('associated_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='associated_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('finish', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('URL', models.CharField(blank=True, max_length=300)),
                ('passcode', models.CharField(blank=True, max_length=100, null=True)),
                ('notes', models.CharField(blank=True, max_length=300)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book', to='clubs.book')),
                ('chosen_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='clubs.club')),
                ('next_book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_book', to='clubs.book')),
            ],
        ),
        migrations.CreateModel(
            name='CustomAvatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('blue', 'Blue'), ('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')], max_length=28, null=True)),
                ('icon', models.CharField(choices=[('brutus', 'Brutus'), ('bill', 'Bill'), ('genie', 'Genie'), ('grinch', 'Grinch'), ('jerry', 'Jerry'), ('keiji', 'Keiji'), ('kermit', 'Kermit'), ('kuroo', 'Kuroo'), ('lion', 'Lion'), ('melody', 'Melody'), ('mermaid', 'Mermaid'), ('morty', 'Morty'), ('turtle', 'Turtle'), ('cheburashka', 'Cheburashka'), ('amethyst', 'Amethyst')], max_length=28, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='favourite_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fav_book', to='clubs.book'),
        ),
        migrations.AddField(
            model_name='user',
            name='follow_requests',
            field=models.ManyToManyField(related_name='sent_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='followees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='want_to_read_next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_read', to='clubs.book'),
        ),
        migrations.CreateModel(
            name='BooksRead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('like', 'like'), ('neutral', 'neutral'), ('dislike', 'dislike')], max_length=30)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewing', to='clubs.book')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('reviewer', 'book')},
            },
        ),
    ]
