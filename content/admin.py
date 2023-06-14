from django.contrib import admin
from .models import Tag, Post, Subscriber, Client, Feedback


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "tag", "title", "author", "date_created", "views_")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "date_created")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent')


