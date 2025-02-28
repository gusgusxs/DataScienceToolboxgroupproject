from django.urls import path
from .views import login_view, google_login_redirect
from .views import *  
from . import views

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("main/", main_view, name="main"),
    path("login/", login_view, name="login"),  # ✅ หน้า Login
    path("google/login/", google_login_redirect, name="google_login_redirect"),  # ✅ เพิ่ม path ที่หายไป
    path("profile/", profile, name="profile"),
    path('cow/<int:cow_id>/', views.cow_detail_view, name='cow_detail'),
]

