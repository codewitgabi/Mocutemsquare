# Generated by Django 3.2 on 2023-06-14 00:44

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=1500, unique=True)),
                ('slug', models.SlugField(editable=False, max_length=2000)),
                ('thumbnail', models.ImageField(upload_to='')),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.BooleanField(default=False)),
                ('notified', models.BooleanField(default=False, editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'blog_post',
                'ordering': ('-date_created',),
                'get_latest_by': ('-date_created',),
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='name_idx'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(limit_choices_to={'is_staff': True, 'is_superuser': True}, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.ManyToManyField(blank=True, editable=False, to='content.Client'),
        ),
        migrations.AddIndex(
            model_name='client',
            index=models.Index(fields=['ip_address', 'user_agent'], name='content_cli_ip_addr_882fe6_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('ip_address', 'user_agent')},
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['title', 'body', 'slug', 'tag'], name='blog_post_title_d11c19_idx'),
        ),
    ]
