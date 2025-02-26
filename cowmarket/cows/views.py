from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django.conf import settings
from .forms import CowForm
from .models import *
from .serializers import CowSerializer

class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer

def community_view(request):
    cows = Cow.objects.all()  # ดึงลูกวัวทั้งหมดจากระบบ
    return render(request, "community/cow_list.html", {"cows": cows})

# แสดงรายละเอียดลูกวัวที่เลือก
def cow_detail_view(request, cow_id):
    cow = get_object_or_404(Cow, id=cow_id)
    return render(request, "community/cow_detail.html", {"cow": cow})

@login_required
def cow_list(request):
    cows = Cow.objects.all()  # ✅ ดึงข้อมูลลูกวัวทั้งหมด
    return render(request, "cows/cow_list.html", {"cows": cows, "MEDIA_URL": settings.MEDIA_URL})

@login_required
def cow_create(request):
    if request.method == "POST":
        form = CowForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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