import json
from django.http import HttpResponse
from django.views.generic import View

class JSONGetView(View):
	def handle(self, object):
		pass

	def get(self, request, *args, **kwargs):
		print request.body
		return HttpResponse("asdf")

class GetToken(JSONGetView):
	pass