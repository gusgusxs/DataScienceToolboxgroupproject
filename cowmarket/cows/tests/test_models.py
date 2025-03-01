from django.test import TestCase
from django.contrib.auth import get_user_model
from cows.models import Cow, Notification

class CowModelTest(TestCase):
    def setUp(self):
        """สร้าง User และ Cow สำหรับทดสอบ"""
        self.user = get_user_model().objects.create_user(username="seller", password="password123")
        self.buyer = get_user_model().objects.create_user(username="buyer", password="password123")

        self.cow = Cow.objects.create(
            name="Bessie",
            breed="Angus",
            age=3,
            weight=450.5,
            price=1200.00,
            owner=self.user,  # Seller
            transaction_status="available"
        )

    def test_cow_creation(self):
        """ทดสอบว่าสามารถสร้าง Cow ได้ถูกต้อง"""
        self.assertEqual(self.cow.name, "Bessie")
        self.assertEqual(self.cow.breed, "Angus")
        self.assertEqual(self.cow.age, 3)
        self.assertEqual(self.cow.weight, 450.5)
        self.assertEqual(self.cow.price, 1200.00)
        self.assertEqual(self.cow.owner, self.user)
        self.assertEqual(self.cow.transaction_status, "available")
        self.assertEqual(self.cow.view_count, 0)  # Default value

    def test_cow_str_method(self):
        """ทดสอบ __str__ method"""
        self.assertEqual(str(self.cow), "Bessie (available)")

    def test_update_transaction_status(self):
        """ทดสอบการอัปเดตสถานะของวัว"""
        self.cow.transaction_status = "sold"
        self.cow.buyer = self.buyer  # Assign buyer
        self.cow.save()

        updated_cow = Cow.objects.get(id=self.cow.id)
        self.assertEqual(updated_cow.transaction_status, "sold")
        self.assertEqual(updated_cow.buyer, self.buyer)

    def test_on_delete_owner(self):
        """ทดสอบว่า Cow ถูกลบเมื่อ Owner ถูกลบ"""
        self.user.delete()
        with self.assertRaises(Cow.DoesNotExist):
            Cow.objects.get(id=self.cow.id)

    def test_on_delete_buyer(self):
        """ทดสอบว่า Buyer ถูกลบแล้ว Cow ยังคงอยู่"""
        self.cow.buyer = self.buyer
        self.cow.save()
        self.buyer.delete()

        updated_cow = Cow.objects.get(id=self.cow.id)
        self.assertIsNone(updated_cow.buyer)  # Buyer ต้องเป็น None

class NotificationModelTest(TestCase):
    def setUp(self):
        """สร้าง User และ Notification สำหรับทดสอบ"""
        self.user = get_user_model().objects.create_user(username="tester", password="password123")
        self.notification = Notification.objects.create(
            message="New cow available!",
            user=self.user
        )

    def test_notification_creation(self):
        """ทดสอบว่าสามารถสร้าง Notification ได้ถูกต้อง"""
        self.assertEqual(self.notification.message, "New cow available!")
        self.assertEqual(self.notification.user, self.user)
        self.assertFalse(self.notification.is_read)  # ค่า Default ต้องเป็น False

    def test_notification_str_method(self):
        """ทดสอบ __str__ method"""
        self.assertEqual(str(self.notification), "🔔 New cow available!")
