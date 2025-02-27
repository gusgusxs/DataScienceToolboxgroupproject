from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    has_farm = models.BooleanField(default=False)  # ผู้ใช้สามารถเป็นทั้งผู้ซื้อและผู้ขาย

    # ✅ เพิ่ม related_name เพื่อป้องกันการ clash กับ Django User Model
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ แก้ตรงนี้
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    line_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
     return self.user.username