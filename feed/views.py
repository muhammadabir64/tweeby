from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Tweet, Comment
from account.models import Account


@login_required
def feed(request):
    data = {
        "tweets": Tweet.objects.filter(
            Q(user__in=request.user.account.user_followers.all()) |
            Q(user__user__username=request.user)).order_by("-id"),
        "otherUsers": Account.objects.filter()
        .exclude(user__account__in=request.user.account.user_followers.all())
        .exclude(user=request.user).order_by("-id")[:10]
    }
    return render(request, "feed/feed.html", data)


@login_required
def tweet_publish(request):
    if request.method == "POST":
        content = request.POST["tweet_content"]
        redirect_uri = request.POST["redirect_uri"]
        tweet = Tweet(user=request.user.account, content=content)
        tweet.save()
        if redirect_uri == "feed":
            return redirect("feed")
        else:
            return redirect("profile", username=request.user.username)


@login_required
@csrf_exempt
def tweet_remover(request, tweet, uri):
    tweet = Tweet.objects.filter(id=tweet).first()
    if request.user.account == tweet.user:
        tweet.delete()
    if uri == "feed":
        return redirect("feed")
    else:
        return redirect("profile", username=request.user.username)


@login_required
@csrf_exempt
def likes_handler(request):
    if request.method == "POST":
        tweet_id = request.POST["tweet_id"]
        user = request.user.account
        tweet = Tweet.objects.get(pk=tweet_id)
        if user in tweet.likes.all():
            tweet.remove_like(request.user.account)
            return JsonResponse({"status": 0, "total": tweet.total_likes()})
        else:
            tweet.add_like(request.user.account)
            return JsonResponse({"status": 1, "total": tweet.total_likes()})


@login_required
@csrf_exempt
def tweet_comment_publish(request):
    if request.method == "POST":
        tweet = request.POST["tweet_id"]
        content = request.POST["content"]
        user = request.user.account
        tweet = Tweet.objects.get(pk=tweet)
        comment = Comment(user=user, tweet=tweet, content=content)
        comment.save()
        tweet.add_comment(comment)
        return JsonResponse({
            "status": 0,
            "total": tweet.total_comments(),
            "user_img": user.profile_img,
            "user_full_name": user.user.first_name+" "+user.user.last_name,
            "username": user.user.username,
            "content": content,
        })