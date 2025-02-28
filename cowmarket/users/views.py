from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from cows.models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    """แสดงหน้า Login"""
    return render(request, "users/login.html")

def google_login_redirect(request):
    """Redirect ไปหน้า Google OAuth"""
    return redirect("/accounts/google/login/")

def logout_view(request):
    logout(request)
    return redirect('community')
    


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

@login_required
def profile(request):
    return render(request, "users/profile.html")

def main_view(request):
    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, "users/home.html", {"unread_notifications": unread_notifications})
