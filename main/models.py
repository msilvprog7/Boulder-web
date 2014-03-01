from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Activity(models.Model):
	""" Activity stored in the database to associate with specific motions
		with the pebble
	"""
	name = models.CharField(max_length=255)
	points = models.IntegerField(default=0)
	description = models.TextField()

	@staticmethod
	def getUserPoints(user_id, activity_id=-1):
		""" Returns the number of points earned by the user for each CompletedActivity
		"""
		completed_activities = CompletedActivity.objects.filter(user=user_id)

		if activity_id >= 0:
			completed_activities = completed_activities.filter(activity=activity_id)

		sum = 0
		for current_activity in completed_activities:
			sum += Activity.objects.get(id=current_activity.activity_id).points

		return sum

	def getActivityUserPoints(self, user_id):
		""" Returns number of points earned by the user for the current activity
		"""
		return Activity.getUserPoints(user_id, self.id)



class CompletedActivity(models.Model):
	""" CompletedActivity in the database for every entry made by the users
	"""
	activity = models.ForeignKey(Activity)
	user = models.ForeignKey(User)
	time = models.TimeField(auto_now_add=True)


class UserProfile(models.Model):
	""" UserProfile for every user - connects a user with the secure_token created for them.
	"""
	user = models.ForeignKey(User)
	secure_token = models.CharField(max_length=255)


class FriendsRecord(models.Model):
	""" FriendsRecord to determine whether or not someone has a pending friend request and
		which users are friends.
	"""
	user1 = models.ForeignKey(User, related_name="friends_set")
	user2 = models.ForeignKey(User, related_name="friend_request_set")
	accepted = models.BooleanField(default=False)