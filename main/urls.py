from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import main.api as api

urlpatterns = patterns('',
	url(r'^home/', TemplateView.as_view(template_name="home.html")),
	url(r'^get_token/', api.GetToken.as_view()),
)
