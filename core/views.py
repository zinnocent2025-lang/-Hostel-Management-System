from django.shortcuts import render
from .models import Hostel
from django.core.paginator import Paginator
from django.http import JsonResponse
from core.models import HostelAnalytics
from django.contrib.auth.decorators import login_required
from .models import FemaleRoom
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from datetime import timedelta
from django.utils import timezone

from .models import MaleBooking
from .models import FemaleBooking

from .forms import MaleBookingForm
from .forms import FemaleBookingForm
from .models import Profile
from .forms import ExternalBookingForm
from .models import ExternalBooking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import (  MaleBooking,FemaleBooking,ExternalBooking,ExternalRoom, SystemSettings)
from .models import SystemSettings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'index.html')  # your HTML file name
# def contact(request):
#     return render(request, 'contact.html')  # your HTML file name
from .models import MaleRoom

from django.contrib.auth.models import AnonymousUser

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout

from django.db.models import F

def bump_system_version():

    settings, _ = SystemSettings.objects.get_or_create(
        id=1
    )

    settings.version += 1

    settings.save()

def male(request):

    user_exists = False

    if request.user.is_authenticated:

        user_exists = User.objects.filter(
            id=request.user.id
        ).exists()

        if not user_exists:

            logout(request)

    from core.utils import update_room_occupancy

    male_rooms = MaleRoom.objects.all()

    for room in male_rooms:
         update_room_occupancy(room)

         room.remaining_beds = room.capacity - room.occupied_beds
         room.progress = int((room.occupied_beds / room.capacity) * 100) if room.capacity else 0
    settings, _ = SystemSettings.objects.get_or_create(id=1)
    for room in male_rooms:

         room.remaining_beds = room.capacity - room.occupied_beds

         room.progress = int((room.occupied_beds / room.capacity) * 100) if room.capacity else 0

    return render(
        request,
        'male-hostel.html',
        {
            'male_rooms': male_rooms,
            'user_exists': user_exists,
             "settings": settings,
        }
    )
def female(request):

    if request.user.is_authenticated:

        exists = User.objects.filter(
            id=request.user.id
        ).exists()

        if not exists:

            request.session.flush()

            request.user = AnonymousUser()

    female_rooms = FemaleRoom.objects.all()
    from core.utils import update_room_occupancy

    for room in female_rooms:

          update_room_occupancy(room)

          room.remaining_beds = (room.capacity - room.occupied_beds)

          room.progress = (int((room.occupied_beds / room.capacity) * 100)if room.capacity else 0)
    settings, _ = SystemSettings.objects.get_or_create(id=1)

    return render(
        request,
        "female-hostel.html",
        {
            "female_rooms": female_rooms,
            "settings": settings,
        }
    )
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from .models import ExternalBooking

from django.utils import timezone

def hostel_list(request):

    hostels = Hostel.objects.all().order_by("-id")

    booking_status = ""
    booked_room_id = ""

    if request.user.is_authenticated:

        latest_booking = (
            ExternalBooking.objects.filter(
                user=request.user
            )
            .order_by("-created_at")
            .first()
        )

        if latest_booking:

            # =========================
            # AUTO EXPIRE BOOKING
            # =========================

            if (
                latest_booking.status == "pending"
                and
                latest_booking.payment_deadline
                and
                latest_booking.payment_deadline < timezone.now()
            ):

                latest_booking.status = "expired"
                latest_booking.save()

                # FREE THE ROOM
                latest_booking.room.status = "available"
                latest_booking.room.save()

            # Refresh from database
            latest_booking.refresh_from_db()

            booking_status = latest_booking.status
            booked_room_id = latest_booking.room.id

            print("STATUS =", booking_status)
            print("ROOM =", booked_room_id)

    return render(
        request,
        "hostels.html",
        {
            "hostels": hostels[:6],
            "booking_status": booking_status,
            "booked_room_id": booked_room_id,
        }
    )

def load_more_hostels(request):

    page = int(request.GET.get('page', 1))

    per_page = 6

    start = (page - 1) * per_page

    end = start + per_page

    hostels = Hostel.objects.all().order_by("-id")[start:end]

    data = []

    for hostel in hostels:

        rooms = []

        for room in hostel.rooms.all():

            rooms.append({
                "id": room.id,
                "number": room.room_number,
                "type": room.room_type,
                "capacity": room.capacity,
                "price": str(room.price),
                "status": room.status,
            })

        data.append({

            "name": hostel.name,

            "location": hostel.location,

            "price": str(hostel.price),

            "image": hostel.image.url if hostel.image else "",

            "hostel_type": hostel.hostel_type,

            "rooms": rooms,
        })

    total_hostels = Hostel.objects.count()

    return JsonResponse({

        "hostels": data,

        "has_next": end < total_hostels

    })



def register(request):
    next_url = request.POST.get("next") or request.GET.get("next") or "/student_dashboard/"

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return JsonResponse({
                "success": False,
                "message": "Passwords do not match"
            })

        if User.objects.filter(username=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Email already exists"
            })

        user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=full_name
        )

        # SAVE PROFILE DATA
        profile = user.user_profile

        profile.gender = gender
        profile.phone = phone

        profile.save()

        user.user_profile.gender = gender
        user.user_profile.phone = phone
        user.user_profile.save()

        # Profile.objects.create(
        #     user=user,
        #     gender=gender,
        #     phone=phone
        # )

        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return JsonResponse({
            "success": True,
            "redirect_url": next_url
        })
   
    return render(request, "register.html", {"next": next_url})



def check_email(request):
    email = request.GET.get("email")

    exists = User.objects.filter(username=email).exists()

    return JsonResponse({
        "exists": exists
    })




def contact(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        #  Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message,
        )

        # ✅ Email content
        subject = "New Contact Message"
        full_message = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        try:
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except Exception as e:
            print("Email error:", e)

        #  THIS WAS MISSING
        return JsonResponse({"success": True})

    #  for GET request
    return render(request, "contact.html")

from django.shortcuts import render
from .models import HostelAnalytics

def student_dashboard(request):
    

    analytics = HostelAnalytics.objects.first()

    context = {
        "analytics": analytics
    }

    return render(request, "dashboard/student_dashboard.html", context)

from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        remember_me = request.POST.get("remember_me")

        if not email or not password:

            return render(request, "login.html", {
                "error": "Please fill all fields"
            })

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)
            user.user_profile.is_online = True
            user.user_profile.save()

          # Remember Me
            if remember_me:
                 request.session.set_expiry(1209600)
            else:
               request.session.set_expiry(0)

            request.session["mode"] = "student"

            return redirect("student_dashboard")

        else:

            return render(request, "login.html", {
                "error": "Invalid email or password"
            })

    return render(request, "login.html")


from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        print(email)
        print(password)

        try:

            # Find user using email
            user_obj = User.objects.get(email=email)

            # Authenticate using actual username
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            print(user)

            if user is not None and user.is_staff:

                login(request, user)

                request.session["mode"] = "admin"

                return redirect("dashboard_home")

            else:

                messages.error(
                    request,
                    "Invalid admin credentials"
                )

        except User.DoesNotExist:

            messages.error(
                request,
                "Admin account not found"
            )

    return render(
        request,
        "admin_login.html"
    )
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

def logout_view(request):

    is_admin = False

    if request.user.is_authenticated:

        is_admin = request.user.is_staff

        try:

            profile = request.user.user_profile

            profile.is_online = False

            profile.last_seen = timezone.now()

            profile.save()

        except:
            pass

    logout(request)

    # =========================
    # REDIRECT BASED ON USER TYPE
    # =========================

    if is_admin:

        return redirect("admin_login")

    return redirect("login")

from .forms import HostelForm


from django.shortcuts import render, redirect
from core.models import Hostel

from django.shortcuts import render, redirect
from .models import Hostel
from .forms import HostelForm

def add_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')   # only after saving
    else:
        form = HostelForm()

    return render(request, 'dashboard/add_hostel.html', {'form': form})


from core.models import Hostel

def hostels(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostels.html', {'hostels': hostels})

from .forms import HostelAnalyticsForm
from .models import HostelAnalytics

def analytics_dashboard(request):

    analytics, created = HostelAnalytics.objects.get_or_create(pk=1)

    if request.method == "POST":

        form = HostelAnalyticsForm(
            request.POST,
            instance=analytics
        )

        if form.is_valid():
            form.save()

    else:

        form = HostelAnalyticsForm(
            instance=analytics
        )

    return render(
        request,
        "dashboard/analytics.html",
        {
            "form": form,
            "analytics": analytics
        }
    )


@login_required
def male_room_booking(request, room_id):
    settings = SystemSettings.objects.first()

    if not settings.allow_male_booking:

       return HttpResponse("Male hostel booking is currently disabled.")

    room = MaleRoom.objects.get(id=room_id)
    current_bookings = MaleBooking.objects.filter(room=room,status__in=["pending", "approved"]).select_related("user")

    try:
        profile = request.user.user_profile

    except:
        return redirect("register")

    # BLOCK FEMALE USERS
    if profile.gender.lower() != "male":

        return redirect("female-hostel")

    # =========================
    # CHECK ALL ACTIVE BOOKINGS
    # =========================

    has_booking = (

        MaleBooking.objects.filter(
            user=request.user,
            status__in=["pending", "approved"]
        ).exists()

        or

        FemaleBooking.objects.filter(
            user=request.user,
            status__in=["pending", "approved"]
        ).exists()

        or

        ExternalBooking.objects.filter(
            user=request.user,
            status__in=["pending", "approved"]
        ).exists()

    )

    if has_booking:

        return redirect("student_dashboard")


    # STOP IF ROOM IS FULL

    if room.status in ["occupied", "full"]:

        return redirect("male-hostel")

    # =========================
    # SAVE BOOKING
    # =========================

    if request.method == "POST":

        form = MaleBookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.user = request.user

            booking.room = room

            system_settings, created = (SystemSettings.objects.get_or_create(id=1))

            booking.payment_deadline = (timezone.now() +timedelta(minutes=system_settings.male_booking_deadline))

            booking.save()

            from core.utils import update_room_occupancy

            update_room_occupancy(room)
            bump_system_version()

            return redirect("student_dashboard")

        else:

            print(form.errors)

    else:

        form = MaleBookingForm(
            initial={
                "full_name": request.user.first_name,
                "phone": request.user.user_profile.phone
            }
        )

    return render(
        request,
        "booking/male_booking.html",
        {
            "form": form,
            "room": room,
            "current_bookings": current_bookings,
        }
    )

@login_required
def female_room_booking(request, room_id):
    settings = SystemSettings.objects.first()

    if not settings.allow_female_booking:

         return HttpResponse("Female hostel booking is currently disabled.")

    room = FemaleRoom.objects.get(id=room_id)
    current_bookings = FemaleBooking.objects.filter(room=room, status__in=["pending", "approved"]).select_related("user")

    try:
        profile = request.user.user_profile

    except:
        return redirect("register")

    # BLOCK MALE USERS
    if profile.gender.lower() != "female":

        return redirect("male-hostel")

    # =========================
    # CHECK ALL ACTIVE BOOKINGS
    # =========================

    male_booking = MaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    female_booking = FemaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    external_booking = ExternalBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    # =========================
    # BLOCK IF USER ALREADY HAS
    # ANY ACTIVE BOOKING
    # =========================

    if male_booking:

        return redirect("student_dashboard")

    if external_booking:

        return redirect("student_dashboard")

    # =========================
    # HANDLE FEMALE BOOKING
    # =========================

    if female_booking:

        # EXPIRED
        if female_booking.payment_deadline < timezone.now():

            update_room_occupancy(female_booking.room)

            if female_booking.room.id != room.id:

                return redirect("student_dashboard")

            female_booking.delete()

        else:

            return redirect("student_dashboard")

    # =========================
    # ROOM OCCUPIED
    # =========================

    if room.status in ["occupied", "full"]:

        return redirect("female-hostel")

    # =========================
    # CREATE BOOKING
    # =========================

    if request.method == "POST":

        form = FemaleBookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.user = request.user

            booking.room = room

            system_settings, created = (SystemSettings.objects.get_or_create(id=1))

            booking.payment_deadline = (timezone.now() +timedelta(minutes=system_settings.female_booking_deadline))

            booking.save()

            from core.utils import update_room_occupancy

            update_room_occupancy(room)
            bump_system_version()
            return redirect("student_dashboard")

        else:

            print(form.errors)

    else:

        form = FemaleBookingForm(
            initial={
                "full_name":
                request.user.first_name,

                "phone":
                request.user.user_profile.phone
            }
        )

    return render(
        request,
        "booking/female_booking.html",
        {
            "form": form,
            "room": room,
            "current_bookings": current_bookings,
        }
    )

from .forms import ExternalBookingForm
from .models import ExternalRoom
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def external_booking(request, room_id):
    settings = SystemSettings.objects.first()

    if not settings.allow_external_booking:

         return HttpResponse("External hostel booking is currently disabled.")

    room = get_object_or_404(
        ExternalRoom,
        id=room_id
    )

    profile = request.user.user_profile

    # =========================
    # GET LATEST BOOKING
    # =========================

    latest_booking = (
        ExternalBooking.objects
        .filter(user=request.user)
        .order_by("-created_at")
        .first()
    )

    is_rebooking = False

    if latest_booking:

        # =========================
        # ACTIVE BOOKING
        # =========================

        if latest_booking.status in [
            "pending",
            "approved"
        ]:
            return redirect(
                "student_dashboard"
            )

        # =========================
        # EXPIRED BOOKING
        # =========================

        elif latest_booking.status == "expired":

            # User can only rebook same room
            if latest_booking.room.id != room.id:
                return redirect(
                    "hostels"
                )

            is_rebooking = True

            # Release room if still occupied
            if room.status == "occupied":
                room.status = "available"
                room.save()

        # =========================
        # REJECTED / CANCELLED
        # =========================

        elif latest_booking.status in [
            "rejected",
            "cancelled"
        ]:
            pass

    # =========================
    # BLOCK SCHOOL BOOKINGS
    # =========================

    has_school_booking = (

        MaleBooking.objects.filter(
            user=request.user,
            status__in=[
                "pending",
                "approved"
            ]
        ).exists()

        or

        FemaleBooking.objects.filter(
            user=request.user,
            status__in=[
                "pending",
                "approved"
            ]
        ).exists()

    )

    if has_school_booking:
        return redirect(
            "student_dashboard"
        )

    # =========================
    # BLOCK OCCUPIED ROOM
    # =========================

    if (
        room.status == "occupied"
        and not is_rebooking
    ):
        return redirect(
            "hostels"
        )

    # =========================
    # CREATE BOOKING
    # =========================

    if request.method == "POST":

        form = ExternalBookingForm(
            request.POST
        )

        if form.is_valid():

            # Delete old expired booking
            if is_rebooking:
                latest_booking.delete()

            booking = form.save(
                commit=False
            )

            booking.user = request.user
            booking.room = room
            booking.hostel = room.hostel

            booking.status = "pending"

            system_settings, created = (SystemSettings.objects.get_or_create(id=1))

            booking.payment_deadline = (timezone.now()+ timedelta(minutes=system_settings.external_booking_deadline))

            booking.save()
            bump_system_version()

            room.status = "occupied"
            room.save()

            return redirect(
                "student_dashboard"
            )

    else:

        form = ExternalBookingForm(
            initial={
                "full_name":
                request.user.first_name,

                "email":
                request.user.email,

                "gender":
                profile.gender,

                "phone":
                profile.phone,
            }
        )

    context = {
        "form": form,
        "hostel": room.hostel,
        "room": room,
        "is_rebooking": is_rebooking,
    }

    return render(
        request,
        "external_booking.html",
        context
    )
def user_has_active_booking(user):

    return (

        MaleBooking.objects.filter(
            user=user,
            status__in=["pending", "approved"]
        ).exists()

        or

        FemaleBooking.objects.filter(
            user=user,
            status__in=["pending", "approved"]
        ).exists()

        or

        ExternalBooking.objects.filter(
            user=user,
            status__in=["pending", "approved"]
        ).exists()

    )

from django.http import JsonResponse
from core.models import SystemSettings


def system_version(request):

    settings, _ = SystemSettings.objects.get_or_create(
        id=1
    )

    return JsonResponse({

        "version": settings.version

    })


from django.contrib.auth.decorators import login_required
from .models import SystemSettings

@login_required
def demo_payment(request):

    settings, _ = SystemSettings.objects.get_or_create(id=1)

    context = {
        "amount": settings.male_hostel_price,
    }

    return render(
        request,
        "payment/demo_payment.html",
        context
    )