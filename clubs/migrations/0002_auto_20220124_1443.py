# Generated by Django 3.2.5 on 2022-01-24 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=2048)),
                ('themes', models.CharField(max_length=256)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='founder_of', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='clubs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]