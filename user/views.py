from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from posts.models import Post, Topic, Comment
from .models import User, Follow
from .forms import UserForm


# @login_required(login_url="account_login")
def user_profile(request, pk):
    user = get_object_or_404(User, id=pk)
    user_posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(comment_author=user)
    topics = Topic.objects.all()  # You need to import Topic model for this to work
    follower_count = len(Follow.objects.filter(following=user))
    following_count = len(Follow.objects.filter(follower=user))
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    context = {
        "profile_user": user,  # Renaming to avoid conflict with "user" used for the request
        "user_posts": user_posts,  # Renamed for clarity
        "comments": comments,
        "topics": topics,
        "is_following": is_following,
        "following": following_count,
        "followers": follower_count,
    }
    return render(request, "user/profile.html", context)


@login_required(login_url="account_login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect("user_profile", pk=user.id)
    return render(request, "user/update_user.html", {"form": form})


@login_required(login_url="account_login")
def follow_user(request, pk):
    user_to_follow = get_object_or_404(User, pk=pk)
    if not request.user.following.filter(pk=pk).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect("user_profile", user_to_follow.id)


@login_required(login_url="account_login")
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(User, pk=pk)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    # request.user.following.filter(pk=pk).delete()
    return redirect("user_profile", user_to_unfollow.id)


# https://medium.com/@abdullafajal/step-by-step-guide-to-implement-follow-unfollow-functionality-in-django-f98dd501aa36
