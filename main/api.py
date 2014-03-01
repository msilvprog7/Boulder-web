import json
from django.http import HttpResponse
from django.views.generic import View

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

class GetToken(JSONGetView):
	def handle(self, object):
		return {"asdf": "boo"}