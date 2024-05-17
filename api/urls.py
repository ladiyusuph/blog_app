from django.urls import path
from .views import (
    CreatePostAPIView,
    ListPostAPIView,
    DetailPostAPIView,
    CreateCommentAPIView,
    ListCommentAPIView,
    DetailCommentAPIView,
    MyTokenObtainPairView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", ListPostAPIView.as_view(), name="list_post"),
    path("create/", CreatePostAPIView.as_view(), name="api_create_post"),
    path("<str:slug>/", DetailPostAPIView.as_view(), name="post_detail"),
    path("<str:slug>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path(
        "<str:slug>/comment/create/",
        CreateCommentAPIView.as_view(),
        name="create_comment",
    ),
    path(
        "<str:slug>/comment/<int:id>/",
        DetailCommentAPIView.as_view(),
        name="comment_detail",
    ),
]
