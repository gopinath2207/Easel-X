from django.shortcuts import render, redirect
from Authentication.models import User
from django.http import HttpResponse
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, user_logged_in

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/core/')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.profile_created)
            print(user.role)
            if user.role == 'artist' and user.profile_created == 0:
                return redirect('artist:create_artist_profile')
            return redirect('/core/')  # Redirect to a success page.
        else:
            return render(request, "login_page.html", {"error": "Invalid credentials"})
    return render(request, 'login_page.html')

def signup_view(request):

    if request.method == "POST":
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        role = request.POST.get("role")
        mobile = request.POST.get("mobile")
        dob = request.POST.get("dob")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")


        if password != confirm_password:
            return render(request, "signup_page.html", {"error": "Passwords do not match"})
        
        if not username or not password or not email or not dob or not first_name or not last_name or not role:
            return render(request, "signup_page.html", {"error": "All fields are required"})

        if User.objects.filter(username=username).exists():
            return render(request, "signup_page.html", {"error": "Username already exists"})
        
        if User.objects.filter(email=email).exists():
            return render(request, "signup_page.html", {"error": "Email already registered"})
        

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, role=role, phone=mobile, dob=dob)
        user.save()
        return redirect('/')  
    return render(request, "signup_page.html")

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('/')