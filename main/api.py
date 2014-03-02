import json
from django.http import HttpResponse
from django.views.generic import View

from django.views.decorators.csrf import csrf_exempt

from main.models import PebbleToken

class JSONPostView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(JSONPostView, self).dispatch(*args, **kwargs)

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
	# Input: {"id": "mypebbleid"}
	# Output: {"token": "P23ASD", "error": 0}
	def handle(self, obj):
		return {"token": PebbleToken.getFreshToken(obj.id), "error": 0}

class LogActivity(JSONPostView):
	# Input: {"activity": "Jumping Jack", "token": "P35"}
	# Output: {"error": 0}
	def handle(self, obj):
		return {"error": 0}

class ViewProfile(JSONPostView):
	# Input: {"token": "P35"}
	# Output: {"reps": 0, "name": "Hunter Leath", "error": 0}
	def handle(self, obj):
		return {"reps": 0, "name": "Hunter Leath", "error": 0}