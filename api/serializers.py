import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Post, Comment

# from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


User = get_user_model()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body", "thumbnail"]

    def validate_title(self, value):
        if len(value) > 200:
            return serializers.ValidationError("Max title length is 100 characters")
        return value

    # def validate_description(self, value):
    #     if len(value) > 200:
    #         return serializers.ValidationError(
    #             "Max description length is 200 characters"
    #         )
    #     return value

    def clean_image(self, value):
        initial_path = value.path
        new_path = settings.MEDIA_ROOT + value.name
        os.rename(initial_path, new_path)
        return value


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "url",
            "title",
            "author",
            "thumbnail",
            "slug",
            "comments",
        ]

    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj).count()
        return qs

    def get_url(self, obj):
        return obj.get_api_url()


class PostDetailSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "title",
            # "description",
            "body",
            "author",
            "thumbnail",
            "created",
            "updated",
            "comments",
        ]

    def get_slug(self, obj):
        return obj.slug

    def get_comments(self, obj):
        qs = Comment.objects.filter(post=obj)
        try:
            serializer = CommentSerializer(qs, many=True)
        except Exception as e:
            print(e)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "comment_author",
            "title",
            "body",
            "created",
            "updated",
        ]


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "title",
            "body",
        ]
