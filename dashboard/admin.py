from django.contrib import admin
from .models import Folder
# Register your models here.
from .models import Booking
from .models import UploadedFile

admin.site.register(Booking)

admin.site.register(UploadedFile)
from .models import FileItem

admin.site.register(FileItem)
admin.site.register(Folder)