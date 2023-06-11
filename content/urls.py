from django.urls import path
from . import views


app_name = "content"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:post_slug>/", views.post_detail, name="post_detail"),
    path("subscribe/",
         views.subscribe_to_newsletter,
         name="subscribe"
         ),
    path("unsubscribe/",
         views.unsubscribe_to_newsletter,
         name="unsubscribe"
         ),
]
