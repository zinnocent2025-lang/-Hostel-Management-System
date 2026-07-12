from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import MaleRoom, FemaleRoom
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Profile


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):

    profile, created = Profile.objects.get_or_create(
        user=user
    )

    profile.is_online = True
    profile.save()


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):

    profile, created = Profile.objects.get_or_create(
        user=user
    )

    profile.is_online = False
    profile.last_seen = timezone.now()

    profile.save()



from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import MaleBooking, FemaleBooking
from .utils import update_room_occupancy


@receiver(post_save, sender=MaleBooking)
def male_booking_saved(sender, instance, **kwargs):
    update_room_occupancy(instance.room)


@receiver(post_delete, sender=MaleBooking)
def male_booking_deleted(sender, instance, **kwargs):
    if instance.room:
        update_room_occupancy(instance.room)


@receiver(post_save, sender=FemaleBooking)
def female_booking_saved(sender, instance, **kwargs):
    update_room_occupancy(instance.room)


@receiver(post_delete, sender=FemaleBooking)
def female_booking_deleted(sender, instance, **kwargs):
    if instance.room:
        update_room_occupancy(instance.room)


@receiver(post_save, sender=MaleRoom)
def male_room_saved(sender, instance, **kwargs):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "rooms",
        {
            "type": "room_update",
            "room_type": instance.__class__.__name__,   # <-- FIX
            "room_id": instance.id,
            "status": instance.status,
            "occupied_beds": instance.occupied_beds,
            "capacity": instance.capacity,
            "remaining_beds": instance.capacity - instance.occupied_beds,
            "progress": int(
                (instance.occupied_beds / instance.capacity) * 100
            ) if instance.capacity else 0,
        },
    )


@receiver(post_save, sender=FemaleRoom)
def female_room_saved(sender, instance, **kwargs):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "rooms",
        {
            "type": "room_update",
            "room_type": instance.__class__.__name__,   # <-- FIX
            "room_id": instance.id,
            "status": instance.status,
            "occupied_beds": instance.occupied_beds,
            "capacity": instance.capacity,
            "remaining_beds": instance.capacity - instance.occupied_beds,
            "progress": int(
                (instance.occupied_beds / instance.capacity) * 100
            ) if instance.capacity else 0,
        },
    )