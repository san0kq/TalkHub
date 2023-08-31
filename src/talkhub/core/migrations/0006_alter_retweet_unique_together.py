# Generated by Django 4.2.4 on 2023-08-30 21:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0005_rename_users_notification_recipients_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="retweet",
            unique_together={("tweet", "user")},
        ),
    ]