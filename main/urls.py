from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required

import main.api as api
import main.web as web

urlpatterns = patterns('',
	url(r'^dash/', login_required(web.Dashboard.as_view())),

	# API ENDPONINTS
	url(r'^api/token/', api.GetToken.as_view()),
	url(r'^api/log/', api.LogActivity.as_view()),
	url(r'^api/view/', api.ViewProfile.as_view()),
	url(r'^api/cookieTest/', "api.cookieTest"),

	url(r'^search/', login_required(web.Search.as_view())),
	url(r'^(?P<user_id>\d+)/\w+\.+\w+/', login_required(web.Profile.as_view())),
)
