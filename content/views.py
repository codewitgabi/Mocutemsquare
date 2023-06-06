from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# custom imports
from .models import Subscriber


def post_detail(request, post_slug):
	return HttpResponse("Hello world")


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

