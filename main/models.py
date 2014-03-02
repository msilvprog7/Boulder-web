from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

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
			sum += Activity.objects.get(id=current_activity.activity_id).points * current_activity.number

		return sum

	def getActivityUserPoints(self, user_id):
		""" Returns number of points earned by the user for the current activity
		"""
		return Activity.getUserPoints(user_id, self.id)


class CompletedActivity(models.Model):
	""" CompletedActivity in the database for every entry made by the users
	"""
	activity = models.ForeignKey(Activity)
	number = models.IntegerField(default=1)
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)

	def getPoints(self):
		""" Get points for the current CompletedActivity
		"""
		return self.number * Activity.objects.get(id=self.activity_id).points



class FriendsRecord(models.Model):
	""" FriendsRecord to determine whether or not someone has a pending friend request and
		which users are friends.
	"""
	user1 = models.ForeignKey(User, related_name="friends_set")
	user2 = models.ForeignKey(User, related_name="friend_request_set")
	accepted = models.BooleanField(default=False)


	@staticmethod
	def getFriends(user_id):
		""" Get a set of friends for the given user_id
		"""
		return FriendsRecord.objects.filter(user1_id=user_id, accepted=True)

	@staticmethod
	def getFriendRequests(user_id):
		""" Get a set of pending friend requests for the given user_id
		"""
		return FriendsRecord.objects.filter(user2_id=user_id, accepted=False)

	@staticmethod
	def createPendingRequest(user1, user2):
		""" Create a pending request from user1 to user2
		"""
		new_friends_record = FriendsRecord(user1=user1, user2=user2, accepted=False)
		new_friends_record.save()

	@staticmethod
	def removeFriendRecords(user1, user2):
		""" Remove FriendRecords that exist between users
		"""
		record1 = FriendsRecord.objects.filter(user1=user1, user2=user2).first()
		record1.delete()

		record2 = FriendsRecord.objects.filter(user1=user2, user2=user1).first()
		record2.delete()

	def acceptFriendRequest(self):
		""" Accept the current FriendsRecord given that this is a pending friend request
		"""
		if not self.accepted:
			new_friends_record = FriendsRecord(user1=self.user2, user2=self.user1, accepted=True)
			new_friends_record.save()
			self.accepted = True
			self.save()


class PebbleToken(models.Model):
	token = models.CharField(max_length=255)
	pebbleId = models.CharField(max_length=255)
	user = models.ForeignKey(User, blank=True, null=True)
	added = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("token", "pebbleId")

	@staticmethod
	def getFreshToken(pebbleId):
		pt = PebbleToken()
		pt.token = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
		pt.pebbleId = pebbleId
		try:
			pt.save()
			return pt.token
		except ValidationError:
			return PebbleToken.getFreshToken(pebbleId)

	@staticmethod
	def getUser(token, pid):
		return PebbleToken.objects.get(token=pebbleToken, pebbleId=pid).user

	def linkUser(self, user):
		self.user = user
		self.save()


class Suggestion(models.Model):
	description = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
