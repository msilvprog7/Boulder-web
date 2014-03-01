from django.shortcuts import render
from django.views.generic import TemplateView, View

from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

class Home (TemplateView):
	template_name="controls/index.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('/boulder/home/')
		return super(Home, self).dispatch(request, *args, **kwargs)

class Login(View):
	def post(self, request, *args, **kwargs):
		if not ('username' in request.POST and 'password' in request.POST):
			messages.error(request, "You need a username and password.")
			return redirect('/')
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/boulder/home/')
				# Redirect to a success page.
			else:
				messages.error(request, "That account is disabled.")
				return redirect('/')
				# Return a 'disabled account' error message
		else:
			messages.error(request, "Incorrect username or password.")
			return redirect('/')

class Register(TemplateView):
	def post(self, request, *args, **kwargs):
		if not ('username' in request.POST and 'password' in request.POST and 'confirm_password' in request.POST and 'full_name' in request.POST):
			messages.error(request, "You've forgotten a field.")
			return redirect('/')
		if not (request.POST['password'] == request.POST['confirm_password']):
			messages.error(request, "You're passwords don't match.")
			return redirect('/')
		user = User.objects.create_user(request.POST['username'], request.POST['username'], request.POST['password'])
		user.first_name = request.POST['full_name']
		user.save()
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		login(request, user)
		return redirect('/boulder/home/')