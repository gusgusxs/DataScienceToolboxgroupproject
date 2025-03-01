from rest_framework import serializers
from .models import Cow

class CowSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)  # ✅ ห้ามเว้นว่าง
    age = serializers.IntegerField(required=True, min_value=0)  # ✅ ต้องเป็นค่าบวก
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = Cow
        fields = "__all__"
