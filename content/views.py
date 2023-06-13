from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# custom imports
from .models import Subscriber, Post, Client


def get_client_ip(request):
    """
    Returns client's IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
    else: ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    posts = Post.objects.all()
    recent_posts = Post.recent()
    
    context = {
        "posts": posts,
        "recent_posts": recent_posts,
        "Post": Post
    }
    return render(request, "content/index.html", context)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    
    # Get the client's IP address and user agent
    client_ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    
    # print(client_ip, user_agent)
    
    # check if client already viewed the post
    client, created = Client.objects.get_or_create(
        ip_address=client_ip,
        user_agent=user_agent
    )
    
    # increment view count if client has not viewed the post
    if created: post.views.add(client)
    
    return HttpResponse("Hello world")


def subscribe_to_newsletter(request):
    """
    Subscriber newsletter subscription handler
    """
    if request.method == "POST":
        email = request.POST.get("email")

        Subscriber.objects.get_or_create(email=email)

    return redirect(request.META.get("HTTP_REFERER", "content:index"))


def unsubscribe_to_newsletter(request):
    """
    Subscriber newsletter unsubscription page view
    """

    if request.method == "POST":
        email = request.POST.get("email")

        subscriber = get_object_or_404(Subscriber, email=email)
        # delete instance
        subscriber.delete()

        return HttpResponse("Unsubscription successful!")

    return render(request, "content/unsubscribe.html")
