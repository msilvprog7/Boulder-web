import json
from django.http import HttpResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from main.models import PebbleToken

from clfMath import *

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
		try:
			return {"token": PebbleToken.getFreshToken(obj["id"]), "error": 0}
		except Exception as e:
			return {"error": e.message}

class LogActivity(JSONPostView):
	# Input: {"activity": "Jumping Jack", "token": "P35"}
	# Output: {"error": 0}
	def handle(self, obj):
		try:
			if not "data" in self.request.session:
				clf = train()
				dWindow = DataWindow()
				dWindow.setClf(clf)
				self.request.session["data"] = dWindow
			for x in obj:
				self.request.session["data"].push((x["x"], x["y"], x["z"], x["time"], 1))
			activity = self.request.session["data"].calculate()
			if activity[0] > 0:
				print "Found Activity", str(activity[0])
			return {"activity": activity[0], "error": 0}
		except Exception as e:
			return {"error": e.message}

class ViewProfile(JSONPostView):
	# Input: {"token": "P35", "id": "mypebbleid"}
	# Output: {"level": 0, "name": "Hunter Leath", "error": 0}
	def handle(self, obj):
		try:
			u = PebbleToken.getUser(obj["token"], obj["id"])
			return {"level": -1, "username": u.first_name, "error": 0}
		except Exception as e:
			return {"error": e.message}

@csrf_exempt
def cookieTest(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("Yay!")
        else:
            return HttpResponse("Cookies don't work")
    request.session.set_test_cookie()
    return HttpResponse("Call again.")