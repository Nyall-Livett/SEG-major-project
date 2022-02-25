# Generated by Django 3.2.5 on 2022-02-25 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_meeting_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_author',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='favourite_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fav_book', to='clubs.book'),
        ),
        migrations.AddField(
            model_name='user',
            name='favourite_character',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='favourite_genre',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='want_to_read_next',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_book', to='clubs.book'),
        ),
    ]
