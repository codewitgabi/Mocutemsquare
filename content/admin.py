from django.contrib import admin
from .models import Tag, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("id", "tag", "title", "author", "date_created")

