from typing import Any

from django.core.management.base import BaseCommand

from talkhub.populate_db import run_populate_db


class Command(BaseCommand):
    help = "Populates the database with random data"

    def add_arguments(self, parser):
        parser.add_argument("records number", type=int, help="The desired number of records")

    def handle(self, *args: Any, **options: Any) -> None:
        records_number = options["records number"]
        run_populate_db(records_number=records_number)
