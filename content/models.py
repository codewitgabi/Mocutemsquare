import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import cloudinary.uploader
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
	thumbnail = models.ImageField(upload_to="thumbnail")
	thumbnail_url = models.URLField(max_length=2048, editable=False)
	body = RichTextField(config_name='awesome_ckeditor')
	author = models.ForeignKey(
		User,
		on_delete=models.DO_NOTHING,
		limit_choices_to={
			"is_staff": True,
			"is_superuser": True
		}
	)
	date_created = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = "blog_post"
		get_latest_by = ("-date_created",)
		ordering = ("-date_created",)
		indexes = [
			models.Index(fields=["title", "body", "slug", "tag"])
		]
	
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title) # create post slug
		super().save(*args, **kwargs)
		response = cloudinary.uploader.upload(self.thumbnail.path) # upload post thumbnail to cloudinary
		self.thumbnail_url = response["secure_url"] # create post thumbnail_url
		print(response["secure_url"])
		# resave
		super().save(*args, **kwargs)
	
	def __str__(self):
		return self.title

