# Generated by Django 3.2.5 on 2022-02-06 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20220206_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.IntegerField(choices=[(0, 'Follow request'), (1, 'Meeting reminder'), (2, 'Club created'), (3, 'Club joined'), (4, 'Received club leadership'), (5, 'New notification')], default=5),
        ),
    ]
