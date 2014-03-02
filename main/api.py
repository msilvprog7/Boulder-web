import json
from django.http import HttpResponse
from django.views.generic import View

from main.models import PebbleToken

class JSONPostView(View):
	def handle(self, object):
		raise ValueError

	def post(self, request, *args, **kwargs):
		obj = json.loads(request.body)
		out = self.handle(obj)
		return HttpResponse(json.dumps(out))

class JSONGetView(View):
	def handle(self):
		raise ValueError

	def get(self, request, *args, **kwargs):
		out = self.handle()
		return HttpResponse(json.dumps(out))

class GetToken(JSONPostView):
	def handle(self, obj):
		return {"token": PebbleToken.getFreshToken(obj.id)}

class LogActivity(JSONPostView):
	def handle(self, obj):
		return {"asdf": "boo"}

class ViewProfile(JSONPostView):
	def handle(self, obj):
		return {"asdf": "boo"}