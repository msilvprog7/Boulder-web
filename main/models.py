from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
import time

import random, math

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

	@staticmethod
	def getLvl(user_id):
		""" Gets the level of the user based on the equation used to compute Pokemon Levels (i.e floor(cubed_root(exp))
			where exp is rep points in our case)
		"""
		return int(Activity.getUserPoints(user_id) ** (1/3.0))

	@staticmethod
	def getNextLvlExp(user_id):
		""" Gets exp req to get to the next level from the base of the current level
		"""
		return int((Activity.getLvl(user_id) + 1) ** 3.0 - Activity.getUserPoints(user_id))
	
	@staticmethod
	def getCurrentLvlExp(user_id):
		""" Get current exp in level from the base of the current level
		"""
		return int(Activity.getUserPoints(user_id) - Activity.getLvl(user_id) ** 3.0)

	@staticmethod
	def activityFromClfId(clfId):
		return Activity.objects.get(description=str(clfId))


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
		return self.number * self.activity.points

	@staticmethod
	def logActivityForUser(user, activity):
		others = CompletedActivity.objects.filter(user=user, activity=activity).order_by("-time")
		if len(others) != 0:
			if (time.mktime(datetime.utcnow().timetuple()) - (time.mktime(others[0].time.timetuple())) < 5:
				others[0].number += 1
				others[0].save()
				return
		c = CompletedActivity()
		c.activity = activity
		c.number = 1
		c.user = user
		c.save()




class FriendsRecord(models.Model):
	""" FriendsRecord to determine whether or not someone has a pending friend request and
		which users are friends.
	"""
	user1 = models.ForeignKey(User, related_name="friends_set")
	user2 = models.ForeignKey(User, related_name="friend_request_set")
	accepted = models.BooleanField(default=False)


	@staticmethod
	def getFriends(user_id):
		""" Get a set of FriendsRecord for the given user_id where user2 in each is one of user1's friends
		"""
		return FriendsRecord.objects.filter(user1_id=user_id, accepted=True)

	@staticmethod
	def getFriendRequests(user_id):
		""" Get a set of FriendsRecord for pending friend requests for the given user_id so user1 in each is a 
			pending friend request sent to user2
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

		news_item1 = NewsfeedItem.objects.filter(user=user1, other_user=user2).first()
		news_item1.delete()
		news_item2 = NewsfeedItem.objects.filter(user=user2, other_user=user1).first()
		news_item2.delete()

	def acceptFriendRequest(self):
		""" Accept the current FriendsRecord given that this is a pending friend request
		"""
		if not self.accepted:
			new_friends_record = FriendsRecord(user1=self.user2, user2=self.user1, accepted=True)
			new_friends_record.save()
			self.accepted = True
			self.save()

			news_item1 = NewsfeedItem(user=self.user1, other_user=self.user2)
			news_item1.save()
			news_item2 = NewsfeedItem(user=self.user2, other_user=self.user1)
			news_item2.save()


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
		pt.token = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
		pt.pebbleId = pebbleId
		try:
			pt.save()
			return pt.token
		except ValidationError:
			return PebbleToken.getFreshToken(pebbleId)

	@staticmethod
	def getUser(token, pid):
		return PebbleToken.objects.get(token=token, pebbleId=pid).user

	def linkUser(self, user):
		self.user = user
		self.save()


class Suggestion(models.Model):
	description = models.TextField()
	time = models.DateTimeField(auto_now_add=True)


class NewsfeedItem(models.Model):
	user = models.ForeignKey(User, related_name="user_set")
	other_user = models.ForeignKey(User, blank=True, null=True, default=None, related_name="other_user_set")

	completed_activity = models.ForeignKey(CompletedActivity, blank=True, null=True, default=None)

	time = models.DateTimeField(auto_now_add=True)
	
	@staticmethod
	def getItems(friends_records):
		""" Get NewsfeedItems for the given friends contained in FriendsRecord list given (via user2)
		"""
		news_item = []
		for friends_record in friends_records:
			news_item.append(NewsfeedItem.objects.filter(user=friends_record.user2).all())

		return news_item

