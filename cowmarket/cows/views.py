from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.conf import settings
from .forms import CowForm
from django.contrib import messages
from .models import *
from .serializers import CowSerializer

class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

@login_required
def community_view(request):
    cows = Cow.objects.filter(transaction_status="available")
    return render(request, "community/cow_list.html", {"cows": cows})

def cow_detail_view(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)
    return render(request, "community/cow_detail.html", {"cow": cow})

@login_required
def cow_list(request):
    cows = Cow.objects.filter(owner=request.user)  # ✅ ดึงข้อมูลลูกวัวทั้งหมด
    return render(request, "cows/cow_list.html", {"cows": cows, "MEDIA_URL": settings.MEDIA_URL})

@login_required
def cow_create(request):
    if request.method == "POST":
        form = CowForm(request.POST, request.FILES)
        if form.is_valid():
            cow = form.save(commit=False)
            cow.owner = request.user  # 🔹 ตั้งให้ owner เป็นผู้ใช้ที่ล็อกอินอยู่
            cow.save()
            return redirect("cow_list")
    else:
        form = CowForm()
    return render(request, "cows/cow_form.html", {"form": form})

@login_required
def cow_update(request, pk):
    cow = get_object_or_404(Cow, pk=pk)
    if request.method == "POST":
        form = CowForm(request.POST, request.FILES, instance=cow)
        if form.is_valid():
            form.save()
            return redirect("cow_list")
    else:
        form = CowForm(instance=cow)
    return render(request, "cows/cow_form.html", {"form": form})

@login_required
def cow_delete(request, pk):
    cow = get_object_or_404(Cow, pk=pk)
    if request.method == "POST":
        cow.delete()
        return redirect("cow_list")
    return render(request, "cows/cow_confirm_delete.html", {"cow": cow})

@login_required
def buy_cow(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)

    # ❌ ป้องกันการซื้อวัวของตัวเอง
    if cow.owner == request.user:
        messages.error(request, "⚠️ คุณไม่สามารถซื้อวัวของตัวเองได้!")
        return redirect("community")

    # ❌ ป้องกันการซื้อวัวที่กำลังขายหรือขายไปแล้ว
    if cow.transaction_status != "available":
        messages.warning(request, "⚠️ วัวตัวนี้ไม่พร้อมขาย หรือกำลังรอการยืนยันจากเจ้าของ")
        return redirect("community")

    # ✅ เปลี่ยนสถานะเป็นรอการยืนยัน
    cow.transaction_status = "pending"
    cow.buyer = request.user  # บันทึกว่าใครกดซื้อ
    cow.save()

    # ✅ แจ้งเตือนให้เจ้าของวัว
    Notification.objects.create(
        user=cow.owner,
        message=f"📢 {request.user.username} สนใจซื้อวัว {cow.name} ของคุณ กรุณายืนยันการขาย"
    )

    # ✅ แจ้งเตือนให้ผู้ซื้อว่าเขาได้ทำรายการแล้ว
    Notification.objects.create(
        user=request.user,
        message=f"✅ คุณได้ทำการสั่งซื้อวัว {cow.name} แล้ว กรุณารอเจ้าของยืนยันการขาย"
    )

    messages.success(request, "✅ ทำรายการซื้อสำเร็จ! กรุณารอเจ้าของวัวตอบรับ")
    return redirect("community")

@login_required
def confirm_transaction(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)
    
    if request.user != cow.owner:
        messages.error(request, "คุณไม่มีสิทธิ์ยืนยันการซื้อขายวัวตัวนี้")
        return redirect("cow_list")
    
    if request.method == "POST":
        status = request.POST.get("status")
        if status == "sold":
            cow.transaction_status = "sold"
            messages.success(request, "✅ ซื้อขายสำเร็จ!")
        elif status == "available":
            cow.transaction_status = "available"
            cow.buyer = None  # ลบผู้ซื้อออกไป
            messages.info(request, "❌ ซื้อขายไม่สำเร็จ! วัวกลับไปแสดงในตลาดอีกครั้ง")

        cow.save()
    
    return redirect("cow_list")

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    
    # ✅ เมื่อผู้ใช้เข้าหน้านี้ ให้ทำเครื่องหมายว่า "อ่านแล้ว"
    notifications.update(is_read=True)

    return render(request, "cows/notifications.html", {"notifications": notifications})

@login_required
def my_purchases(request):
    # ดึงรายการวัวที่ผู้ใช้ซื้อและถูกยืนยันแล้ว
    cows = Cow.objects.filter(buyer=request.user, transaction_status="sold")
    return render(request, "cows/my_purchases.html", {"cows": cows})