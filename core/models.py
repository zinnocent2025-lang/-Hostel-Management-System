from django.db import models
from django.contrib.auth.models import User


# ======================
# USER PROFILE
# ======================
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )

    image = models.ImageField(upload_to='profiles/',blank=True,null=True)

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    level = models.CharField(
        max_length=20,
        blank=True
    )

    matric_no = models.CharField(max_length=50,blank=True)
    is_online = models.BooleanField(default=False)

    last_seen = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return self.user.username

# ======================
# HOSTELS
# ======================
class Hostel(models.Model):

    HOSTEL_TYPES = [
        ("Boys Lodge", "Boys Lodge"),
        ("Girls Lodge", "Girls Lodge"),
        ("Mixed Hostel", "Mixed Hostel"),
        ("Self Contain", "Self Contain"),
        ("Single Room", "Single Room"),
        ("Shared Apartment", "Shared Apartment"),
    ]

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    image = models.ImageField(upload_to='hostels/')

    description = models.TextField(blank=True, null=True)

    hostel_type = models.CharField(
        max_length=100,
        choices=HOSTEL_TYPES,
        default="Boys Lodge"
    )

    # NEW
    capacity = models.PositiveIntegerField(
        default=0,
        help_text="Maximum number of occupants"
    )

    total_rooms = models.PositiveIntegerField(
        default=6,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ======================
# CONTACT FORM
# ======================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class HostelAnalytics(models.Model):

    # PROGRESS BARS
    electricity = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    maintenance = models.IntegerField(default=0)

    # PIE CHART
    occupied = models.IntegerField(default=65)
    available = models.IntegerField(default=25)

    # LINE GRAPH
    mon = models.IntegerField(default=20)
    tue = models.IntegerField(default=30)
    wed = models.IntegerField(default=40)
    thu = models.IntegerField(default=50)
    fri = models.IntegerField(default=60)
    sat = models.IntegerField(default=70)
    sun = models.IntegerField(default=80)

    class Meta:
        verbose_name = "Hostel Analytics"
        verbose_name_plural = "Hostel Analytics"

    def __str__(self):
        return "Hostel Analytics"
    

class MaleRoom(models.Model):

    STATUS_CHOICES = (
    ("available", "Available"),
    ("filling", "Filling"),
    ("full", "Full"),
)

    room_number = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    image = models.ImageField(upload_to="rooms/",blank=True, null=True)
    capacity = models.PositiveIntegerField(default=4)

    occupied_beds = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_number

class FemaleRoom(models.Model):

    STATUS_CHOICES = (
    ("available", "Available"),
    ("filling", "Filling"),
    ("full", "Full"),
)

    room_number = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    image = models.ImageField(upload_to="female_rooms/",blank=True,null=True)
    capacity = models.PositiveIntegerField(default=4)

    occupied_beds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.room_number


class MaleBooking(models.Model):

    STATUS_CHOICES = (("pending", "Pending"),("approved", "Approved"),("expired", "Expired"),("cancelled", "Cancelled"),)
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=20,blank=True,null=True)

    room = models.ForeignKey(
        MaleRoom,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)

    gender = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)
    emergency_phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)

    level = models.CharField(max_length=20)

    duration = models.CharField(
        max_length=50,
        default="2 years"
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):

      super().save(*args, **kwargs)

      if not self.booking_reference:

          self.booking_reference = (f"HMS-M-{self.id:05d}")

          super().save( update_fields=["booking_reference"])
    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)

        from .utils import update_room_occupancy
        update_room_occupancy(room)      

    def __str__(self):
             
        return self.full_name

    


class FemaleBooking(models.Model):

    STATUS_CHOICES = (("pending", "Pending"),("approved", "Approved"),("expired", "Expired"),("cancelled", "Cancelled"),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=20,blank=True,null=True)

    room = models.ForeignKey(FemaleRoom, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)

    gender = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)
    emergency_phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)

    level = models.CharField(max_length=20)

    duration = models.CharField(max_length=50, default="2 years")

    note = models.TextField(blank=True,null=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default="pending")

    payment_deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

       super().save(*args, **kwargs)

       if not self.booking_reference:

           self.booking_reference = (f"HMS-F-{self.id:05d}")

           super().save( update_fields=["booking_reference"])
    def delete(self, *args, **kwargs):
        room = self.room
        super().delete(*args, **kwargs)

        from .utils import update_room_occupancy
        update_room_occupancy(room)       

    def __str__(self):
      return self.full_name
    

class Message(models.Model):

    MESSAGE_TYPES = (
        ("text", "Text"),
        ("image", "Image"),
        ("file", "File"),
        ("voice", "Voice"),
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    message = models.TextField(
        blank=True,
        null=True
    )

    file = models.FileField(
        upload_to="chat_files/",
        blank=True,
        null=True
    )

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default="text"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
    




class ExternalBooking(models.Model):

    user = models.ForeignKey( User,on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=20,blank=True,null=True)


    hostel = models.ForeignKey(Hostel,on_delete=models.CASCADE,null=True,blank=True)

    room = models.ForeignKey('ExternalRoom',on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)

    email = models.EmailField()

    gender = models.CharField(max_length=20)

    phone = models.CharField(max_length=20)

    emergency_phone = models.CharField( max_length=20)

    duration = models.CharField(max_length=100)

    note = models.TextField(blank=True, null=True)

    status = models.CharField( max_length=20,  default="pending")

    payment_deadline = models.DateTimeField( null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

      super().save(*args, **kwargs)

      if not self.booking_reference:

          self.booking_reference = (f"HMS-E-{self.id:05d}")

          super().save(update_fields=["booking_reference"])

    def __str__(self):

        return self.full_name


    

class ExternalRoom(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        related_name="rooms",
        on_delete=models.CASCADE
    )

    room_number = models.CharField(max_length=20, blank=True)

    room_type = models.CharField(max_length=50)

    capacity = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, default="available")

    def save(self, *args, **kwargs):

        if not self.room_number:

           prefix = self.hostel.name[:3].upper()

           last_room = (ExternalRoom.objects .filter(hostel=self.hostel) .order_by("-id").first())

           if last_room:
               last = int(last_room.room_number[-3:])
               next_number = last + 1
           else:
               next_number = 1

           self.room_number = f"{prefix}{next_number:03d}"

        super().save(*args, **kwargs)
    
    
    
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Hostel)
def create_default_rooms(sender, instance, created, **kwargs):

    if not created:
        return

    for number in range(1, instance.total_rooms + 1):

       ExternalRoom.objects.create(hostel=instance,room_type="Shared Room", capacity=2,price=instance.price)


class SystemSettings(models.Model):
    version = models.IntegerField(default=1)

    male_booking_deadline = models.IntegerField(default=30)

    female_booking_deadline = models.IntegerField(
        default=30
    )

    external_booking_deadline = models.IntegerField(
        default=60
    )

    allow_male_booking = models.BooleanField(
        default=True
    )

    allow_female_booking = models.BooleanField(
        default=True
    )

    allow_external_booking = models.BooleanField(default=True)
    male_hostel_price = models.DecimalField( max_digits=10,decimal_places=2,default=150000)

    female_hostel_price = models.DecimalField(max_digits=10, decimal_places=2,default=150000)

    def __str__(self):
        return "System Settings"