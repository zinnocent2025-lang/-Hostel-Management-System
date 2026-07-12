from core.models import SystemSettings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def bump_system_version():

    settings, created = (
        SystemSettings.objects.get_or_create(
            id=1
        )
    )

    settings.version += 1

    settings.save( update_fields=["version"])


from core.models import MaleBooking, FemaleBooking

from core.models import MaleBooking, FemaleBooking
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def update_room_occupancy(room):
    """
    Updates occupied beds automatically.
    Admin Occupied rooms are never overridden.
    """

    if room.__class__.__name__ == "MaleRoom":

        occupied = MaleBooking.objects.filter(
            room=room,
            status__in=["pending", "approved"]
        ).count()

    else:

        occupied = FemaleBooking.objects.filter(
            room=room,
            status__in=["pending", "approved"]
        ).count()

    room.occupied_beds = occupied

    # ===================================================
    # ADMIN LOCK
    # ===================================================

    if room.status != "occupied":

        if occupied == 0:

            room.status = "available"

        elif occupied < room.capacity:

            room.status = "filling"

        else:

            room.status = "full"

    room.save(update_fields=["occupied_beds", "status"])

    channel_layer = get_channel_layer()

    progress = int((room.occupied_beds / room.capacity) * 100)

    async_to_sync(channel_layer.group_send)(
    "rooms",
    {
        "type": "room_update",

        "room_type": room.__class__.__name__,

        "room_id": room.id,

        "status": room.status,

        "occupied_beds": room.occupied_beds,

        "capacity": room.capacity,

        "remaining_beds": room.capacity - room.occupied_beds,

        "progress": progress,
    }
)