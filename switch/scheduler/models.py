from django.db import models
from django.contrib.auth.models import User
from datetime import timezone, datetime
import pytz
from switch import settings

class Feeder(models.Model):
	name = models.CharField(max_length=30,unique=True)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return u'%s' % self.name

class Receiver(models.Model):
	name = models.CharField(max_length=30,unique=True)
	client = models.ForeignKey(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return u'%s' % self.name

class ScheduledItem(models.Model):
	feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE)
	receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
	start = models.DateTimeField()
	end = models.DateTimeField()

	def __unicode__(self):
		return self.feeder.name

	def __str__(self):
		return u'%s' % self.feeder.name

	def save(self, *args, **kwargs):
		if self.slot_available():
			return super(ScheduledItem, self).save(*args, **kwargs)
		return False

	def sensible_range(self):

		if self.start == None or self.end == None:
			return False

		if self.start.tzinfo == None or self.end.tzinfo == None:
			return False

		if self.end <= self.start:
			return False

		return True

	def slot_available(self):

		if self.sensible_range() == False:
			return 

		if ScheduledItem.objects.filter(start__gt=self.start, start__lte=self.end).exists() or \
			ScheduledItem.objects.filter(end__gte=self.start, end__lt=self.end).exists():
			return False

		if ScheduledItem.objects.filter(start__lt=self.start, end__gt=self.end).exists():
			return False

		return True

	#def save(self, *args, **kwargs):