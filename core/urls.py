
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views as dashboard_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('male-hostel/', views.male, name='male-hostel'),
    path('female-hostel/', views.female, name='female-hostel'),
    path('hostels/', views.hostel_list, name='hostels'),
    path('load-more-hostels/', views.load_more_hostels, name='load_more_hostels'),
    path("check-email/", views.check_email, name="check_email"),

    path("student_dashboard/",dashboard_views.student_dashboard,name="student_dashboard"),
    path( "student-dashboard-data/",dashboard_views.student_dashboard_data,name="student_dashboard_data",),
    path("logout/", views.logout_view, name="logout"),
    path('add-hostel/', views.add_hostel, name='add_hostel'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path("control-room-7392/",views.admin_login, name="admin_login"),
    path('male-booking/<int:room_id>/',views.male_room_booking,name='male_room_booking'),
    path('female-booking/<int:room_id>/', views.female_room_booking,name='female_room_booking'),
    path("external-booking/<int:room_id>/",dashboard_views.external_hostel_booking,name="external_hostel_booking"),
    path("system-version/",views.system_version,name="system_version"),
    path("payment/demo/",views.demo_payment,name="demo_payment",),

    


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)