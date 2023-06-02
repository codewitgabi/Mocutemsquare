from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Post, Subscriber


@receiver(post_save, sender=Post)
def send_subscriber_post_update(sender, instance, created, **kwargs):
	if instance.published and not instance.notified:
		# send email
		subject = "New Post Update"
		content = render_to_string("content/newsletter.html", {
			"post_link": "http://localhost:8000" + instance.get_absolute_url(),
		})
		
		msg = EmailMessage(
			subject,
			content,
			to=[subscriber for subscriber in Subscriber.objects.all()]
		)
		msg.content_subtype = "html"
		msg.fail_silently = False
		msg.send()
		
		instance.notified = True
		instance.save()

