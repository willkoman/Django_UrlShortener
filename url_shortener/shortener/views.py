import random
import string

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import URL


def generate_short_url():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


def register(request):
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        user.save()
        context["message"] = "User registered successfully!"
        auth_login(request, user)
        return redirect("home")

    return render(request, "register.html", context)


def login(request):
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            context["message"] = "Login failed! Please check your username and password."

    return render(request, "login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("home")


def home(request):
    context = {}

    if request.method == "POST":
        original_url = request.POST["original_url"]
        created_by = request.user.username if request.user.is_authenticated else "Anonymous"

        # Generate a unique short URL
        short_url = generate_short_url()
        while URL.objects.filter(short_url=short_url).exists():
            short_url = generate_short_url()

        url = URL(original_url=original_url, short_url=short_url, created_by=created_by)
        url.save(host_url=request.build_absolute_uri("/"))
        context["short_url"] = request.build_absolute_uri("/") + short_url

    if request.user.is_authenticated:
        urls = URL.objects.filter(created_by=request.user.username)
        context["urls"] = urls
        context["username"] = request.user.username
    else:
        urls = URL.objects.filter(created_by="Anonymous")
        context["urls"] = urls

    return render(request, "home.html", context)


def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    url.num_of_visits += 1
    url.save()
    return redirect(url.original_url)


# Requires user to be logged in
@login_required(login_url="login")
def delete_url(request, url_id):
    url = get_object_or_404(URL, pk=url_id)
    url.delete()
    return redirect("home")
