from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from cows.models import Cow, Notification

class CowViewsTest(TestCase):
    def setUp(self):
        """สร้างข้อมูลสำหรับทดสอบ"""
        self.client = APIClient()

        # สร้าง Users
        self.owner = get_user_model().objects.create_user(username="seller", password="password123")
        self.buyer = get_user_model().objects.create_user(username="buyer", password="password123")

        self.client.force_login(self.owner)  # ✅ ล็อกอินเป็นเจ้าของวัว

        # สร้างวัว 1 ตัว
        self.cow = Cow.objects.create(
            name="Bessie",
            breed="Angus",
            age=3,
            weight=450.5,
            price=1200.00,
            owner=self.owner
        )

    def test_cow_list_view(self):
        """ทดสอบหน้า cow_list"""
        url = reverse("cow_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Bessie")  # ✅ ตรวจสอบว่ามีชื่อวัวในหน้า

    def test_cow_detail_view(self):
        """ทดสอบ cow_detail"""
        self.client.force_login(self.buyer)  # ✅ เปลี่ยนเป็น Buyer
        url = reverse("cow_detail", args=[self.cow.id])  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)  # ✅ ต้องโหลดหน้า cow_detail สำเร็จ
        self.assertContains(response, f"{self.cow.name}")  # ✅ ตรวจสอบว่าชื่อวัวแสดงผล

    def test_cow_create_view(self):
        """ทดสอบการเพิ่ม Cow"""
        url = reverse("cow_create")
        data = {
            "name": "Daisy",
            "breed": "Holstein",
            "age": 2,
            "weight": 400.0,
            "price": 1500.00,
        }
        response = self.client.post(url, data, follow=True)  # ✅ ใช้ follow=True ตาม Redirect

        self.assertEqual(response.status_code, 200)  # ✅ หน้า cow_list ต้องโหลดสำเร็จ
        self.assertEqual(Cow.objects.count(), 2)  # ✅ วัวต้องเพิ่มขึ้นเป็น 2 ตัว
        self.assertContains(response, "Daisy")  # ✅ ตรวจสอบว่าชื่อ Daisy แสดงในหน้า

    def test_cow_delete_view(self):
        """ทดสอบการลบ Cow"""
        url = reverse("cow_delete", args=[self.cow.id])  
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # ✅ ต้อง Redirect
        self.assertEqual(Cow.objects.count(), 0)  # ✅ วัวต้องถูกลบไป

    def test_buy_cow_view(self):
        """ทดสอบการซื้อวัว"""
        self.client.force_login(self.buyer)  # ✅ เปลี่ยนเป็น Buyer
        url = reverse("buy_cow", args=[self.cow.id])

        response = self.client.post(url)

        self.cow.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # ✅ Redirect
        self.assertEqual(self.cow.transaction_status, "pending")
        self.assertEqual(self.cow.buyer, self.buyer)

    def test_buy_cow_self(self):
        """ทดสอบว่าผู้ใช้ไม่สามารถซื้อวัวของตัวเองได้"""
        url = reverse("buy_cow", args=[self.cow.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # ✅ Redirect
        self.assertNotEqual(self.cow.transaction_status, "pending")  # ✅ ไม่ควรเปลี่ยนสถานะ

    def test_confirm_transaction_sold(self):
        """ทดสอบการยืนยันการซื้อขายวัว"""
        self.cow.transaction_status = "pending"
        self.cow.buyer = self.buyer
        self.cow.save()

        url = reverse("confirm_transaction", args=[self.cow.id])
        response = self.client.post(url, {"status": "sold"})

        self.cow.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # ✅ Redirect
        self.assertEqual(self.cow.transaction_status, "sold")

    def test_notifications_view(self):
        """ทดสอบหน้าแจ้งเตือน"""
        Notification.objects.create(user=self.owner, message="Test Notification")
        
        self.client.force_login(self.owner)  # ✅ ล็อกอินก่อนเข้าหน้าแจ้งเตือน
        url = reverse("notifications")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Test Notification")  # ✅ ตรวจสอบข้อความแจ้งเตือน
