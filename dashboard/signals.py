from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import (
    MaleBooking,
    FemaleBooking,
    ExternalBooking,
    MaleRoom,
    FemaleRoom,
    Hostel,
    Message,
    HostelAnalytics,
    SystemSettings,
    Profile
)

from core.utils import bump_system_version


@receiver(post_save, sender=MaleBooking)
@receiver(post_delete, sender=MaleBooking)
@receiver(post_save, sender=FemaleBooking)
@receiver(post_delete, sender=FemaleBooking)
@receiver(post_save, sender=ExternalBooking)
@receiver(post_delete, sender=ExternalBooking)
@receiver(post_save, sender=MaleRoom)
@receiver(post_delete, sender=MaleRoom)
@receiver(post_save, sender=FemaleRoom)
@receiver(post_delete, sender=FemaleRoom)
@receiver(post_save, sender=Hostel)
@receiver(post_delete, sender=Hostel)
@receiver(post_save, sender=Message)
@receiver(post_delete, sender=Message)
@receiver(post_save, sender=HostelAnalytics)
@receiver(post_save, sender=Profile)
def refresh_system(sender, **kwargs):

    bump_system_version()

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models import Hostel, ExternalRoom


@receiver(post_save, sender=ExternalRoom)
@receiver(post_delete, sender=ExternalRoom)
def update_hostel_room_count(sender, instance, **kwargs):

    hostel = instance.hostel

    hostel.total_rooms = hostel.rooms.count()

    hostel.save(update_fields=["total_rooms"])