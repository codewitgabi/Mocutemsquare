from django.urls import path
from . import views


app_name = "content"
urlpatterns = [
	path("post/<slug:post_slug>/", views.post_detail, name="post_detail"),
]
