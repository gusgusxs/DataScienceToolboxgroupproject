from django.urls import path
from .views import login_view, google_login_redirect
from .views import *  

urlpatterns = [
    path("my-farm/", farm_profile_view, name="farm_profile"),
    path("main/", main_view, name="main"),
    path("login/", login_view, name="login"),  # ✅ หน้า Login
    path("google/login/", google_login_redirect, name="google_login_redirect"),  # ✅ เพิ่ม path ที่หายไป
]
