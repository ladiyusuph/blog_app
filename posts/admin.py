from django.contrib import admin
from .models import Post, Comment, Topic


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_active", "updated"]
    list_filter = ["author", "updated", "is_active"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Topic)
