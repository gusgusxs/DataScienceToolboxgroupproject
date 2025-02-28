from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
#ใช้ในการทดสอบ REST API ของ Django
router = DefaultRouter()
router.register(r"cows", CowViewSet)

urlpatterns = [
    path("my-purchases/", my_purchases, name="my_purchases"),
    path("buy/<int:cow_id>/", buy_cow, name="buy_cow"),
    path("notifications/", notifications_view, name="notifications"),
    path("", cow_list, name="cow_list"),  # ✅ URL ดูรายการลูกวัว
    path("create/", cow_create, name="cow_create"),  # ✅ URL เพิ่มลูกวัว
    path("<int:pk>/edit/", cow_update, name="cow_update"),  # ✅ URL แก้ไขลูกวัว
    path("<int:pk>/delete/", cow_delete, name="cow_delete"),  # ✅ URL ลบลูกวัว
    path("community/", community_view, name="community"),  # หน้าหลัก Community
    path("community/<int:cow_id>/", cow_detail_view, name="cow_detail"),  # หน้ารายละเอียดลูกวัว
    path("confirm_transaction/<int:cow_id>/", confirm_transaction, name="confirm_transaction"),
]
