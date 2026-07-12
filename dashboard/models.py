from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student_name = models.CharField(max_length=100)
    room = models.CharField(max_length=50)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.student_name
    

    def __str__(self):
        return self.user.username

class PermissionModel(models.Model):
    class Meta:
        permissions = [
            ("can_manage_bookings", "Can manage bookings"),
            ("can_view_users", "Can view users"),
            ("can_delete_users", "Can delete users"),
        ]    


from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=20)  # image, document
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.file.name

from django.db import models

class FileItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='files'
    )

    folder = models.ForeignKey(
        'Folder',
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to='file_manager/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.file.name
class Folder(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='folders'
    )

    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name