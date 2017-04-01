from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
	text = models.CharField(max_length = 256)
	date = models.DateTimeField()
	amount = models.BigIntegerField()
	user = models.ForeignKey(User)
	def __unicode__(text):
		return "{}-{}".format(self.date, self.amount)

class Income(models.Model):
	text = models.CharField(max_length = 256)
	date = models.DateTimeField()
	amount = models.BigIntegerField()
	user = models.ForeignKey(User)
	def __unicode__(text):
		return "{}-{}".format(self.date, self.amount)

	
