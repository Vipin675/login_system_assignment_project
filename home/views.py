from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        return render(request, 'index/index.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("--------------------------------", username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")
        else:
            # No backend authenticated the credentials
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(
                request, "Password and Confirm password must be same")

        if User.objects.filter(username=username):
            messages.error(request, "Username is already exists!")
            redirect("/login")

        if User.objects.filter(email=email):
            messages.error(request, "Email is already exists!")
            redirect("/login")

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()

        messages.success(request, "Your account has been succefully created.")
        return redirect("/login")

    return render(request, "register/register.html")
