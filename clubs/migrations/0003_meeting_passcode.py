# Generated by Django 3.2.5 on 2022-03-18 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_alter_club_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='passcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]