from django.core.management.base import BaseCommand
from core.models import (
    Hostel,
    ExternalRoom,
    ExternalBooking,
)
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Migrate external rooms and bookings"

    def handle(self, *args, **kwargs):

        self.stdout.write("Migrating External Rooms...")

        for room in ExternalRoom.objects.using("default").all():

            try:

                hostel = Hostel.objects.using("postgres").get(pk=room.hostel_id)

                ExternalRoom.objects.using("postgres").update_or_create(
                    id=room.id,
                    defaults={
                        "hostel": hostel,
                        "room_number": room.room_number,
                        "room_type": room.room_type,
                        "capacity": room.capacity,
                        "price": room.price,
                        "status": room.status,
                    },
                )

            except Exception as e:
                self.stdout.write(f"Skipped room {room.id}: {e}")

        self.stdout.write(self.style.SUCCESS("External Rooms migrated."))


        self.stdout.write("Migrating External Bookings...")

        for booking in ExternalBooking.objects.using("default").all():

            try:

                user = User.objects.using("postgres").get(pk=booking.user_id)
                room = ExternalRoom.objects.using("postgres").get(pk=booking.room_id)

                hostel = None
                if booking.hostel_id:
                    hostel = Hostel.objects.using("postgres").get(pk=booking.hostel_id)

                ExternalBooking.objects.using("postgres").update_or_create(
                    id=booking.id,
                    defaults={
                        "user": user,
                        "hostel": hostel,
                        "room": room,
                        "booking_reference": booking.booking_reference,
                        "full_name": booking.full_name,
                        "email": booking.email,
                        "gender": booking.gender,
                        "phone": booking.phone,
                        "emergency_phone": booking.emergency_phone,
                        "duration": booking.duration,
                        "note": booking.note,
                        "status": booking.status,
                        "payment_deadline": booking.payment_deadline,
                        "created_at": booking.created_at,
                    },
                )

            except Exception as e:
                self.stdout.write(f"Skipped booking {booking.id}: {e}")

        self.stdout.write(self.style.SUCCESS("External Bookings migrated."))

        self.stdout.write(self.style.SUCCESS("🎉 ALL DATA MIGRATED SUCCESSFULLY"))