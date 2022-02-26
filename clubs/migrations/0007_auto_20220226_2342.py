# Generated by Django 3.2.5 on 2022-02-26 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_auto_20220225_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='members',
        ),
        migrations.AddField(
            model_name='meeting',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='meeting',
            name='next_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_book', to='clubs.book'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book', to='clubs.book'),
        ),
        migrations.AlterField(
            model_name='user',
            name='want_to_read_next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_read', to='clubs.book'),
        ),
    ]
