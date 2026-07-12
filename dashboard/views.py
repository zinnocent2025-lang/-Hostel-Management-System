from django.shortcuts import render
from .models import Booking
from django.contrib.auth.models import User
from django.shortcuts import redirect
from core.models import Profile
from django.db.models import Q
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User, Permission
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from .models import FileItem
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, time
from core.models import Hostel
from core.forms import HostelForm
from django.shortcuts import render, redirect, get_object_or_404
from core.models import MaleRoom, FemaleRoom
from core.models import MaleBooking, FemaleBooking
from core.models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from core.models import ExternalBooking
from core.forms import ( HostelForm,ExternalBookingForm,)
from core.models import ExternalRoom
from core.models import SystemSettings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .decorators import admin_required, student_required
from core.utils import (bump_system_version,update_room_occupancy,)
from core.models import MaleRoom, FemaleRoom, ExternalRoom


@admin_required
def bookings(request):

    if not request.user.is_staff:
        return HttpResponse("Access Denied")

    male_bookings = MaleBooking.objects.select_related("room").order_by("-created_at")

    female_bookings = FemaleBooking.objects.select_related("room").order_by("-created_at")

    external_bookings = ExternalBooking.objects.select_related( "room","hostel").order_by("-created_at")

    
    # =====================
    # SORT NEWEST FIRST
    # =====================

    # all_bookings.sort(
    #     key=lambda x: x["created_at"],
    #     reverse=True
    # )

    # =====================
    # STATISTICS
    # ===================

    total_bookings = (
    male_bookings.count()
    + female_bookings.count()
    + external_bookings.count()
    )
    pending_count = (
    male_bookings.filter(status="pending").count()
    + female_bookings.filter(status="pending").count()
    + external_bookings.filter(status="pending").count()
    )

    approved_count = (
    male_bookings.filter(status="approved").count()
    + female_bookings.filter(status="approved").count()
    + external_bookings.filter(status="approved").count()
    )

    expired_count = (
    male_bookings.filter(status="expired").count()
    + female_bookings.filter(status="expired").count()
    + external_bookings.filter(status="expired").count()
    )

    cancelled_count = (
    male_bookings.filter(status="cancelled").count()
    + female_bookings.filter(status="cancelled").count()
    + external_bookings.filter(status="cancelled").count()
    )

    return render(
    request,
    "dashboard/bookings.html",
    {
        "male_bookings": male_bookings,
        "female_bookings": female_bookings,
        "external_bookings": external_bookings,

        "total_bookings": total_bookings,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "expired_count": expired_count,
        "cancelled_count": cancelled_count,
    }
   )


@admin_required
def users(request):

    if not request.user.is_staff:
        return HttpResponse("Access Denied")

    users = User.objects.select_related(
        "user_profile"
    ).all()

    return render(
        request,
        "dashboard/users.html",
        {
            "users": users
        }
    )


@csrf_exempt
@admin_required
def update_booking(request, id):

    if request.method != "POST":

        return JsonResponse({
            "success": False
        })

    data = json.loads(request.body)

    status = data.get("status")
    booking_type = data.get("booking_type")

    # =========================
    # GET BOOKING
    # =========================

    if booking_type == "male":

        booking = MaleBooking.objects.get(id=id)

    elif booking_type == "female":

        booking = FemaleBooking.objects.get(id=id)

    elif booking_type == "external":

        booking = ExternalBooking.objects.get(id=id)

    else:

        return JsonResponse({
            "success": False
        })

    # =========================
    # UPDATE STATUS
    # =========================

    booking.status = status

    booking.save()

    # =========================
    # UPDATE ROOM
    # =========================

    if booking_type in ["male", "female"]:

        update_room_occupancy(booking.room)

    else:

        if status in ["approved", "pending"]:

            booking.room.status = "occupied"

        elif status in [

            "expired",
            "cancelled",
            "rejected"

        ]:

            booking.room.status = "available"

        booking.room.save()

    # =========================
    # BUMP SYSTEM VERSION
    # =========================

    bump_system_version()

    return JsonResponse({

        "success": True

    })


def add_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_staff = 'is_staff' in request.POST

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = is_staff
        user.save()

    return redirect('/dashboard/users/')


@admin_required
def get_user(request, user_id):

    try:

        user = User.objects.get(id=user_id)

        profile, created = Profile.objects.get_or_create(
            user=user
        )

        # ==========================
        # GET ALL BOOKINGS
        # ==========================

        bookings = []

        male_booking = (
            MaleBooking.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        female_booking = (
            FemaleBooking.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        external_booking = (
            ExternalBooking.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if male_booking:
            bookings.append(male_booking)

        if female_booking:
            bookings.append(female_booking)

        if external_booking:
            bookings.append(external_booking)

        latest_booking = None

        if bookings:
            latest_booking = max(
                bookings,
                key=lambda b: b.created_at
            )

        # ==========================
        # USER FULL NAME
        # ==========================

        if (
            user.first_name
            or
            user.last_name
        ):

            full_name = (
                f"{user.first_name} "
                f"{user.last_name}"
            ).strip()

        elif (
            latest_booking
            and
            hasattr(latest_booking, "full_name")
        ):

            full_name = latest_booking.full_name

        else:

            full_name = user.username

        # ==========================
        # PROFILE FALLBACKS
        # ==========================

        phone = profile.phone
        department = profile.department
        level = profile.level
        gender = profile.gender
        matric_no = profile.matric_no

        if latest_booking:

            if not phone and hasattr(latest_booking, "phone"):
                phone = latest_booking.phone

            if (
                not department
                and
                hasattr(latest_booking, "department")
            ):
                department = latest_booking.department

            if (
                not level
                and
                hasattr(latest_booking, "level")
            ):
                level = latest_booking.level

            if (
                not gender
                and
                hasattr(latest_booking, "gender")
            ):
                gender = latest_booking.gender

        # ==========================
        # HOSTEL INFORMATION
        # ==========================

        current_hostel = "No Hostel"
        current_room = "N/A"
        booking_status = "No Booking"
        hostel_type = "None"

        if latest_booking:

            booking_status = latest_booking.status

            if isinstance(
                latest_booking,
                MaleBooking
            ):

                current_hostel = "Male Hostel"

                current_room = (
                    latest_booking.room.room_number
                )

                hostel_type = "School Hostel"

            elif isinstance(
                latest_booking,
                FemaleBooking
            ):

                current_hostel = "Female Hostel"

                current_room = (
                    latest_booking.room.room_number
                )

                hostel_type = "School Hostel"

            elif isinstance(
                latest_booking,
                ExternalBooking
            ):

                current_hostel = (
                    latest_booking.hostel.name
                )

                current_room = (
                    latest_booking.room.room_number
                )

                hostel_type = "External Hostel"

        # ==========================
        # BOOKING STATS
        # ==========================

        male_count = (
            MaleBooking.objects
            .filter(user=user)
            .count()
        )

        female_count = (
            FemaleBooking.objects
            .filter(user=user)
            .count()
        )

        external_count = (
            ExternalBooking.objects
            .filter(user=user)
            .count()
        )

        booking_count = (
            male_count
            + female_count
            + external_count
        )

        # ==========================
        # RESPONSE
        # ==========================

        data = {

            "id": user.id,

            "username": user.username,

            "full_name": full_name,

            "email": user.email,

            "is_staff": user.is_staff,

            "is_active": user.is_active,

            "online": profile.is_online,

            "date_joined": user.date_joined.strftime(
                "%Y-%m-%d"
            ),

            "last_login": (
                user.last_login.strftime(
                    "%Y-%m-%d %H:%M"
                )
                if user.last_login
                else "Never"
            ),

            "image": (
                profile.image.url
                if profile.image
                else ""
            ),

            "phone": (
                phone
                if phone
                else "Not Available"
            ),

            "department": (
                department
                if department
                else "Not Available"
            ),

            "level": (
                level
                if level
                else "Not Available"
            ),

            "gender": (
                gender
                if gender
                else "Not Available"
            ),

            "matric_no": (
                matric_no
                if matric_no
                else "Not Available"
            ),

            "hostel": current_hostel,

            "hostel_type": hostel_type,

            "room": current_room,

            "booking_status": booking_status,

            "booking_count": booking_count,
        }

        return JsonResponse(data)

    except User.DoesNotExist:

        return JsonResponse({
            "success": False,
            "error": "User not found"
        })




from django.db.models import Q
@admin_required
def search_users(request):

    query = request.GET.get("q", "").strip()

    if not query:

        return JsonResponse({
            "users": []
        })

    users = User.objects.filter(

        Q(username__icontains=query) |
        Q(email__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(user_profile__phone__icontains=query) |
        Q(user_profile__department__icontains=query) |
        Q(user_profile__matric_no__icontains=query)

    ).distinct()

    data = []

    for user in users:

        profile, _ = Profile.objects.get_or_create(
            user=user
        )

        data.append({

            "id": user.id,

            "username": user.username,

            "full_name": (
                f"{user.first_name} {user.last_name}".strip()
                or user.username
            ),

            "email": user.email,

            "image": (
                profile.image.url
                if profile.image
                else ""
            ),

            "phone": profile.phone,

            "department": profile.department,

            "matric_no": profile.matric_no,

            "is_active": user.is_active,

            "is_staff": user.is_staff,
        })

    return JsonResponse({
        "users": data
    })

import csv
from .models import User
@admin_required
def export_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Active', 'Staff'])

    users = User.objects.all()

    for user in users:
        writer.writerow([
            user.username,
            user.email,
            user.is_active,
            user.is_staff
        ])

    return response



from django.contrib.auth.models import Group

def groups_page(request):
    groups = Group.objects.all()

    group_data = []

    for group in groups:
        permissions = group.permissions.values_list("codename", flat=True)

        group_data.append({
            "id": group.id,
            "name": group.name,
            "users_count": group.user_set.count(),
            "permissions": list(permissions)
        })

    return render(request, "dashboard/groups.html", {
        "groups": group_data
    })
@admin_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("group_name")

        if name:
            Group.objects.create(name=name)

    return redirect("groups")

from django.contrib.auth.models import Group, User
@admin_required
def group_users(request, group_id):
    group = Group.objects.get(id=group_id)

    users = User.objects.all()
    group_users = group.user_set.all()

    return render(request, "dashboard/group_users.html", {
        "group": group,
        "users": users,
        "group_users": group_users
    })


@admin_required
def get_group_users(request, group_id):
    group = Group.objects.get(id=group_id)
    users = User.objects.all()

    data = []

    for user in users:
        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "in_group": user in group.user_set.all()
        })

    return JsonResponse({"users": data})

from django.contrib.auth.models import Group, Permission

def setup_groups():
    admin, _ = Group.objects.get_or_create(name="Admin")
    staff, _ = Group.objects.get_or_create(name="Staff")
    student, _ = Group.objects.get_or_create(name="Student")

    permissions = Permission.objects.all()

    # Admin → all permissions
    admin.permissions.set(permissions)

    # Staff → limited
    staff.permissions.set(
        Permission.objects.filter(codename__in=[
            "can_manage_bookings",
            "can_view_users"
        ])
    )

    # Student → minimal
    student.permissions.set(
        Permission.objects.filter(codename__in=[
            "can_view_users"
        ])
    )
from django.contrib.auth.models import Group, Permission

def setup_groups_permissions():
    
    # Get or create groups
    admin, _ = Group.objects.get_or_create(name="Admin")
    staff, _ = Group.objects.get_or_create(name="Staff")
    student, _ = Group.objects.get_or_create(name="Student")

    # Get permissions
    manage_bookings = Permission.objects.get(codename="can_manage_bookings")
    view_users = Permission.objects.get(codename="can_view_users")
    delete_users = Permission.objects.get(codename="can_delete_users")

    # Assign permissions

    # Admin → all
    admin.permissions.set(Permission.objects.all())

    # Staff → limited
    staff.permissions.set([
        manage_bookings,
        view_users
    ])

    # Student → minimal
    student.permissions.set([
        view_users
    ])

    print("Permissions assigned successfully!")

def has_permission(user, perm):
    return user.is_superuser or user.has_perm(perm)


def delete_user(request, user_id):

    # 🔒 CHECK PERMISSION
    if not (request.user.is_superuser or request.user.has_perm("dashboard.can_delete_users")):
        return JsonResponse({"error": "Permission denied"})

    user = User.objects.get(id=user_id)
    user.delete()

    return JsonResponse({"success": True})
def users_page(request):

    if not has_permission(request.user, "dashboard.can_view_users"):
        return redirect("no_access")

    users = User.objects.all()

    return render(request, "dashboard/users.html", {"users": users})

def bookings_page(request):

    if not has_permission(request.user, "dashboard.can_manage_bookings"):
        return redirect("no_access")

    return render(request, "dashboard/bookings.html")

def no_access(request):
    return render(request, "dashboard/no_access.html")



def create_booking(request):

    #  PERMISSION CHECK
    if not (request.user.is_superuser or request.user.has_perm("dashboard.can_book_room")):
        return JsonResponse({"error": "Permission denied"})

    # continue your booking logic
    return JsonResponse({"success": True})

@admin_required
def get_group_data(request, group_id):
    group = Group.objects.get(id=group_id)

    users = User.objects.all()
    group_users = group.user_set.all()
    permissions = Permission.objects.filter(codename__startswith="can_")

    return JsonResponse({
        "group_name": group.name,
        "is_admin": group.name == "Admin",
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "in_group": u in group_users
            } for u in users
        ],
        "permissions": [
            {
                "id": p.id,
                "name": p.name,
                "codename": p.codename,
                "enabled": p in group.permissions.all()
            } for p in permissions
        ]
    })
@admin_required
def update_group_user(request):

    user_id = request.GET.get("user_id")
    group_id = request.GET.get("group_id")
    action = request.GET.get("action")

    print("DEBUG:", user_id, group_id, action)  # 👈 VERY IMPORTANT

    if not user_id or not group_id or not action:
        return JsonResponse({"error": "Missing data"})

    try:
        user = User.objects.get(id=int(user_id))
        group = Group.objects.get(id=int(group_id))
    except:
        return JsonResponse({"error": "Invalid user or group"})

    if action == "add":
        user.groups.add(group)
    elif action == "remove":
        user.groups.remove(group)

    user.save()  # 👈 IMPORTANT

    return JsonResponse({"success": True})
@admin_required
def toggle_permission(request):

    group_id = request.GET.get("group_id")
    perm_id = request.GET.get("perm_id")

    if not group_id or not perm_id:
        return JsonResponse({"error": "Missing data"})

    group = Group.objects.get(id=group_id)
    permission = Permission.objects.get(id=perm_id)

    if permission in group.permissions.all():
        group.permissions.remove(permission)
    else:
        group.permissions.add(permission)

    return JsonResponse({"success": True})
@admin_required
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)

    if group.name == "Admin":
        return JsonResponse({"error": "Cannot delete Admin group"})

    group.delete()
    return JsonResponse({"success": True})


from django.contrib.auth.models import User
from core.models import Profile

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def update_profile(request):
    if request.method == "POST":

        user = request.user
        profile = user.user_profile

        email = request.POST.get("email")
        phone = request.POST.get("phone")
        department = request.POST.get("department")
        level = request.POST.get("level")
        matric_no = request.POST.get("matric_no")
        image = request.FILES.get("image")

        if email:
            user.email = email
            user.save()

        if phone is not None:
            profile.phone = phone

        if department is not None:
            profile.department = department

        if level is not None:
            profile.level = level

        if matric_no is not None:
            profile.matric_no = matric_no

        if image:
            profile.image = image

        profile.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):

        image = request.FILES["image"]

        fs = FileSystemStorage(location='media/uploads/')
        filename = fs.save(image.name, image)

        return JsonResponse({
            "success": True,
            "file_url": fs.url(filename)
        })

    return JsonResponse({"error": "No image"})



@student_required
def student_dashboard(request):
    expire_bookings()

    if not request.user.is_active:
        return HttpResponse(
            "Your account has been suspended."
        )

    if request.user.is_staff:
        return redirect("dashboard_home")

    analytics = HostelAnalytics.objects.first()

    booking = None
    current_room = None
    current_hostel = "No Hostel"
    booking_status = "No Active Booking"
    countdown = 0
    deadline = ""

    # =========================
    # ADMIN CHAT
    # =========================

    admin_user = User.objects.filter(
        is_staff=True
    ).first()

    if request.method == "POST" and admin_user:

        text = request.POST.get("message")
        uploaded_file = request.FILES.get("file")

        message_type = "text"

        if uploaded_file:

            content_type = uploaded_file.content_type

            if content_type.startswith("image"):
                message_type = "image"

            elif content_type.startswith("audio"):
                message_type = "voice"

            else:
                message_type = "file"

        if text or uploaded_file:

            Message.objects.create(
                sender=request.user,
                receiver=admin_user,
                message=text,
                file=uploaded_file,
                message_type=message_type
            )

        return redirect("student_dashboard")

    # =========================
    # ACTIVE BOOKINGS
    # =========================

    male_booking = MaleBooking.objects.filter(user=request.user,status__in=["pending", "approved"]).order_by("-created_at").first()

    female_booking = FemaleBooking.objects.filter(user=request.user,status__in=["pending", "approved"]).order_by("-created_at").first()

    external_booking = ExternalBooking.objects.filter(user=request.user,status__in=["pending", "approved"]).order_by("-created_at").first()

    # =========================
    # EXPIRE MALE BOOKING
    # =========================

    if (male_booking and male_booking.status == "pending" and male_booking.payment_deadline and male_booking.payment_deadline < timezone.now() ):

        update_room_occupancy(male_booking.room)

        male_booking.status = "expired"
        male_booking.save()

        male_booking = None

    # =========================
    # EXPIRE FEMALE BOOKING
    # =========================

    if (
    female_booking and
    female_booking.status == "pending" and
    female_booking.payment_deadline and
    female_booking.payment_deadline < timezone.now()
    ):

        update_room_occupancy(male_booking.room)

        female_booking.status = "expired"
        female_booking.save()

        female_booking = None

    # =========================
    # EXPIRE EXTERNAL BOOKING
    # =========================

    if ( external_booking and external_booking.status == "pending" and external_booking.payment_deadline and external_booking.payment_deadline < timezone.now() ):

        external_booking.room.status = "available"
        external_booking.room.save()

        external_booking.status = "expired"
        external_booking.save()

        external_booking = None

    # =========================
    # COMBINE BOOKINGS
    # =========================

    all_bookings = []

    if male_booking:
        all_bookings.append(male_booking)

    if female_booking:
        all_bookings.append(female_booking)

    if external_booking:
        all_bookings.append(external_booking)

    # =========================
    # CURRENT BOOKING
    # =========================
    current_hostel_url = "#"

    if all_bookings:

        booking = max(
            all_bookings,
            key=lambda x: x.created_at
        )

        booking_status = "Booked"

        if isinstance(booking, MaleBooking):

           current_room = booking.room.room_number
           current_hostel = "Male Hostel"
           current_hostel_url = "/male-hostel/"


        elif isinstance(booking, FemaleBooking):

           current_room = booking.room.room_number
           current_hostel = "Female Hostel"
           current_hostel_url = "/female-hostel/"


        elif isinstance(booking, ExternalBooking):

              current_room = booking.room.room_number
              current_hostel = booking.room.hostel.name
              current_hostel_url = "/hostels/"

        if (booking.status == "pending" and booking.payment_deadline):

           remaining_time = (booking.payment_deadline - timezone.now())

           countdown = max(0, int(remaining_time.total_seconds()))

           deadline = (booking.payment_deadline.isoformat())

    # =========================
    # BOOKING HISTORY
    # =========================

    male_history = MaleBooking.objects.filter(
        user=request.user
    )

    female_history = FemaleBooking.objects.filter(
        user=request.user
    )

    external_history = ExternalBooking.objects.filter(
        user=request.user
    )

    booking_history = (
        list(male_history) +
        list(female_history) +
        list(external_history)
    )

    booking_history.sort(
        key=lambda x: x.created_at,
        reverse=True
    )

    # =========================
    # AVATAR
    # =========================

    colors = [ "blue","green", "purple","orange","teal","olive"]

    email = request.user.email.lower()

    index = (sum(ord(c) for c in email)% len(colors))

    avatar_color = colors[index]
    avatar_text = email[0].upper()

    # =========================
    # LOAD CHAT
    # =========================

    messages = []

    if admin_user:

        messages = Message.objects.filter(
            Q(
                sender=request.user,
                receiver=admin_user
            ) |
            Q(
                sender=admin_user,
                receiver=request.user
            )
        ).order_by("created_at")

    # =========================
    # CONTEXT
    # =========================

    context = {
        "avatar_color": avatar_color,
        "avatar_text": avatar_text,
        "analytics": analytics,
        "booking": booking,
        "current_hostel_url": current_hostel_url,
        "countdown": countdown,
        "deadline": deadline,
        "current_room": current_room,
        "booking_status": booking_status,
        "current_hostel": current_hostel,
        "booking_history": booking_history,
        "messages": messages,
        "today": timezone.now().date(),
        "yesterday": timezone.now().date() - timedelta(days=1),
    }

    return render(request,"dashboard/student_dashboard.html", context)
from django.http import JsonResponse

@login_required
def student_dashboard_data(request):

    booking = None
    current_room = None
    current_hostel = "No Hostel"
    current_hostel_url = "#"
    booking_status = "No Booking"

    male_booking = MaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).order_by("-created_at").first()

    female_booking = FemaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).order_by("-created_at").first()

    external_booking = ExternalBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).order_by("-created_at").first()

    all_bookings = []

    if male_booking:
        all_bookings.append(male_booking)

    if female_booking:
        all_bookings.append(female_booking)

    if external_booking:
        all_bookings.append(external_booking)

    if all_bookings:

        booking = max(
            all_bookings,
            key=lambda x: x.created_at
        )

        booking_status = booking.status

        if isinstance(booking, MaleBooking):

            current_hostel = "Male Hostel"
            current_room = booking.room.room_number
            current_hostel_url = "/male-hostel/"

        elif isinstance(booking, FemaleBooking):

            current_hostel = "Female Hostel"
            current_room = booking.room.room_number
            current_hostel_url = "/female-hostel/"

        elif isinstance(booking, ExternalBooking):

            current_hostel = booking.hostel.name
            current_room = booking.room.room_number
            current_hostel_url = "/hostels/"

    return JsonResponse({

        "booking": bool(booking),

        "booking_status": booking_status,

        "current_room": current_room,

        "current_hostel": current_hostel,

        "current_hostel_url": current_hostel_url,

    })



def expire_bookings():

    now = timezone.now()

    # Male
    for booking in MaleBooking.objects.filter( status="pending"):

        if booking.payment_deadline < now:

            booking.status = "expired"
            booking.save()

            update_room_occupancy(booking.room)
            bump_system_version()

    # Female
    for booking in FemaleBooking.objects.filter(
        status="pending"
    ):

        if booking.payment_deadline < now:

            booking.status = "expired"
            booking.save()

            update_room_occupancy(booking.room)

    # External
    for booking in ExternalBooking.objects.filter(
        status="pending"
    ):

        if booking.payment_deadline < now:

            booking.status = "expired"
            booking.save()

            booking.room.status = "available"
            booking.room.save()
            bump_system_version()


@admin_required
def dashboard_home(request):
    expire_bookings()

    # BLOCK NON ADMINS
    if not request.user.is_staff:
        return HttpResponse("Access Denied")

    hostels = Hostel.objects.all()
    settings, created = SystemSettings.objects.get_or_create(id=1)


    # =========================
    # RECENT BOOKINGS
    # =========================

    recent_bookings = []

    # Male Hostel Bookings
    for booking in MaleBooking.objects.all():

        recent_bookings.append({
            "id": booking.id,
            "student": booking.full_name,
            "room": booking.room.room_number,
            "hostel": "Male Hostel",
            "hostel_type": "Male Hostel",
            "status": booking.status,
            "phone": booking.phone,
            "created_at": booking.created_at,
            "booking_type": "male"
        })

    # Female Hostel Bookings
    for booking in FemaleBooking.objects.all():

        recent_bookings.append({
            "id": booking.id,
            "student": booking.full_name,
            "room": booking.room.room_number,
            "hostel": "Female Hostel",
            "hostel_type": "Female Hostel",
            "status": booking.status,
            "phone": booking.phone,
            "created_at": booking.created_at,
            "booking_type": "female"
        })

    # External Hostel Bookings
    for booking in ExternalBooking.objects.all():

        recent_bookings.append({
            "id": booking.id,
            "student": booking.full_name,
            "room": booking.room.room_number,
            "hostel": booking.hostel.name,
            "hostel_type": "External Hostel",
            "status": booking.status,
            "phone": booking.phone,
            "created_at": booking.created_at,
            "booking_type": "external"
        })

    # Sort newest first
    recent_bookings.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    # Only latest 5
    recent_bookings = recent_bookings[:5]

    # =========================
    # STUDENT CHAT
    # =========================

    students = User.objects.filter(
        sent_messages__receiver=request.user
    ).distinct()

    selected_student = None
    messages = []

    student_id = request.GET.get("student")

    if student_id:

        selected_student = User.objects.get(
            id=student_id
        )

        messages = Message.objects.filter(
            sender__in=[
                request.user,
                selected_student
            ],
            receiver__in=[
                request.user,
                selected_student
            ]
        ).order_by("created_at")

        if request.method == "POST":

            text = request.POST.get("message")

            uploaded_file = request.FILES.get("file")

            message_type = "text"

            if uploaded_file:

                content_type = uploaded_file.content_type

                if content_type.startswith("image"):
                    message_type = "image"

                elif content_type.startswith("audio"):
                    message_type = "voice"

                else:
                    message_type = "file"

            if text or uploaded_file:

                Message.objects.create(
                    sender=request.user,
                    receiver=selected_student,
                    message=text,
                    file=uploaded_file,
                    message_type=message_type
                )

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":

                return JsonResponse({
                    "success": True
                })

            return redirect(f"/dashboard/?student={selected_student.id}")

    return render(request,"dashboard/dashboard.html",
        {
            "hostels": hostels,
            "recent_bookings": recent_bookings,
            "students": students,
            "selected_student": selected_student,
            "messages": messages,
            "today": timezone.now().date(),
            "yesterday": (timezone.now().date()- timedelta(days=1)),
            "settings": settings,
        }
    )
def edit_hostel(request, id):

    hostel = get_object_or_404(Hostel, id=id)

    if request.method == "POST":

        form = HostelForm(
            request.POST,
            request.FILES,
            instance=hostel
        )

        if form.is_valid():
            form.save()
            bump_system_version()
            return redirect('dashboard_home')

    else:
        form = HostelForm(instance=hostel)

    return render(
        request,
        'dashboard/edit_hostel.html',
        {'form': form}
    )


def delete_hostel(request, id):

    hostel = get_object_or_404(Hostel, id=id)

    hostel.delete()
    bump_system_version()

    return redirect('dashboard_home')
from django.shortcuts import render, redirect
def add_hostel(request):
    if request.method == "POST":
        form = HostelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("dashboard_home")
        else:
          print(form.errors)

    else:
        form = HostelForm()

    return render(request, "dashboard/add_hostel.html", {
        "form": form
    })

from core.models import HostelAnalytics
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
@admin_required
def analytics_dashboard(request):

    analytics, created = HostelAnalytics.objects.get_or_create(pk=1)

    if request.method == "POST":

        analytics.electricity = request.POST.get("electricity")
        analytics.water = request.POST.get("water")
        analytics.maintenance = request.POST.get("maintenance")

        analytics.occupied = request.POST.get("occupied")
        analytics.available = request.POST.get("available")

        analytics.mon = request.POST.get("mon")
        analytics.tue = request.POST.get("tue")
        analytics.wed = request.POST.get("wed")
        analytics.thu = request.POST.get("thu")
        analytics.fri = request.POST.get("fri")
        analytics.sat = request.POST.get("sat")
        analytics.sun = request.POST.get("sun")

        analytics.save()

    return render(
        request,
        "dashboard/analytics_dashboard.html",
        {
            "analytics": analytics
        }
    )

from django.contrib.auth import authenticate, login

def admin_login(request):

    # USER ALREADY LOGGED IN

    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect("dashboard_home")

        return redirect("student_dashboard")

    # LOGIN FORM

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user and user.is_staff:

            login(request, user)

            request.session["mode"] = "admin"

            return redirect("dashboard_home")

        return render(
            request,
            "admin_login.html",
            {
                "error": "Invalid admin credentials"
            }
        )

    return render(
        request,
        "admin_login.html"
    )

from .models import Folder
@admin_required
def file_manager(request):

    folders = Folder.objects.filter(user=request.user)

    context = {
        'folders': folders
    }

    return render(request, 'dashboard/file_manager.html', context)

from .models import FileItem, Folder

@admin_required
def upload_file(request):

    if request.method == 'POST':

        uploaded_file = request.FILES.get('file')
        folder_id = request.POST.get('folder_id')

        folder = None

        if folder_id:
            try:
                folder = Folder.objects.get(id=folder_id)
            except Folder.DoesNotExist:
                folder = None

        new_file = FileItem.objects.create(
       user=request.user,
       file=uploaded_file,
       folder=folder
        )

        return JsonResponse({
            'success': True,
            'id': new_file.id,
            'name': new_file.file.name,
            'url': new_file.file.url
        })

    return JsonResponse({'success': False})



from .models import FileItem
import os
@login_required

def get_files(request):

    folder_id = request.GET.get("folder")

    files = FileItem.objects.all()

    if folder_id:
        files = files.filter(folder_id=folder_id)

    folders = Folder.objects.all()

    return JsonResponse({

        "files": [
            {
                "id": file.id,
                "name": file.file.name.split("/")[-1],
                "url": file.file.url,
                "uploaded_at": file.uploaded_at.strftime("%Y-%m-%d"),
                "type": file.file.name.split(".")[-1].lower(),
                "size": "Unknown"
                
            }

            for file in files
        ],

        "folders": [
            {
                "id": folder.id,
                "name": folder.name
            }

            for folder in folders
        ]

    })
def delete_file(request, id):

    if request.method == "DELETE":

        try:

            file = FileItem.objects.get(id=id)

            file.file.delete()

            file.delete()

            return JsonResponse({
                "success": True
            })

        except:

            return JsonResponse({
                "success": False
            })

    return JsonResponse({
        "success": False
    })

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Folder

@login_required
@require_POST
def create_folder(request):

    folder_name = request.POST.get("name")

    if not folder_name:

        return JsonResponse({
            "success": False,
            "error": "Folder name required"
        })

    folder = Folder.objects.create(
        user=request.user,
        name=folder_name
    )

    return JsonResponse({
        "success": True,
        "id": folder.id,
        "name": folder.name
    })

def delete_folder(request, id):

    if request.method == "DELETE":

        folder = Folder.objects.get(id=id)

        folder.delete()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })


@csrf_exempt
def rename_file(request, id):

    if request.method == "POST":

        data = json.loads(request.body)

        new_name = data.get("name")

        file = FileItem.objects.get(id=id)

        old_path = file.file.path

        extension = old_path.split(".")[-1]

        new_file_name = f"{new_name}.{extension}"

        new_path = os.path.join(
            os.path.dirname(old_path),
            new_file_name
        )

        os.rename(old_path, new_path)

        file.file.name = f"file_manager/{new_file_name}"

        file.save()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })
@csrf_exempt
def rename_folder(request, id):

    if request.method == "POST":

        data = json.loads(request.body)

        folder = Folder.objects.get(id=id)

        folder.name = data.get("name")

        folder.save()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
@admin_required
@csrf_exempt
def update_user_status(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "error": "Invalid request"
        })

    try:

        data = json.loads(request.body)

        user_id = data.get("user_id")
        status = data.get("status")

        phone = data.get("phone", "")
        department = data.get("department", "")
        level = data.get("level", "")
        matric_no = data.get("matric_no", "")
        gender = data.get("gender", "")

        user = User.objects.get(id=user_id)

        profile, _ = Profile.objects.get_or_create(
            user=user
        )

        # Account status
        user.is_active = status == "active"
        user.save()

        # Profile updates
        profile.phone = phone
        profile.department = department
        profile.level = level
        profile.matric_no = matric_no
        profile.gender = gender

        profile.save()

        return JsonResponse({
            "success": True,
            "message": "User updated successfully"
        })

    except User.DoesNotExist:

        return JsonResponse({
            "success": False,
            "error": "User not found"
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "error": str(e)
        })

@admin_required
def room_management(request):

    male_rooms = MaleRoom.objects.all()
    female_rooms = FemaleRoom.objects.all()

    external_hostels = Hostel.objects.prefetch_related("rooms")

    context = {
        "male_rooms": male_rooms,
        "female_rooms": female_rooms,
        "external_hostels": external_hostels,
    }

    return render(
        request,
        "dashboard/room_management.html",
        context
    )
@admin_required
@csrf_exempt
def update_room_status(request):

    if request.method == "POST":

        data = json.loads(request.body)

        room_id = data.get("room_id")
        status = data.get("status")
        hostel_type = data.get("hostel_type")

        if hostel_type == "male":
            room = MaleRoom.objects.get(id=room_id)

        elif hostel_type == "female":
            room = FemaleRoom.objects.get(id=room_id)

        elif hostel_type == "external":
            room = ExternalRoom.objects.get(id=room_id)

        else:
            return JsonResponse({ "success": False})

        room.status = status
        room.save()
        bump_system_version()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })

@student_required
def student_messages(request):

    admin_user = User.objects.filter(
        is_staff=True
    ).first()

    messages = Message.objects.filter(
        sender__in=[request.user, admin_user],
        receiver__in=[request.user, admin_user]
    ).order_by("created_at")

    if request.method == "POST":

        text = request.POST.get("message")

        if text:

            Message.objects.create(
                sender=request.user,
                receiver=admin_user,
                message=text
            )

        return redirect("student_messages")

    return render(
        request,
        "dashboard/student_messages.html",
        {
            "messages": messages,
            "admin_user": admin_user
        }
    )

@login_required
def admin_messages(request, user_id):

    if not request.user.is_staff:
        return redirect("student_dashboard")

    student = User.objects.get(id=user_id)

    messages = Message.objects.filter(
        sender__in=[request.user, student],
        receiver__in=[request.user, student]
    ).order_by("created_at")

    if request.method == "POST":

        text = request.POST.get("message")

        if text:

            Message.objects.create(
                sender=request.user,
                receiver=student,
                message=text
            )

        return redirect("admin_messages", user_id=student.id)

    return render(
        request,
        "dashboard/admin_messages.html",
        {
            "messages": messages,
            "student": student
        }
    )

@login_required
def admin_chat_list(request):

    if not request.user.is_staff:
        return redirect("student_dashboard")

    students = User.objects.filter(
        received_messages__receiver=request.user
    ).distinct()

    return render(
        request,
        "dashboard/admin_chat_list.html",
        {
            "students": students
        }
    )

@login_required
def delete_message(request, message_id):

    message = Message.objects.get(id=message_id)

    # ADMIN OR OWNER ONLY
    if not (
        request.user.is_staff or
        message.sender == request.user
    ):

        return redirect("student_dashboard")

    message.delete()

    return redirect(
        request.META.get("HTTP_REFERER")
    )

@student_required
def external_hostel_booking(request, room_id):

    room = ExternalRoom.objects.get(id=room_id)

    hostel = room.hostel

    # =========================
    # CHECK MALE BOOKING
    # =========================

    male_booking = MaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    # =========================
    # CHECK FEMALE BOOKING
    # =========================

    female_booking = FemaleBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    # =========================
    # CHECK EXTERNAL BOOKING
    # =========================

    external_booking = ExternalBooking.objects.filter(
        user=request.user,
        status__in=["pending", "approved"]
    ).first()

    # =========================
    # BLOCK OTHER BOOKINGS
    # =========================

    if male_booking or female_booking:

        return HttpResponse(
            "You already have a school hostel booking."
        )

    # =========================
    # ROOM ALREADY OCCUPIED
    # =========================

    if room.status == "occupied":

        return HttpResponse(
            "This room is already occupied."
        )

    # =========================
    # USER HAS EXTERNAL BOOKING
    # =========================

    if external_booking:

        # =====================
        # SAME ROOM = REBOOK
        # =====================

        if external_booking.room.id == room.id:

            # EXPIRED
            if external_booking.payment_deadline < timezone.now():

                room.status = "available"
                room.save()

                external_booking.status = "expired"
                external_booking.save()

                external_booking.delete()

            else:

                return HttpResponse(
                    "You already booked this room."
                )

        else:

            return HttpResponse(
                "You already booked another room."
            )

    # =========================
    # CREATE BOOKING
    # =========================

    if request.method == "POST":

        form = ExternalBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.hostel = hostel
            booking.payment_deadline = ( timezone.now() + timedelta(minutes=2))
            booking.save()

            # =====================
            # LOCK ROOM
            # =====================

            room.status = "occupied"

            room.save()

            return redirect("student_dashboard")

    else:
 
        
       form = ExternalBookingForm(
          initial={

        "full_name":
        request.user.first_name,

        "email":
        request.user.email,

        "gender":
        request.user.user_profile.gender,

        "phone":
        request.user.user_profile.phone,

     }
    )


    return render(
        request,
        "booking/external_booking.html",
        {
            "form": form,
            "room": room,
            "hostel": hostel
        }
    )


@admin_required
def system_settings_page(request):

    if not request.user.is_staff:
        return HttpResponse("Access Denied")

    settings, created = (SystemSettings.objects.get_or_create(id=1))

    if request.method == "POST":

        settings.male_booking_deadline = (
            request.POST.get(
                "male_booking_deadline"
            )
        )

        settings.female_booking_deadline = (
            request.POST.get(
                "female_booking_deadline"
            )
        )

        settings.external_booking_deadline = (request.POST.get("external_booking_deadline"))
        settings.male_hostel_price = request.POST.get("male_hostel_price")

        settings.female_hostel_price = request.POST.get("female_hostel_price")
        

        settings.save()
        bump_system_version()

    return render(
        request,
        "dashboard/settings.html",
        {
            "settings": settings
        }
    )


@login_required
def get_system_settings(request):

    settings, _ = SystemSettings.objects.get_or_create(
        id=1
    )

    return JsonResponse({

        "male_booking_deadline":
        settings.male_booking_deadline,

        "female_booking_deadline":
        settings.female_booking_deadline,

        "external_booking_deadline":
        settings.external_booking_deadline,

        "allow_male_booking":
        settings.allow_male_booking,

        "allow_female_booking":
        settings.allow_female_booking,

        "allow_external_booking":
        settings.allow_external_booking,
    })

@csrf_exempt
@admin_required
def update_system_settings(request):

    if request.method == "POST":

        settings, _ = SystemSettings.objects.get_or_create(
            id=1
        )

        data = json.loads(request.body)

        settings.male_booking_deadline = data.get(
            "male_booking_deadline"
        )

        settings.female_booking_deadline = data.get(
            "female_booking_deadline"
        )

        settings.external_booking_deadline = data.get(
            "external_booking_deadline"
        )

        settings.allow_male_booking = data.get("allow_male_booking")

        settings.allow_female_booking = data.get("allow_female_booking")

        settings.allow_external_booking = data.get("allow_external_booking")
        settings.male_hostel_price = data.get("male_hostel_price")

        settings.female_hostel_price = data.get("female_hostel_price")

        settings.save()

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })

from django.http import JsonResponse
from core.models import Hostel, MaleRoom, FemaleRoom

@login_required
def search_hostels(request):

    query = request.GET.get("q", "").strip()

    results = []

    if not query:
        return JsonResponse({"results": []})

    # External Hostels
    hostels = Hostel.objects.filter(
        name__icontains=query
    )

    for hostel in hostels:

        results.append({
            "name": hostel.name,
            "url": "/hostels/",
            "type": "External Hostel"
        })

    # Male Hostel
    if "male".startswith(query.lower()) or query.lower() in "male hostel":

        results.append({
            "name": "Male Hostel",
            "url": "/male-hostel/",
            "type": "School Hostel"
        })

    # Female Hostel
    if "female".startswith(query.lower()) or query.lower() in "female hostel":

        results.append({
            "name": "Female Hostel",
            "url": "/female-hostel/",
            "type": "School Hostel"
        })

    # Male Rooms
    male_rooms = MaleRoom.objects.filter(
        room_number__icontains=query
    )

    for room in male_rooms:

        results.append({
            "name": f"Room {room.room_number}",
            "url": "/male-hostel/",
            "type": "Male Room"
        })

    # Female Rooms
    female_rooms = FemaleRoom.objects.filter(
        room_number__icontains=query
    )

    for room in female_rooms:

        results.append({
            "name": f"Room {room.room_number}",
            "url": "/female-hostel/",
            "type": "Female Room"
        })

    return JsonResponse({
        "results": results[:10]
    })