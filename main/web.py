from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import Http404

from main.models import Activity, CompletedActivity, FriendsRecord
from django.contrib.auth.models import User


# Create your views here.

class Dashboard(TemplateView):
	template_name = "main/home.html"

	def get_context_data(self, **kwargs):
		context = super(Dashboard, self).get_context_data(**kwargs)

		context["reps"] = Activity.getUserPoints(self.request.user.id)
		context["recent_reps"] = CompletedActivity.objects.filter(user_id=self.request.user.id).order_by("-time")[:5]
		context["friends"] = FriendsRecord.getFriends(self.request.user.id)
		context["pending_friends"] = FriendsRecord.getFriendRequests(self.request.user.id)


		return context



class Search(TemplateView):
	template_name = "main/search.html"

	def dispatch(self, request, *args, **kwargs):
		userSearched = User.objects.filter(email=self.request.GET["search_email"]).first()

		if userSearched != None and request.user.is_authenticated():
			return redirect("/boulder/%d/%s/" % (userSearched.id, '.'.join(userSearched.first_name.lower().split())))

		return super(Search, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Search, self).get_context_data(**kwargs)

		context["search_email"] = self.request.GET["search_email"]

		return context



class Profile(TemplateView):
	template_name = "main/profile.html"

	def dispatch(self, request, *args, **kwargs):
		
		if request.user.id == int(kwargs["user_id"]):
			return redirect("/boulder/dash/")
		elif not User.objects.filter(id=kwargs["user_id"]):
			raise Http404
		
		return super(Profile, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Profile, self).get_context_data(**kwargs)

		context["user_info"] = User.objects.get(id=kwargs["user_id"])
		context["reps"] = Activity.getUserPoints(kwargs["user_id"])
		context["recent_reps"] = CompletedActivity.objects.filter(user_id=kwargs["user_id"]).order_by("-time")[:5]
		context["friends"] = FriendsRecord.getFriends(kwargs["user_id"])
		context["your_friends"] = len(FriendsRecord.getFriends(self.request.user.id).filter(user2=User.objects.get(id=kwargs["user_id"]))) > 0

		return context
