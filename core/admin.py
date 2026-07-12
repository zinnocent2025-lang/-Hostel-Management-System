from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Hostel
from django.utils.html import format_html
from .models import HostelAnalytics

admin.site.site_header = "Hostel Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Welcome to HMS Dashboard"



class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price','hostel_type', 'image_preview')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    list_editable = ('price',)

    fieldsets = (
    ("Basic Info", {
        'fields': ('name', 'location')
    }),
    ("Pricing", {
        'fields': ('price',)
    }),
    ("Media", {
        'fields': ('image',)
    }),
)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"

    image_preview.short_description = "Preview"

admin.site.register(Hostel, HostelAdmin)

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
from .models import HostelAnalytics

class HostelAnalyticsAdmin(admin.ModelAdmin):

    fieldsets = (

        ("Progress Bars", {
            "fields": (
                "electricity",
                "water",
                "maintenance"
            )
        }),

        ("Pie Chart", {
            "fields": (
                "occupied",
                "available"
            )
        }),

        ("Line Graph", {
            "fields": (
                "mon",
                "tue",
                "wed",
                "thu",
                "fri",
                "sat",
                "sun"
            )
        }),

    )

    def has_add_permission(self, request):

        # Prevent multiple rows
        if HostelAnalytics.objects.exists():
            return False

        return True


admin.site.register(
    HostelAnalytics,
    HostelAnalyticsAdmin
)
from .models import MaleRoom

admin.site.register(MaleRoom)

from .models import FemaleRoom

admin.site.register(FemaleRoom)

from .models import MaleBooking
from .models import FemaleBooking

admin.site.register(MaleBooking)
admin.site.register(FemaleBooking)
from .models import ExternalRoom, ExternalBooking
admin.site.register(ExternalRoom)
admin.site.register(ExternalBooking)