import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

# User object
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx")
        ]

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post model
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=1500, unique=True)
    slug = models.SlugField(max_length=2000, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    body = RichTextField(config_name='awesome_ckeditor')
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        limit_choices_to={
            "is_staff": True,
            "is_superuser": True
        }
    )
    published = models.BooleanField(default=False)
    notified = models.BooleanField(default=False, editable=False)
    views = models.ManyToManyField("Client", blank=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "blog_post"
        get_latest_by = ("-date_created",)
        ordering = ("-date_created",)
        indexes = [
            models.Index(fields=["title", "body", "slug", "tag"])
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # create post slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("content:post_detail", kwargs={"post_slug": self.slug})
    
    @property
    def views_(self):
        return self.views.count()
    
    @classmethod
    def popular(cls):
        return cls.objects.order_by("-views")[:10]
    
    @classmethod
    def recent(cls):
        return cls.objects.order_by("-date_created")[:4]

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    """
    Newsletter subscriber model
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Client(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500)

    class Meta:
        unique_together = ('ip_address', 'user_agent')
        indexes = [
            models.Index(fields=['ip_address', 'user_agent'])
        ]
    
    def __str__(self):
        return self.ip_address

