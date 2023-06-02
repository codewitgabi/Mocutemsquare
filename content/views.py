from django.shortcuts import render
from django.http import HttpResponse


def post_detail(request, post_slug):
	return HttpResponse("Hello world")

