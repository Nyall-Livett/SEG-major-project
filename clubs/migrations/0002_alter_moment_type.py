# Generated by Django 3.2.5 on 2022-03-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moment',
            name='type',
            field=models.IntegerField(choices=[(0, 'Custom'), (1, 'Became Friends'), (2, 'Club Created'), (3, 'Book Rating')]),
        ),
    ]
