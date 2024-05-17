from django.urls import path
from .views import (
    list_posts,
    post_detail,
    create_post,
    update_post,
    delete_post,
    # create_comment,
    delete_comment,
    update_comment,
    share_post,
    like_post,
)


urlpatterns = [
    path("posts/", list_posts, name="posts"),
    path("posts/<str:slug>/", post_detail, name="post_detail"),
    path("create/", create_post, name="create_post"),
    path("update/<str:slug>", update_post, name="update_post"),
    path("delete/<str:slug>", delete_post, name="delete_post"),
    # path("comment/<int:pk>", create_comment, name="create_comment"),
    path("delete-comment/<int:pk>", delete_comment, name="delete_comment"),
    path("update-comment/<int:pk>", update_comment, name="update_comment"),
    path("share/<str:slug>/", share_post, name="share_post"),
    path("like/<str:slug>/", like_post, name="like"),
]
