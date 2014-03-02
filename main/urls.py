from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import main.api as api

urlpatterns = patterns('',
	url(r'^home/', TemplateView.as_view(template_name="home.html")),

	# API ENDPONINTS
	url(r'^api/token/', api.GetToken.as_view()),
	url(r'^api/log/', api.LogActivity.as_view()),
	url(r'^api/view/', api.ViewProfile.as_view()),
)
