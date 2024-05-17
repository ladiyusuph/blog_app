from django.db import models
from django.db.models.signals import pre_save

# from django.contrib.auth.models import User
from user.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


# First, define the Manager subclass.
class PostActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=False, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(
        blank=True,
    )
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name="post_likes")
    objects = models.Manager()
    active_manager = PostActiveManager()

    # comments = models.ForeignKey(
    #     Comment, on_delete=models.SET_NULL, null=True, blank=True
    # )
    class Meta:
        ordering = ["-created", "-updated"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_api_url(self):
        try:
            return reverse("post_detail", kwargs={"slug": self.slug})
        except:
            None

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(post=instance)
        return qs


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
