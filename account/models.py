import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import cloudinary.uploader


class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	avatar = models.ImageField(upload_to="avatar", default="avatar.jpg")
	avatar_url = models.URLField(
		max_length=2048,
		editable=False,
		default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-uPy9lZuIjzqW0aACiqVpVRFQqP3mpf54Fw&s")
	
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["username"]
	
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.avatar:
			response = cloudinary.uploader.upload(self.avatar.path) # upload post thumbnail to cloudinary
			self.avatar_url = response["secure_url"] # create post thumbnail_url
			print(response["secure_url"])
			# resave
			super().save(*args, **kwargs)
	
	def __str__(self):
		return self.username

