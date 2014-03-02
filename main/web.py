from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import Http404
import random

from main.models import Activity, CompletedActivity, FriendsRecord, Suggestion, NewsfeedItem
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

		context["suggestions"] = []
		suggestionSeq = []
		while len(suggestionSeq) < len(Suggestion.objects.all()) and len(suggestionSeq) < 5:
			randInt = random.randrange(1, len(Suggestion.objects.all()) + 1)
			if randInt not in suggestionSeq:
				suggestionSeq.append(randInt)
				context["suggestions"].append(Suggestion.objects.get(id=randInt))

		context["news_items"] = sorted([item for subset in NewsfeedItem.getItems(FriendsRecord.getFriends(self.request.user.id)) for item in subset], key=lambda news_item: news_item.time, reverse=True)[:5]

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
		elif not User.objects.filter(id=int(kwargs["user_id"])):
			raise Http404

		if request.method == "POST":
			if request.POST["type"] == "add":
				FriendsRecord.createPendingRequest(request.user, User.objects.get(id=int(kwargs["user_id"])))
			elif request.POST["type"] == "accept":
				FriendsRecord.objects.get(user1=User.objects.get(id=int(kwargs["user_id"])), user2=request.user, accepted=False).acceptFriendRequest()
			elif request.POST["type"] == "remove":
				FriendsRecord.removeFriendRecords(request.user, User.objects.get(id=int(kwargs["user_id"])))

			return redirect("/boulder/" + kwargs["user_id"] + "/" + '.'.join(User.objects.get(id=int(kwargs["user_id"])).first_name.lower().split()))

		
		return super(Profile, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(Profile, self).get_context_data(**kwargs)

		context["user_info"] = User.objects.get(id=int(kwargs["user_id"]))
		context["reps"] = Activity.getUserPoints(int(kwargs["user_id"]))
		context["recent_reps"] = CompletedActivity.objects.filter(user_id=kwargs["user_id"]).order_by("-time")[:5]
		context["friends"] = FriendsRecord.getFriends(int(kwargs["user_id"]))
		context["your_friends"] = len(FriendsRecord.getFriends(self.request.user.id).filter(user2=User.objects.get(id=int(kwargs["user_id"])))) > 0
		context["pending_friends"] = len(FriendsRecord.getFriendRequests(self.request.user.id).filter(user1=User.objects.get(id=int(kwargs["user_id"])), accepted=False)) > 0
		context["you_requested"] = len(FriendsRecord.getFriendRequests(int(kwargs["user_id"])).filter(user1=self.request.user, accepted=False)) > 0

		return context
