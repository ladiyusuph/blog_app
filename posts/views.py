from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Post, Topic
from .forms import PostForm, CommentForm, SharePostForm
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json


def list_posts(request):
    q = request.GET.get("q") if request.GET.get("q") else ""
    topics = Topic.objects.all()[0:4]
    post_list = Post.active_manager.filter(
        Q(topic__name__icontains=q) | Q(title__icontains=q) | Q(body__icontains=q)
    )
    topics = Topic.objects.all()[:5]
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)
    context = {"posts": posts, "topics": topics}
    return render(request, "posts/post_list.html", context=context)


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post).order_by("-updated")
    topics = Topic.objects.all()
    msg = False

    if request.user.is_authenticated:
        user = request.user

        if post.likes.filter(id=user.id).exists():
            msg = True
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.comment_author = request.user
            new_comment.save()
            return redirect("post_detail", slug=post.slug)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "topics": topics,
        "msg": msg,
        "form": form,
        # "new_comment": new_comment,
    }
    return render(
        request,
        "posts/post_detail.html",
        context=context,
    )


@login_required(login_url="account_login")
def create_post(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Post.objects.create(
            author=request.user,
            topic=topic,
            title=request.POST.get("title"),
            body=request.POST.get("body"),
            thumbnail=request.FILES.get("thumbnail"),
        )
        return redirect("posts")
    context = {"form": form, "topics": topics}
    return render(request, "posts/create_post.html", context=context)


@login_required(login_url="account_login")
def update_post(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)
    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST, files=request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.save()
            return redirect("post_detail", post.slug)
    context = {"form": form}
    return render(request, "posts/create_post.html", context=context)


@login_required(login_url="account_login")
def delete_post(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    post.delete()

    return redirect("posts")


# @login_required(login_url="account_login")
def like_post(request, slug=None):
    # data = json.loads(request.body)
    # id = data["id"]
    post = Post.objects.get(slug=slug)
    # checker = None

    if request.user.is_authenticated:

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0

        else:
            post.likes.add(request.user)
            checker = 1

    likes = post.likes.count()

    info = {"check": checker, "num_of_likes": likes}

    return redirect("post_detail", post.slug)


# @login_required(login_url="account_login")
# def create_comment(request, pk=None):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.comment_author = request.user
#             comment.save()
#             return redirect("post_detail", slug=post.slug)
#     else:
#         form = CommentForm()
#     context = {"form": form, "post": post}
#     return render(request, "posts/create_comment.html", context=context)


@login_required(login_url="account_login")
def delete_comment(request, pk=None):
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    comment.delete()

    return redirect("post_detail", post_slug)


@login_required(login_url="account_login")
def update_comment(request, pk=None):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = comment.post
            comment.comment_author = request.user
            comment.save()
            return redirect("post_detail", slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    context = {"form": form, "comment": comment}
    return render(request, "posts/create_comment.html", context=context)


@login_required(login_url="account_login")
def share_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = SharePostForm()
    sent = False
    if request.method == "POST":
        form = SharePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}'s comments: {cd['comment']}"
            send_mail(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    context = {"form": form, "post": post, "sent": sent}
    return render(request, "posts/share_post.html", context=context)
