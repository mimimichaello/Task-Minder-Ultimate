# Generated by Django 4.2.7 on 2023-11-14 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_accept_friend_request', 'Can accept friend requests')]},
        ),
    ]
