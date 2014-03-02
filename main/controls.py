from django.shortcuts import render
from django.views.generic import TemplateView, View

from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic.edit import FormView
from django import forms

from main.models import PebbleToken

# Create your views here.

class Home (TemplateView):
	template_name="controls/index.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('/boulder/dash/')
		return super(Home, self).dispatch(request, *args, **kwargs)

class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect('/')

class Login(View):
	def post(self, request, *args, **kwargs):
		if not ('username' in request.POST and 'password' in request.POST):
			messages.error(request, "You need a username and password.")
			return redirect('/')
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('/boulder/dash/')
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
		return redirect('/boulder/dash/')

class TokenForm(forms.Form):
	token = forms.CharField()

class RegisterToken(FormView):
	template_name = "controls/token.html"
	form_class = TokenForm
	success_url = "/boulder/dash/"

	def form_valid(self, form):
		p = PebbleToken.objects.get(token=form.cleaned_data['token'], user=None)
		p.linkUser(self.request.user)
		messages.info(self.request, "Successfully linked your Pebble.")
		return super(RegisterToken, self).form_valid(form)