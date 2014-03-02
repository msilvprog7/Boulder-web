from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Activity, CompletedActivity, FriendsRecord


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