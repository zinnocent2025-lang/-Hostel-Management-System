from django import forms
from .models import Hostel
from .models import MaleBooking
from .models import FemaleBooking
from .models import ExternalBooking
# from core.forms import ExternalBookingForm


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'location','hostel_type', 'price',"capacity",'total_rooms', 'image', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hostel Name'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location'
            }),

            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description',
                'rows': 4
            }),
            'hostel_type': forms.Select(attrs={
            'class': 'form-control'
            }),

           'capacity': forms.NumberInput(attrs={
           'class': 'form-control',
           'placeholder': 'Maximum Occupants'
           }),

          'total_rooms': forms.NumberInput(attrs={
         'class': 'form-control',
         'placeholder': 'Number of Rooms'
        }),
        }

from django import forms
from .models import HostelAnalytics

class HostelAnalyticsForm(forms.ModelForm):
    class Meta:
        model = HostelAnalytics
        fields = ['electricity', 'water', 'maintenance',]



from django import forms

from .models import MaleBooking
from .models import FemaleBooking


class MaleBookingForm(forms.ModelForm):

    class Meta:

        model = MaleBooking

        fields = [
            "full_name",
            "gender",
            "phone",
            "emergency_phone",
            "department",
            "level",
            "duration",
            "note",
        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter full name"
            }),

            "gender": forms.Select(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "emergency_phone": forms.TextInput(attrs={
           "class": "form-control",
           "placeholder": "Emergency contact number"
            }),

            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter department"
            }),

            "level": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter level"
            }),

            "duration": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "1 Academic Session"
            }),

            "note": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Optional note",
                "rows": 4
            }),
        }


class FemaleBookingForm(forms.ModelForm):

    class Meta:

        model = FemaleBooking

        fields = [
            "full_name",
            "gender",
            "phone",
            "department",
            "level",
            "duration",
            "note",
        ]

        widgets = {

            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter full name"
            }),

            "gender": forms.Select(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),

            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter department"
            }),

            "level": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter level"
            }),

            "duration": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "1 Academic Session"
            }),

            "note": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Optional note",
                "rows": 4
            }),
        }




from django import forms
from .models import ExternalBooking


class ExternalBookingForm(forms.ModelForm):

    full_name = forms.CharField(

        widget=forms.TextInput(attrs={

            "class": "form-control",

            "readonly": True,

            "placeholder": "Full name"

        })
    )

    email = forms.EmailField(

        widget=forms.EmailInput(attrs={

            "class": "form-control",

            "readonly": True,

            "placeholder": "Email address"

        })
    )

    gender = forms.CharField(

        widget=forms.TextInput(attrs={

            "class": "form-control",

            "readonly": True,

            "placeholder": "Gender"

        })
    )

    phone = forms.CharField(

        widget=forms.TextInput(attrs={

            "class": "form-control",

            "readonly": True,

            "placeholder": "Phone number"

        })
    )

    duration = forms.CharField(

        widget=forms.TextInput(attrs={

            "class": "form-control",

            "placeholder": "Example: 1 year"

        })
    )

    class Meta:

        model = ExternalBooking

        fields = [

            "full_name",

            "email",

            "gender",

            "phone",

            "emergency_phone",

            "duration",

            "note"

        ]

        widgets = {

            "emergency_phone": forms.TextInput(attrs={

                "class": "form-control",

                "placeholder": "Emergency phone number"

            }),

            "note": forms.Textarea(attrs={

                "class": "form-control",

                "rows": 4,

                "placeholder": "Additional notes"

            }),

        }

