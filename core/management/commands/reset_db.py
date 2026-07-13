from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = "Reset PostgreSQL database"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE django_session CASCADE;")
            cursor.execute("TRUNCATE TABLE auth_user CASCADE;")
            cursor.execute("TRUNCATE TABLE core_profile CASCADE;")
            cursor.execute("TRUNCATE TABLE core_hostel CASCADE;")
            cursor.execute("TRUNCATE TABLE dashboard_fileitem CASCADE;")

        self.stdout.write(self.style.SUCCESS("Database cleared."))