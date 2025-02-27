from django.conf import settings 
from django.db import models


class Cow(models.Model):
    TRANSACTION_STATUS = [
        ("available", "พร้อมขาย"),
        ("pending", "รอการยืนยัน"),
        ("sold", "ขายสำเร็จ"),
    ]

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)  
    age = models.IntegerField()
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="cows/", blank=True, null=True)
    pedigree_file = models.FileField(upload_to="pedigree/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchases")
    
    transaction_status = models.CharField(
        max_length=20, choices=TRANSACTION_STATUS, default="available"
    )

    def __str__(self):
        return f"{self.name} ({self.transaction_status})"


class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"🔔 {self.message}"

