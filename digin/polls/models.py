import datetime

from django.db import models
from django.utils import timezone
from users.models import CustomUser as User

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	owner =  models.ForeignKey(User, on_delete=models.CASCADE)
	deadline = models.DateTimeField('deadline time')
	is_active = models.BooleanField()

	def __str__(self):
		return self.question_text

	
class Poll_members(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	member = models.ForeignKey(User, on_delete=models.CASCADE)

	

class Place(models.Model):
	name = models.CharField(max_length=200)
	phone = models.CharField(max_length=200, blank=True)
	address = models.CharField(max_length=200)
	price_level = models.IntegerField(blank=True)
	rating = models.IntegerField()
	latitude = models.IntegerField()
	longitude = models.IntegerField()
	place_id = models.CharField(max_length=200, unique=True)
	website = models.CharField(max_length=200, blank=True)
	reviews = models.CharField(max_length=10000)


class Choice(models.Model):
	'''
	need to have unique field of question and choice_text
	'''
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	votes = models.IntegerField(default=0)
	owner =  models.ForeignKey(User, on_delete=models.CASCADE)
	place_id = models.ForeignKey(Place, to_field="place_id", db_column="place_id", on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	

class Archive_question(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	place_id = models.ForeignKey(Place, to_field="place_id", db_column="place_id", on_delete=models.CASCADE)


class Vote(models.Model):
	question=models.ForeignKey(Question, on_delete=models.CASCADE)
	owner= models.ForeignKey(User, on_delete=models.CASCADE)
	choice=models.ForeignKey(Choice, on_delete=models.CASCADE)