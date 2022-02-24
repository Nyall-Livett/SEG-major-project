# Generated by Django 3.2.5 on 2022-01-28 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meeting_club', to='clubs.club'),
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='member_selected',
        ),
        migrations.AddField(
            model_name='meeting',
            name='member_selected',
            field=models.ManyToManyField(related_name='meeting_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
