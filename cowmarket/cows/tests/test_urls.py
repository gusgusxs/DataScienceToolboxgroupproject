from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cows.views import (
    cow_list, cow_create, cow_update, cow_delete,
    buy_cow, confirm_transaction, my_purchases,
    notifications_view, community_view, cow_detail_view
)

class TestUrls(SimpleTestCase):
    """ทดสอบว่า URL สามารถ resolve ไปยัง views ที่ถูกต้อง"""

    def test_cow_list_url_resolves(self):
        url = reverse("cow_list")
        self.assertEqual(resolve(url).func, cow_list)

    def test_cow_create_url_resolves(self):
        url = reverse("cow_create")
        self.assertEqual(resolve(url).func, cow_create)

    def test_cow_update_url_resolves(self):
        url = reverse("cow_update", args=[1])  # ทดสอบอัปเดตวัว ID=1
        self.assertEqual(resolve(url).func, cow_update)

    def test_cow_delete_url_resolves(self):
        url = reverse("cow_delete", args=[1])  # ทดสอบลบวัว ID=1
        self.assertEqual(resolve(url).func, cow_delete)

    def test_buy_cow_url_resolves(self):
        url = reverse("buy_cow", args=[1])  # ทดสอบซื้อวัว ID=1
        self.assertEqual(resolve(url).func, buy_cow)

    def test_confirm_transaction_url_resolves(self):
        url = reverse("confirm_transaction", args=[1])  # ทดสอบยืนยันการซื้อวัว ID=1
        self.assertEqual(resolve(url).func, confirm_transaction)

    def test_my_purchases_url_resolves(self):
        url = reverse("my_purchases")
        self.assertEqual(resolve(url).func, my_purchases)

    def test_notifications_url_resolves(self):
        url = reverse("notifications")
        self.assertEqual(resolve(url).func, notifications_view)

    def test_community_url_resolves(self):
        url = reverse("community")
        self.assertEqual(resolve(url).func, community_view)

    def test_cow_detail_url_resolves(self):
        url = reverse("cow_detail", args=[1])  # ทดสอบดูรายละเอียดวัว ID=1
        self.assertEqual(resolve(url).func, cow_detail_view)
