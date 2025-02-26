from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"cows", CowViewSet)

urlpatterns = [
    path("", cow_list, name="cow_list"),  # ✅ URL ดูรายการลูกวัว
    path("create/", cow_create, name="cow_create"),  # ✅ URL เพิ่มลูกวัว
    path("<int:pk>/edit/", cow_update, name="cow_update"),  # ✅ URL แก้ไขลูกวัว
    path("<int:pk>/delete/", cow_delete, name="cow_delete"),  # ✅ URL ลบลูกวัว
    path("community/", community_view, name="community"),  # หน้าหลัก Community
    path("community/<int:cow_id>/", cow_detail_view, name="cow_detail"),  # หน้ารายละเอียดลูกวัว
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
