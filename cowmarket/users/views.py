from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from cows.models import Notification
from django.contrib.auth.decorators import login_required

def login_view(request):
    """แสดงหน้า Login"""
    return render(request, "users/login.html")

def google_login_redirect(request):
    """Redirect ไปหน้า Google OAuth"""
    return redirect("/accounts/google/login/")

@login_required  
def main_view(request):
    user = request.user  
    return render(request, "users/home.html", {"user": user})  

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = UserProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {"form": form})

import plotly.express as px
import plotly.io as pio
from django.shortcuts import render
from cows.models import Cow
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    # ดึงข้อมูลวัวของผู้ใช้ที่ล็อกอิน
    available_count = Cow.objects.filter(transaction_status="available", owner=request.user).count()
    pending_count = Cow.objects.filter(transaction_status="pending", owner=request.user).count()
    sold_count = Cow.objects.filter(transaction_status="sold", owner=request.user).count()

    # สร้าง Pie Chart สำหรับสถานะการขายวัว
    labels = ["พร้อมขาย", "รอการยืนยัน", "ขายสำเร็จ"]
    values = [available_count, pending_count, sold_count]

    fig_pie = px.pie(
        names=labels,
        values=values,
        title="📊 สถานะการขายวัวของฉัน",
        color=labels,
        color_discrete_map={"พร้อมขาย": "green", "รอการยืนยัน": "orange", "ขายสำเร็จ": "red"}
    )

    # แปลงกราฟเป็น HTML
    chart_pie_html = pio.to_html(fig_pie, full_html=False)

    # ดึงข้อมูลจำนวนวัวทั้งหมดที่ผู้ใช้มี
    total_cows = Cow.objects.filter(owner=request.user).count()
    total_labels = ['จำนวนวัวทั้งหมด']
    total_values = [total_cows]

    fig_total = px.bar(
        x=total_labels,
        y=total_values,
        title="📊 จำนวนวัวทั้งหมดที่คุณมี",
        labels={'x': 'ประเภท', 'y': 'จำนวน'},
        color=total_labels,
        color_discrete_map={"จำนวนวัวทั้งหมด": "blue"}
    )

    # แปลงกราฟเป็น HTML
    chart_total_html = pio.to_html(fig_total, full_html=False)

    # ดึงข้อมูลยอดวิวของแต่ละวัว
    cows = Cow.objects.filter(owner=request.user)
    cow_names = [cow.name for cow in cows]
    view_counts = [cow.view_count for cow in cows]

    # สร้างกราฟ Bar Chart สำหรับยอดวิวของวัวทั้งหมด
    fig_view = px.bar(
        x=cow_names,  # แก้ไขให้ 'x' เป็นชื่อของวัว
        y=view_counts,  # 'y' เป็นยอดวิว
        title="📊 ยอดวิวของวัวทั้งหมดที่คุณมี",
        labels={'x': 'วัว', 'y': 'ยอดวิว'},
        color=cow_names,  # ให้ใช้ชื่อวัวเป็นสีของแต่ละบาร์
        color_discrete_map={name: "blue" for name in cow_names}  # เปลี่ยนสีแต่ละบาร์
    )

    # แปลงกราฟเป็น HTML
    chart_view_html = pio.to_html(fig_view, full_html=False)

    return render(request, "users/profile.html", {
        "chart_pie": chart_pie_html,
        "chart_total": chart_total_html,
        "chart_view": chart_view_html  # ส่งกราฟยอดวิวไปยังหน้า profile
    })


def main_view(request):
    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, "users/home.html", {"unread_notifications": unread_notifications})

from django.shortcuts import render, get_object_or_404
from cows.models import Cow
from django.contrib.auth.decorators import login_required

@login_required
def cow_detail_view(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)
    
    # เพิ่มยอดวิวเมื่อผู้ใช้ดูรายละเอียด
    if request.method == "POST":
        cow.view_count += 1
        cow.save()  # บันทึกการเปลี่ยนแปลงยอดวิว

    return render(request, "community/cow_detail.html", {"cow": cow})
