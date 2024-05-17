from django.urls import path
from .views import update_user, user_profile, follow_user, unfollow_user

urlpatterns = [
    path("profile/<int:pk>/", user_profile, name="user_profile"),
    path("update-user/", update_user, name="update_user"),
    path("follow/<int:pk>/", follow_user, name="follow_user"),
    path("unfollow/<int:pk>/", unfollow_user, name="unfollow_user"),
]
