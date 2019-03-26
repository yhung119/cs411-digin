import datetime

from django.db import models
from django.utils import timezone
from users.models import CustomUser as User

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	owner =  models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.question_text
	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	
	
class Choice(models.Model):
	'''
	need to have unique field of question and choice_text
	'''
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	owner =  models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.choice_text