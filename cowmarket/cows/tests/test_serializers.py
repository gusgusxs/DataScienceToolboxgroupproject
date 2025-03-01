from django.test import TestCase
from cows.models import Cow
from cows.serializers import CowSerializer
from django.contrib.auth import get_user_model

class CowSerializerTest(TestCase):
    def setUp(self):
        """สร้างข้อมูลสำหรับทดสอบ"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")

        self.cow_data = {
            "name": "Brownie",
            "breed": "Jersey",
            "age": 4,
            "weight": 500.0,
            "price": "2000.00",  # ✅ ให้เป็น string ตามที่ Serializer รับ
            "owner": self.user.id  # ✅ ต้องเป็น id เพราะเป็น ForeignKey
        }

        self.invalid_data = {
            "name": "",  # ❌ ชื่อห้ามว่าง
            "breed": "Jersey",
            "age": -1,  # ❌ อายุไม่สามารถติดลบได้
            "weight": 500.0,
            "price": "not_a_number",  # ❌ ราคาต้องเป็นตัวเลข
            "owner": self.user.id
        }

        self.cow = Cow.objects.create(
            name="Brownie",
            breed="Jersey",
            age=4,
            weight=500.0,
            price=2000.00,
            owner=self.user
        )

    def test_cow_serializer_valid_data(self):
        """ทดสอบว่า CowSerializer สามารถ serialize ข้อมูลได้ถูกต้อง"""
        serializer = CowSerializer(instance=self.cow)
        data = serializer.data

        self.assertEqual(data["name"], self.cow.name)
        self.assertEqual(data["breed"], self.cow.breed)
        self.assertEqual(data["age"], self.cow.age)
        self.assertEqual(data["weight"], self.cow.weight)
        self.assertEqual(float(data["price"]), float(self.cow.price))  # ✅ เช็คค่า price
        self.assertEqual(data["owner"], self.cow.owner.id)  # ✅ owner ต้องตรงกัน

    def test_cow_serializer_invalid_data(self):
        """ทดสอบว่า CowSerializer ตรวจจับข้อมูลผิดพลาดได้"""
        serializer = CowSerializer(data=self.invalid_data)

        self.assertFalse(serializer.is_valid())  # ✅ Serializer ควรเป็น False
        self.assertIn("name", serializer.errors)  # ✅ ควรมี error name
        self.assertIn("age", serializer.errors)  # ✅ ควรมี error age (min_value=0)
        self.assertIn("price", serializer.errors)  # ✅ ควรมี error price

    def test_cow_serializer_create(self):
        """ทดสอบว่าสามารถสร้าง Cow ได้ผ่าน Serializer"""
        serializer = CowSerializer(data=self.cow_data)

        self.assertTrue(serializer.is_valid(), msg=f"Serializer Errors: {serializer.errors}")  # ✅ แสดง error message ถ้า test fail
        cow_instance = serializer.save()

        self.assertEqual(cow_instance.name, self.cow_data["name"])
        self.assertEqual(cow_instance.breed, self.cow_data["breed"])
        self.assertEqual(cow_instance.age, self.cow_data["age"])
        self.assertEqual(cow_instance.weight, self.cow_data["weight"])
        self.assertEqual(float(cow_instance.price), float(self.cow_data["price"]))
        self.assertEqual(cow_instance.owner.id, self.cow_data["owner"])

    def test_cow_serializer_update(self):
        """ทดสอบว่าสามารถอัปเดต Cow ผ่าน Serializer"""
        updated_data = {
            "name": "Updated Brownie",
            "breed": "Holstein",
            "age": 5,
            "weight": 550.0,
            "price": "2500.00",
            "owner": self.user.id
        }
        serializer = CowSerializer(instance=self.cow, data=updated_data, partial=True)
        
        self.assertTrue(serializer.is_valid(), msg=f"Serializer Errors: {serializer.errors}")  # ✅ แสดง error message ถ้า test fail
        updated_cow = serializer.save()

        self.assertEqual(updated_cow.name, "Updated Brownie")
        self.assertEqual(updated_cow.breed, "Holstein")
        self.assertEqual(updated_cow.age, 5)
        self.assertEqual(updated_cow.weight, 550.0)
        self.assertEqual(float(updated_cow.price), 2500.00)
