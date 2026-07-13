from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = "Import initial data into PostgreSQL"

    def handle(self, *args, **kwargs):
        if os.path.exists("project_data.json"):
            self.stdout.write("Importing project_data.json...")
            call_command("loaddata", "project_data.json")
            self.stdout.write(self.style.SUCCESS("Data imported successfully."))
        else:
            self.stdout.write(self.style.WARNING("project_data.json not found."))