import json
from django.http import HttpResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from main.models import PebbleToken, Activity, CompletedActivity

from clfMath.features import *

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
			return {"error": str(e)}

class LogActivity(JSONPostView):
	# Input: {"activity": "Jumping Jack", "token": "P35"}
	# Output: {"error": 0}
	def handle(self, obj):
		try:
			dWindow = DataWindow()
			clf = train()
			dWindow.setClf(clf)
			dWindow.current_window = self.request.session.get('current_window', [])
			dWindow.next_window = self.request.session.get('next_window', [])

			for x in obj["data"]:
				dWindow.push((x["x"], x["y"], x["z"], x["time"], 1))

			# print len(dWindow.current_window), len(dWindow.next_window)

			activity = dWindow.predict()

			self.request.session['current_window'] = dWindow.current_window
			self.request.session['next_window'] = dWindow.next_window

			if activity[0] > 0:
				# print "Got Activity", str(activity[0])
				u = PebbleToken.getUser(obj["token"], obj["id"])
				a = Activity.activityFromClfId(int(activity[0]))
				CompletedActivity.logActivityForUser(u, a)

			return {"activity": str(activity), "error": 0}
		except Exception as e:
			return {"error": str(e)}

class ViewProfile(JSONPostView):
	# Input: {"token": "P35", "id": "mypebbleid"}
	# Output: {"level": 0, "name": "Hunter Leath", "error": 0}
	def handle(self, obj):
		try:
			u = PebbleToken.getUser(obj["token"], obj["id"])
			return {"level": Activity.getLevel(u.id), "username": u.first_name, "error": 0}
		except Exception as e:
			return {"error": str(e)}

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