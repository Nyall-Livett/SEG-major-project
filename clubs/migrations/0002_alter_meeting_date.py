# Generated by Django 3.2.5 on 2022-02-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.CharField(max_length=300),
        ),
    ]