from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

# Create your views here.

class Home (TemplateView):
	template_name="controls/index.html"

class Register(View):
	pass

class Login(View):
	pass