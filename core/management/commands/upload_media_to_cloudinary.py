import os

import cloudinary
import cloudinary.uploader

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Hostel, MaleRoom, FemaleRoom, Profile


class Command(BaseCommand):
    help = "Upload all existing media to Cloudinary"


    def upload(self, image_field, folder):

        if not image_field:
            return None

        local_file = os.path.join(
            settings.MEDIA_ROOT,
            image_field.name
        )

        if not os.path.isfile(local_file):
            self.stdout.write(
                self.style.WARNING(f"Missing: {local_file}")
            )
            return None

        result = cloudinary.uploader.upload(
            local_file,
            folder=folder,
            overwrite=True,
        )

        return result["public_id"]


    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS("\nUploading Hostel Images...\n"))

        for hostel in Hostel.objects.all():

            public_id = self.upload(hostel.image, "hostels")

            if public_id:
                hostel.image = public_id
                hostel.save(update_fields=["image"])


        self.stdout.write(self.style.SUCCESS("\nUploading Male Rooms...\n"))

        for room in MaleRoom.objects.all():

            public_id = self.upload(room.image, "male_rooms")

            if public_id:
                room.image = public_id
                room.save(update_fields=["image"])


        self.stdout.write(self.style.SUCCESS("\nUploading Female Rooms...\n"))

        for room in FemaleRoom.objects.all():

            public_id = self.upload(room.image, "female_rooms")

            if public_id:
                room.image = public_id
                room.save(update_fields=["image"])


        self.stdout.write(self.style.SUCCESS("\nUploading Profiles...\n"))

        for profile in Profile.objects.all():

            public_id = self.upload(profile.image, "profiles")

            if public_id:
                profile.image = public_id
                profile.save(update_fields=["image"])


        self.stdout.write(
            self.style.SUCCESS(
                "\n🎉 ALL MEDIA SUCCESSFULLY UPLOADED TO CLOUDINARY\n"
            )
        )