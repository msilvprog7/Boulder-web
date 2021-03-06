from django.conf.urls import patterns, include, url

from django.contrib import admin
from main import controls

from django.contrib.auth.decorators import login_required

from boulder import settings

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', controls.Home.as_view()),

	url(r'^login/', controls.Login.as_view()),
	url(r'^logout/', controls.Logout.as_view()),
	url(r'^register/', controls.Register.as_view()),

	url(r'^pebble/', login_required(controls.RegisterToken.as_view())),

	# url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	
	url(r'^boulder/', include('main.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
