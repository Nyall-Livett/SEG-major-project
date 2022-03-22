# Generated by Django 3.2.5 on 2022-03-21 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='theme',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Juvenile Fiction', 'Juvenile Fiction'), ('Biography & Autobiography', 'Biography & Autobiography'), ('Humor', 'Humor'), ('History', 'History'), ('Religion', 'Religion'), ('Juvenile Nonfiction', 'Juvenile Nonfiction'), ('Social Science', 'Social Science'), ('Body, Mind & Spirit', 'Body, Mind & Spirit'), ('Business & Economics', 'Business & Economics'), ('Family & Relationships', 'Family & Relationships'), ('Self-Help', 'Self-Help'), ('Health & Fitness', 'Health & Fitness'), ('Cooking', 'Cooking'), ('Travel', 'Travel'), ('True Crime', 'True Crime'), ('Psychology', 'Psychology'), ('Literary Criticism', 'Literary Criticism'), ('Poetry', 'Poetry'), ('Science', 'Science'), ('Drama', 'Drama'), ('Computers', 'Computers'), ('Political Science', 'Political Science'), ('Nature', 'Nature'), ('Philosophy', 'Philosophy'), ('Detective and mystery stories', 'Detective and mystery stories'), ('Performing Arts', 'Performing Arts'), ('Reference', 'Reference'), ('Language Arts & Disciplines', 'Language Arts & Disciplines'), ('Comics & Graphic Novels', 'Comics & Graphic Novels'), ('Art', 'Art'), ('Pets', 'Pets'), ('Literary Collections', 'Literary Collections'), ('Sports & Recreation', 'Sports & Recreation'), ('Medical', 'Medical'), ('Education', 'Education'), ('Crafts & Hobbies', 'Crafts & Hobbies'), ('Adventure stories', 'Adventure stories'), ("Children's stories", "Children's stories"), ('American fiction', 'American fiction'), ('Music', 'Music'), ('Domestic fiction', 'Domestic fiction'), ('Animals', 'Animals'), ('Gardening', 'Gardening'), ('Horror tales', 'Horror tales'), ('Foreign Language Study', 'Foreign Language Study'), ('House & Home', 'House & Home'), ('Law', 'Law'), ('English fiction', 'English fiction'), ('England', 'England'), ('Friendship', 'Friendship'), ('Brothers and sisters', 'Brothers and sisters'), ('Adultery', 'Adultery'), ('Science fiction', 'Science fiction'), ('Technology & Engineering', 'Technology & Engineering'), ('Fantasy', 'Fantasy'), ('California', 'California'), ('Americans', 'Americans'), ('Cats', 'Cats'), ('Families', 'Families'), ('Intelligence service', 'Intelligence service'), ('Games & Activities', 'Games & Activities'), ('Adolescence', 'Adolescence'), ('Games', 'Games'), ('Fantasy fiction', 'Fantasy fiction'), ('Great Britain', 'Great Britain'), ('Middle West', 'Middle West'), ('Babysitters', 'Babysitters'), ('Actors', 'Actors'), ('Photography', 'Photography'), ('Christian life', 'Christian life'), ('African American men', 'African American men'), ('German fiction', 'German fiction'), ('Diary fiction', 'Diary fiction'), ('Bible', 'Bible'), ('Rapture (Christian eschatology)', 'Rapture (Christian eschatology)'), ('Dogs', 'Dogs'), ('Adventure and adventurers', 'Adventure and adventurers'), ('Architecture', 'Architecture'), ('Australia', 'Australia'), ('Authors, American', 'Authors, American'), ('British and Irish fiction (Fictional works by one author).', 'British and Irish fiction (Fictional works by one author).'), ('JUVENILE FICTION', 'JUVENILE FICTION'), ('Young Adult Fiction', 'Young Adult Fiction'), ('Conduct of life', 'Conduct of life'), ('Mathematics', 'Mathematics'), ('Dune (Imaginary place)', 'Dune (Imaginary place)'), ('Boys', 'Boys'), ('Crime', 'Crime'), ('Antiques & Collectibles', 'Antiques & Collectibles'), ('London (England)', 'London (England)'), ('American literature', 'American literature'), ('American wit and humor', 'American wit and humor'), ('City and town life', 'City and town life'), ('African Americans', 'African Americans'), ('Fathers and sons', 'Fathers and sons'), ('Child psychologists', 'Child psychologists'), ('Christmas stories', 'Christmas stories'), ('United States', 'United States'), ('Abortion', 'Abortion'), ('Man-woman relationships', 'Man-woman relationships'), ('American poetry', 'American poetry'), ('HISTORY', 'HISTORY'), ('English language', 'English language'), ('France', 'France'), ('Businessmen', 'Businessmen'), ('British', 'British'), ('Dent, Arthur (Fictitious character)', 'Dent, Arthur (Fictitious character)'), ('Blake, Anita (Fictitious character)', 'Blake, Anita (Fictitious character)'), ('Interpersonal relations', 'Interpersonal relations'), ('Boston (Mass.)', 'Boston (Mass.)'), ('Interplanetary voyages', 'Interplanetary voyages'), ('Romance fiction', 'Romance fiction'), ('Fairy tales', 'Fairy tales'), ('Businesswomen', 'Businesswomen'), ('Murder', 'Murder'), ('Humorous stories', 'Humorous stories'), ('Canada', 'Canada'), ('French fiction', 'French fiction'), ('Geishas', 'Geishas'), ('Children', 'Children'), ('Chocolate', 'Chocolate'), ('Artificial intelligence', 'Artificial intelligence'), ('Design', 'Design'), ('Dragons', 'Dragons'), ('Arctic regions', 'Arctic regions'), ("Children's stories, American", "Children's stories, American"), ('Ghost stories', 'Ghost stories'), ('Africa', 'Africa'), ('Assassins', 'Assassins'), ('Bears', 'Bears'), ('Character', 'Character'), ('Brothers', 'Brothers'), ('Horror stories.', 'Horror stories.'), ('Authors, English', 'Authors, English'), ('African American women', 'African American women'), ('BIOGRAPHY & AUTOBIOGRAPHY', 'BIOGRAPHY & AUTOBIOGRAPHY'), ('Fantasy fiction, American', 'Fantasy fiction, American'), ('Life on other planets', 'Life on other planets'), ('Arthurian romances', 'Arthurian romances'), ('Death', 'Death'), ('Artists', 'Artists'), ('American drama', 'American drama'), ('Books and reading', 'Books and reading'), ('Historical fiction', 'Historical fiction'), ('Dinosaurs', 'Dinosaurs'), ('Curiosities and wonders', 'Curiosities and wonders'), ('Cousins', 'Cousins'), ('Transportation', 'Transportation'), ('Fiction in English', 'Fiction in English'), ("Children's stories, English", "Children's stories, English"), ('China', 'China'), ('Extraterrestrial beings', 'Extraterrestrial beings'), ('Amsterdam (Netherlands)', 'Amsterdam (Netherlands)'), ('Audiobooks', 'Audiobooks'), ("Children's stories, American.", "Children's stories, American."), ('Indians of North America', 'Indians of North America'), ('Country life', 'Country life'), ('Angels', 'Angels'), ('Trials (Murder)', 'Trials (Murder)'), ('Egypt', 'Egypt'), ('Science fiction, American', 'Science fiction, American'), ("Children's literature", "Children's literature"), ('Christian fiction', 'Christian fiction'), ('Motion picture actors and actresses', 'Motion picture actors and actresses'), ('Love stories', 'Love stories'), ('Baggins, Frodo (Fictitious character)', 'Baggins, Frodo (Fictitious character)'), ('Cancer', 'Cancer'), ('Materia medica', 'Materia medica'), ('Blind', 'Blind'), ('Aunts', 'Aunts'), ('Bildungsromans', 'Bildungsromans'), ('Covenant, Thomas (Fictitious character)', 'Covenant, Thomas (Fictitious character)'), ('Crisis management in government', 'Crisis management in government'), ('Community colleges', 'Community colleges'), ('Boarding schools', 'Boarding schools'), ('Canadian fiction', 'Canadian fiction'), ('Frontier and pioneer life', 'Frontier and pioneer life'), ('American wit and humor, Pictorial', 'American wit and humor, Pictorial'), ('Comic books, strips, etc', 'Comic books, strips, etc'), ('Criminals', 'Criminals'), ('Divorce', 'Divorce'), ('Cornwall (England : County)', 'Cornwall (England : County)'), ('Chicago (Ill.)', 'Chicago (Ill.)'), ('Schools', 'Schools'), ('Miscellaneous 1', 'Miscellaneous 1'), ('Miscellaneous 2', 'Miscellaneous 2'), ('Miscellaneous 3', 'Miscellaneous 3'), ('Miscellaneous 4', 'Miscellaneous 4'), ('Miscellaneous 5', 'Miscellaneous 5'), ('Miscellaneous 6', 'Miscellaneous 6'), ('Miscellaneous 7', 'Miscellaneous 7'), ('Miscellaneous 8', 'Miscellaneous 8'), ('Miscellaneous 9', 'Miscellaneous 9'), ('Miscellaneous 10', 'Miscellaneous 10')], default='Fiction', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_genre',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Juvenile Fiction', 'Juvenile Fiction'), ('Biography & Autobiography', 'Biography & Autobiography'), ('Humor', 'Humor'), ('History', 'History'), ('Religion', 'Religion'), ('Juvenile Nonfiction', 'Juvenile Nonfiction'), ('Social Science', 'Social Science'), ('Body, Mind & Spirit', 'Body, Mind & Spirit'), ('Business & Economics', 'Business & Economics'), ('Family & Relationships', 'Family & Relationships'), ('Self-Help', 'Self-Help'), ('Health & Fitness', 'Health & Fitness'), ('Cooking', 'Cooking'), ('Travel', 'Travel'), ('True Crime', 'True Crime'), ('Psychology', 'Psychology'), ('Literary Criticism', 'Literary Criticism'), ('Poetry', 'Poetry'), ('Science', 'Science'), ('Drama', 'Drama'), ('Computers', 'Computers'), ('Political Science', 'Political Science'), ('Nature', 'Nature'), ('Philosophy', 'Philosophy'), ('Detective and mystery stories', 'Detective and mystery stories'), ('Performing Arts', 'Performing Arts'), ('Reference', 'Reference'), ('Language Arts & Disciplines', 'Language Arts & Disciplines'), ('Comics & Graphic Novels', 'Comics & Graphic Novels'), ('Art', 'Art'), ('Pets', 'Pets'), ('Literary Collections', 'Literary Collections'), ('Sports & Recreation', 'Sports & Recreation'), ('Medical', 'Medical'), ('Education', 'Education'), ('Crafts & Hobbies', 'Crafts & Hobbies'), ('Adventure stories', 'Adventure stories'), ("Children's stories", "Children's stories"), ('American fiction', 'American fiction'), ('Music', 'Music'), ('Domestic fiction', 'Domestic fiction'), ('Animals', 'Animals'), ('Gardening', 'Gardening'), ('Horror tales', 'Horror tales'), ('Foreign Language Study', 'Foreign Language Study'), ('House & Home', 'House & Home'), ('Law', 'Law'), ('English fiction', 'English fiction'), ('England', 'England'), ('Friendship', 'Friendship'), ('Brothers and sisters', 'Brothers and sisters'), ('Adultery', 'Adultery'), ('Science fiction', 'Science fiction'), ('Technology & Engineering', 'Technology & Engineering'), ('Fantasy', 'Fantasy'), ('California', 'California'), ('Americans', 'Americans'), ('Cats', 'Cats'), ('Families', 'Families'), ('Intelligence service', 'Intelligence service'), ('Games & Activities', 'Games & Activities'), ('Adolescence', 'Adolescence'), ('Games', 'Games'), ('Fantasy fiction', 'Fantasy fiction'), ('Great Britain', 'Great Britain'), ('Middle West', 'Middle West'), ('Babysitters', 'Babysitters'), ('Actors', 'Actors'), ('Photography', 'Photography'), ('Christian life', 'Christian life'), ('African American men', 'African American men'), ('German fiction', 'German fiction'), ('Diary fiction', 'Diary fiction'), ('Bible', 'Bible'), ('Rapture (Christian eschatology)', 'Rapture (Christian eschatology)'), ('Dogs', 'Dogs'), ('Adventure and adventurers', 'Adventure and adventurers'), ('Architecture', 'Architecture'), ('Australia', 'Australia'), ('Authors, American', 'Authors, American'), ('British and Irish fiction (Fictional works by one author).', 'British and Irish fiction (Fictional works by one author).'), ('JUVENILE FICTION', 'JUVENILE FICTION'), ('Young Adult Fiction', 'Young Adult Fiction'), ('Conduct of life', 'Conduct of life'), ('Mathematics', 'Mathematics'), ('Dune (Imaginary place)', 'Dune (Imaginary place)'), ('Boys', 'Boys'), ('Crime', 'Crime'), ('Antiques & Collectibles', 'Antiques & Collectibles'), ('London (England)', 'London (England)'), ('American literature', 'American literature'), ('American wit and humor', 'American wit and humor'), ('City and town life', 'City and town life'), ('African Americans', 'African Americans'), ('Fathers and sons', 'Fathers and sons'), ('Child psychologists', 'Child psychologists'), ('Christmas stories', 'Christmas stories'), ('United States', 'United States'), ('Abortion', 'Abortion'), ('Man-woman relationships', 'Man-woman relationships'), ('American poetry', 'American poetry'), ('HISTORY', 'HISTORY'), ('English language', 'English language'), ('France', 'France'), ('Businessmen', 'Businessmen'), ('British', 'British'), ('Dent, Arthur (Fictitious character)', 'Dent, Arthur (Fictitious character)'), ('Blake, Anita (Fictitious character)', 'Blake, Anita (Fictitious character)'), ('Interpersonal relations', 'Interpersonal relations'), ('Boston (Mass.)', 'Boston (Mass.)'), ('Interplanetary voyages', 'Interplanetary voyages'), ('Romance fiction', 'Romance fiction'), ('Fairy tales', 'Fairy tales'), ('Businesswomen', 'Businesswomen'), ('Murder', 'Murder'), ('Humorous stories', 'Humorous stories'), ('Canada', 'Canada'), ('French fiction', 'French fiction'), ('Geishas', 'Geishas'), ('Children', 'Children'), ('Chocolate', 'Chocolate'), ('Artificial intelligence', 'Artificial intelligence'), ('Design', 'Design'), ('Dragons', 'Dragons'), ('Arctic regions', 'Arctic regions'), ("Children's stories, American", "Children's stories, American"), ('Ghost stories', 'Ghost stories'), ('Africa', 'Africa'), ('Assassins', 'Assassins'), ('Bears', 'Bears'), ('Character', 'Character'), ('Brothers', 'Brothers'), ('Horror stories.', 'Horror stories.'), ('Authors, English', 'Authors, English'), ('African American women', 'African American women'), ('BIOGRAPHY & AUTOBIOGRAPHY', 'BIOGRAPHY & AUTOBIOGRAPHY'), ('Fantasy fiction, American', 'Fantasy fiction, American'), ('Life on other planets', 'Life on other planets'), ('Arthurian romances', 'Arthurian romances'), ('Death', 'Death'), ('Artists', 'Artists'), ('American drama', 'American drama'), ('Books and reading', 'Books and reading'), ('Historical fiction', 'Historical fiction'), ('Dinosaurs', 'Dinosaurs'), ('Curiosities and wonders', 'Curiosities and wonders'), ('Cousins', 'Cousins'), ('Transportation', 'Transportation'), ('Fiction in English', 'Fiction in English'), ("Children's stories, English", "Children's stories, English"), ('China', 'China'), ('Extraterrestrial beings', 'Extraterrestrial beings'), ('Amsterdam (Netherlands)', 'Amsterdam (Netherlands)'), ('Audiobooks', 'Audiobooks'), ("Children's stories, American.", "Children's stories, American."), ('Indians of North America', 'Indians of North America'), ('Country life', 'Country life'), ('Angels', 'Angels'), ('Trials (Murder)', 'Trials (Murder)'), ('Egypt', 'Egypt'), ('Science fiction, American', 'Science fiction, American'), ("Children's literature", "Children's literature"), ('Christian fiction', 'Christian fiction'), ('Motion picture actors and actresses', 'Motion picture actors and actresses'), ('Love stories', 'Love stories'), ('Baggins, Frodo (Fictitious character)', 'Baggins, Frodo (Fictitious character)'), ('Cancer', 'Cancer'), ('Materia medica', 'Materia medica'), ('Blind', 'Blind'), ('Aunts', 'Aunts'), ('Bildungsromans', 'Bildungsromans'), ('Covenant, Thomas (Fictitious character)', 'Covenant, Thomas (Fictitious character)'), ('Crisis management in government', 'Crisis management in government'), ('Community colleges', 'Community colleges'), ('Boarding schools', 'Boarding schools'), ('Canadian fiction', 'Canadian fiction'), ('Frontier and pioneer life', 'Frontier and pioneer life'), ('American wit and humor, Pictorial', 'American wit and humor, Pictorial'), ('Comic books, strips, etc', 'Comic books, strips, etc'), ('Criminals', 'Criminals'), ('Divorce', 'Divorce'), ('Cornwall (England : County)', 'Cornwall (England : County)'), ('Chicago (Ill.)', 'Chicago (Ill.)'), ('Schools', 'Schools'), ('Miscellaneous 1', 'Miscellaneous 1'), ('Miscellaneous 2', 'Miscellaneous 2'), ('Miscellaneous 3', 'Miscellaneous 3'), ('Miscellaneous 4', 'Miscellaneous 4'), ('Miscellaneous 5', 'Miscellaneous 5'), ('Miscellaneous 6', 'Miscellaneous 6'), ('Miscellaneous 7', 'Miscellaneous 7'), ('Miscellaneous 8', 'Miscellaneous 8'), ('Miscellaneous 9', 'Miscellaneous 9'), ('Miscellaneous 10', 'Miscellaneous 10')], default='Fiction', max_length=100),
        ),
    ]
