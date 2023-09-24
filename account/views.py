from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm
from .models import Account
from feed.models import Tweet
from django.core import serializers
import re


def register(request):
    if request.user.is_authenticated:
        return redirect("feed")
        
    if request.method == "POST":
        form = RegisterForm(request.POST)
        flag = request.POST["flag"]
        country = request.POST["city"]
        city = request.POST["city"]
        if form.is_valid():
            user = form.save()
            account = Account.objects.filter(user=user).first()
            account.flag = flag
            account.country = country
            account.city = city
            account.save()
            messages.success(request, f"Welcome <strong>{request.POST['username']}</strong>, your account has created successfully. please login to continue...")
            return redirect("login")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("register")
    return render(request, "account/register.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("feed")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("feed")
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")

    return render(request, "account/login.html")


@login_required
def logout_page(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect("login")


@login_required
def profile(request, username):
    data = {
        "tweets": Tweet.objects.filter(user__user__username=username).order_by("-id"),
        "userData": Account.objects.get(user__username=username),
        "otherUsers": Account.objects.filter()
        .exclude(user__account__in=request.user.account.user_followers.all())
        .exclude(user=request.user).order_by("-id")[:10]
    }
    return render(request, "account/profile.html", data)


@login_required
@csrf_exempt
def follow_handler(request):
    if request.method == "POST":
        user = Account.objects.get(user__username=request.POST["user"])
        user_self = request.user.account
        if user in user_self.following.all():
            user_self.remove_following(user)
            user.remove_follower(user_self)
            return JsonResponse({"status": 0, "total": user.total_followers()})
        else:
            user_self.add_following(user)
            user.add_follower(user_self)
            return JsonResponse({"status": 1, "total": user.total_followers()})


@login_required
def following_list(request):
    data = {
        "following": Account.objects.get(user=request.user).following.all(),
        "otherUsers": Account.objects.filter()
        .exclude(user__account__in=request.user.account.user_followers.all())
        .exclude(user=request.user).order_by("-id")[:10]
    }
    return render(request, "account/following_list.html", data)


@login_required
def followers_list(request):
    data = {
        "followers": Account.objects.get(user=request.user).followers.all(),
        "otherUsers": Account.objects.filter()
        .exclude(user__account__in=request.user.account.user_followers.all())
        .exclude(user=request.user).order_by("-id")[:10]
    }
    return render(request, "account/followers_list.html", data)


@login_required
@csrf_exempt
def follower_remover(request):
    follower = Account.objects.get(id=request.POST["user_id"])
    account = request.user.account
    account.remove_follower(follower)
    follower.remove_following(account)
    return redirect("followers_list")


@login_required
@csrf_exempt
def following_remover(request):
    following = Account.objects.get(id=request.POST["user_id"])
    account = request.user.account
    account.remove_following(following)
    following.remove_follower(account)
    return redirect("following_list")


@login_required
@csrf_exempt
def nav_search_bar(request):
    results = []
    value = request.POST["value"]
    query = User.objects.filter(
            Q(username__startswith=value) | 
            Q(first_name__startswith=value) | 
            Q(last_name__startswith=value))[:10]
    if len(results) > 0:
        results.clear()
    for user in query:
        results.append({
            "name": user.first_name+" "+user.last_name,
            "username": user.username,
            "picture": user.account.profile_img
        })
    return JsonResponse({"data": results})


@login_required
def profile_edit(request):
    if request.method == "POST":
        user = User.objects.filter(pk=request.user.pk).first()
        account = Account.objects.filter(user=request.user).first()

        user.first_name = request.POST["fname"]
        user.last_name = request.POST["lname"]
        account.cover_img = request.POST["cover_img"]
        account.profile_img = request.POST["profile_img"]
        account.bio = request.POST["bio"]
        account.website = request.POST["website"]
        
        user.save()
        account.save()
    return redirect("profile", username=request.user.username)


@login_required
def account_setting_email(request):
    if request.method == "POST":
        hide_email = request.POST.get("hide_email", False)
        user = User.objects.filter(pk=request.user.pk).first()
        account = Account.objects.filter(user=request.user).first()

        user.email = request.POST["email"]
        if hide_email == "on":
            account.hide_email = True
        elif hide_email == False:
            account.hide_email = False
        
        user.save()
        account.save()
    return redirect("profile", username=request.user.username)


@login_required
@csrf_exempt
def account_setting_password(request):
    if request.method == "POST":
        password = request.POST["password"].strip()
        password1 = request.POST["password1"].strip()
        password2 = request.POST["password2"].strip()

        user = User.objects.filter(pk=request.user.pk).first()

        if bool(user.check_password(password) == False):
            return JsonResponse({"type": "error", "msg": "Old password doesn't match!"})
        elif password1 != password2:
            return JsonResponse({"type": "error", "msg": "Password & Confirm password doesn't match!"})
        elif password == password1:
            return JsonResponse({"type": "error", "msg": "Old password & New password can't be similar!"})
        elif len(password1) < 8:
            return JsonResponse({"type": "error", "msg": "Password length should be at least 8 characters long!"})
        elif bool(re.search("[0-9]", password1)) == False:
            return JsonResponse({"type": "error", "msg": "Make sure your password has a number letter"})
        elif any(c in "!@#$%^&*()-+?_=,<>/}[{]" for c in password1) == False:
            return JsonResponse({"type": "error", "msg": "Make sure your password has a special character [@,#,$,%,&]"})
        else:
            user.set_password(password1)
            user.save()
            return JsonResponse({"type": "success", "msg": "Passoword has been changed successfully. You'll be redirect to login page..."})