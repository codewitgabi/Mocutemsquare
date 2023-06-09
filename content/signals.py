from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Post, Subscriber
from django.utils.html import strip_tags


@receiver(post_save, sender=Post)
def send_subscriber_post_update(sender, instance, created, **kwargs):
	if instance.published and not instance.notified:
		# send email
		subject = "New Post Update"
		context = {
			"post_url": "http://localhost:8000" + instance.get_absolute_url(),
			"post": instance,
			"unsubscribe_url": "http://localhost:8000/unsubscribe/",
		}
		email_content = render_to_string("content/newsletter.html", context)
		
		text_content = strip_tags(email_content)
		
		email = EmailMultiAlternatives(
			subject,
			text_content,
			to=[subscriber for subscriber in Subscriber.objects.all()]
		)
		email.attach_alternative(email_content, "text/html")
		
		email.fail_silently = False
		email.send()
		
		instance.notified = True
		instance.save()

