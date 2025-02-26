from django.db import models

class Sale(models.Model):
    buyer = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    cow = models.ForeignKey("cows.Cow", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed")])
    created_at = models.DateTimeField(auto_now_add=True)

