# Generated by Django 3.2.5 on 2022-02-05 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(blank=True, default='', max_length=2048),
        ),
        migrations.AlterField(
            model_name='book',
            name='image_url_l',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='image_url_m',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='image_url_s',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='', max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.CharField(blank=True, default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
