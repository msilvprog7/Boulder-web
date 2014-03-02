from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import main.api as api
import main.web as web

urlpatterns = patterns('',
	url(r'^home/', web.Dashboard.as_view()),

	# API ENDPONINTS
	url(r'^api/token/', api.GetToken.as_view()),
	url(r'^api/log/', api.LogActivity.as_view()),
	url(r'^api/view/', api.ViewProfile.as_view()),
)
