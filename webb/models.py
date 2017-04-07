from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Passwordresetcodes(models.Model):
	code = models.CharField(max_length = 32)
	email = models.CharField(max_length = 120)
	time = models.DateTimeField()
	username = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)
# Create your models here.
class Token(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	token = models.CharField(max_length=48)
	def __unicode__(self):
		return "{}_token".format(self.user)

class Expense(models.Model):
	text = models.CharField(max_length = 256)
	date = models.DateTimeField()
	amount = models.BigIntegerField()
	user = models.ForeignKey(User)
	def __unicode__(self):
		return "{}-{}".format(self.date,self.user, self.amount)

class Income(models.Model):
	text = models.CharField(max_length = 256)
	date = models.DateTimeField()
	amount = models.BigIntegerField()
	user = models.ForeignKey(User)
	def __unicode__(self):
		return "{}-{}".format(self.date,self.user, self.amount)

	
