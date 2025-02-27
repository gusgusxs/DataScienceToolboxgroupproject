from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models  # ✅ Import models เพื่อใช้ models.Q
from .models import ChatMessage, User  # ✅ Import Models ที่เกี่ยวข้อง
from django.db.models import Q

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=other_user
    ) | ChatMessage.objects.filter(
        sender=other_user, receiver=request.user
    )
    messages = messages.order_by("timestamp")  # เรียงตามเวลาส่งข้อความ

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=message_text
            )
            return redirect('chat', user_id=other_user.id)  # รีเฟรชหน้าแชทหลังส่งข้อความ

    return render(request, 'chat/chat_room.html', {
        'other_user': other_user,
        'messages': messages
    })

@login_required
def chat_list(request):
    # ดึงแชทที่ส่งมาหาผู้ขาย (ผู้ใช้งานปัจจุบันเป็นคนรับ)
    messages = ChatMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    
    return render(request, "chat/chat_list.html", {"messages": messages})
