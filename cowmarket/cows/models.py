from django.db import models

class Cow(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)  # ✅ เปลี่ยนจาก choices เป็น CharField ให้ผู้ใช้กรอกเอง
    age = models.IntegerField()
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="cows/", blank=True, null=True)

    # ✅ pedigree_file รองรับทั้งรูปภาพและไฟล์ทั่วไป
    pedigree_file = models.FileField(upload_to="pedigree/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



