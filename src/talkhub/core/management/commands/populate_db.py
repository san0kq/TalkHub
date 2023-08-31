from typing import Any

from django.core.management.base import BaseCommand

from talkhub.populate_db import run


class Command(BaseCommand):
    help = "Populates the database with random data"

    def handle(self, *args: Any, **options: Any) -> None:
        run()
