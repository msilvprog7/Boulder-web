from django.conf.urls import patterns, include, url

from django.contrib import admin
from main import controls

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', controls.Home.as_view()),
	url(r'^login/', controls.Login.as_view()),
	url(r'^register/', controls.Register.as_view()),
	url(r'^pebble/', controls.RegisterToken.as_view()),

	url(r'^boulder/', include('main.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
