from django.urls import path
from .views import google_login_redirect
from .views import *  

urlpatterns = [
    path("profile/", profile, name="profile"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("main/", main_view, name="main"),
    path("google/login/", google_login_redirect, name="google_login_redirect"),  # ✅ เพิ่ม path ที่หายไป
    path("logout/", login_view, name="logout")
]
