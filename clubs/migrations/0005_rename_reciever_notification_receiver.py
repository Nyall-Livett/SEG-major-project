# Generated by Django 3.2.5 on 2022-01-29 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_auto_20220129_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='reciever',
            new_name='receiver',
        ),
    ]
