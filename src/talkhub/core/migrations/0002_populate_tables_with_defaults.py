from typing import Any

from core.models import NotificationType, Rating
from django.db import migrations

DEFAULT_NOTIFICATION_TYPES = ("admin", "rating")
DEFAULT_RATINGS = ("like", "dislike")


def populate_notification_types_table(apps: Any, schema_editor: Any) -> None:
    for notification_type in DEFAULT_NOTIFICATION_TYPES:
        NotificationType.objects.create(name=notification_type)


def reverse_notification_types_table(apps: Any, schema_editor: Any) -> None:
    for notification_type in DEFAULT_NOTIFICATION_TYPES:
        NotificationType.objects.get(name=notification_type).delete()


def populate_ratings_table(apps: Any, schema_editor: Any) -> None:
    for rating in DEFAULT_RATINGS:
        Rating.objects.create(name=rating)


def reverse_ratings_table(apps: Any, schema_editor: Any) -> None:
    for rating in DEFAULT_RATINGS:
        Rating.objects.get(name=rating).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(code=populate_notification_types_table, reverse_code=reverse_notification_types_table),
        migrations.RunPython(code=populate_ratings_table, reverse_code=reverse_ratings_table),
    ]
