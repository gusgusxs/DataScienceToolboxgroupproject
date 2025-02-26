from django.shortcuts import render, redirect
from .models import FarmProfile
from .forms import FarmProfileForm
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
def farm_profile_view(request):
    farm, created = FarmProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = FarmProfileForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            return redirect("home")  # ✅ หลังจากบันทึกเสร็จให้กลับไปหน้า Main
    else:
        form = FarmProfileForm(instance=farm)
    return render(request, "users/farm_profile.html", {"form": form})