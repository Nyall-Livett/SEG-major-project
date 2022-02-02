# Generated by Django 3.2.5 on 2022-02-02 18:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow_requests',
            field=models.ManyToManyField(related_name='sent_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]