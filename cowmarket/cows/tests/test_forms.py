from django.test import TestCase
from cows.forms import CowForm

class TestCowForm(TestCase):
    """ทดสอบฟอร์ม CowForm"""

    def test_cow_form_valid_data(self):
        """✅ ทดสอบว่าฟอร์มสามารถรับข้อมูลที่ถูกต้องได้"""
        form = CowForm(data={
            "name": "Brownie",
            "breed": "Jersey",
            "age": 3,
            "weight": 500.0,
            "price": 1500.00
        })
        self.assertTrue(form.is_valid())  # ✅ ต้องผ่าน validation

    def test_cow_form_missing_required_fields(self):
        """❌ ทดสอบว่าฟอร์มแจ้งเตือนเมื่อไม่มีฟิลด์ที่จำเป็น"""
        form = CowForm(data={})  # ❌ ไม่ส่งข้อมูลเลย
        self.assertFalse(form.is_valid())  # ❌ ต้องไม่ผ่าน validation
        self.assertIn("name", form.errors)  # ❌ ฟิลด์ `name` ต้องมี error
        self.assertIn("breed", form.errors)  # ❌ ฟิลด์ `breed` ต้องมี error
        self.assertIn("age", form.errors)  # ❌ ฟิลด์ `age` ต้องมี error
        self.assertIn("weight", form.errors)  # ❌ ฟิลด์ `weight` ต้องมี error
        self.assertIn("price", form.errors)  # ❌ ฟิลด์ `price` ต้องมี error

    def test_cow_form_invalid_age(self):
        """❌ ทดสอบว่าฟอร์มแจ้งเตือนเมื่ออายุน้อยกว่า 0"""
        form = CowForm(data={
            "name": "Brownie",
            "breed": "Jersey",
            "age": -1,  # ❌ อายุไม่สามารถติดลบได้
            "weight": 500.0,
            "price": 1500.00
        })
        self.assertFalse(form.is_valid())  # ❌ ต้องไม่ผ่าน validation
        self.assertIn("age", form.errors)  # ❌ ต้องมี error เรื่องอายุ

    def test_cow_form_invalid_price(self):
        """❌ ทดสอบว่าฟอร์มแจ้งเตือนเมื่อราคาไม่ถูกต้อง"""
        form = CowForm(data={
            "name": "Brownie",
            "breed": "Jersey",
            "age": 3,
            "weight": 500.0,
            "price": "not_a_number"  # ❌ ราคาต้องเป็นตัวเลข
        })
        self.assertFalse(form.is_valid())  # ❌ ต้องไม่ผ่าน validation
        self.assertIn("price", form.errors)  # ❌ ต้องมี error เรื่องราคา
