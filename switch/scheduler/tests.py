from django.test import TestCase
from scheduler.models import Feeder, Receiver, ScheduledItem
from django.contrib.auth.models import User
from datetime import timezone, datetime
import pytz

class SchedulerTest(TestCase):

	def setUp(self):
		self.timezone = pytz.timezone('Europe/London')

	def test_create_feeder_item(self):
		feeder = self.create_feeder()
		self.assertTrue(isinstance(feeder, Feeder))
		self.assertEqual(feeder.__str__(), feeder.name)

	def test_create_receiver_item(self):
		client = self.create_user()
		receiver = self.create_receiver(client)
		self.assertTrue(isinstance(receiver, Receiver))
		self.assertEqual(receiver.__str__(), receiver.name)

	def test_create_scheduled_item_item(self):
		client = self.create_user()
		feeder = self.create_feeder()
		receiver = self.create_receiver(client)
		scheduledItem = self.create_scheduled_item(feeder, receiver)
		self.assertTrue(isinstance(scheduledItem, ScheduledItem))
		self.assertEqual(scheduledItem.__str__(), scheduledItem.feeder.name)


	# Sensible Range (function)

	def test_scheduled_item_sensible_range_fail_no_start_or_end_function(self):
		self.create_client_feeder_receiver()
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_no_start_function(self):
		self.create_client_feeder_receiver()
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver,end=end)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_no_end_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver,start=start)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_start_no_time_zone_function(self):
		self.create_client_feeder_receiver()
		start = datetime(1970, 1, 1, 0, 0, 0)
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_end_no_time_zone_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = datetime(1970, 1, 1, 0, 30, 0)
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_end_before_start_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver,start=start, end=end)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_fail_start_same_as_end_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver,start=start, end=end)
		self.assertFalse(scheduledItem.sensible_range())

	def test_scheduled_item_sensible_range_pass_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		scheduledItem = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		self.assertTrue(scheduledItem.sensible_range())


	# Slot Available (function)

	def test_scheduled_item_slot_available_fail_slot_end_equals_item_start_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1969, 12, 31, 23, 59, 59))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_fail_slot_end_greater_than_item_start_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1969, 12, 31, 23, 59, 59))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 1))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_fail_slot_start_equal_to_item_end_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 1))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_fail_slot_start_less_than_item_end_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1970, 1, 1, 0, 29, 59))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 1))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_fail_slot_inside_item_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1970, 1, 1, 0, 10, 0))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 20, 0))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_fail_slot_covers_item_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1969, 12, 31, 23, 30, 0))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 1, 30, 0))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertFalse(slot_request.slot_available())

	def test_scheduled_item_slot_available_pass_slot_in_past_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1969, 12, 31, 23, 30, 0))
		end_req = self.timezone.localize(datetime(1969, 12, 31, 23, 40, 0))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertTrue(slot_request.slot_available())

	def test_scheduled_item_slot_available_pass_slot_in_future_function(self):
		self.create_client_feeder_receiver()
		start = self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0))
		end = self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0))
		ScheduledItem.objects.create(feeder=self.feeder, receiver=self.receiver, start=start, end=end)
		start_req = self.timezone.localize(datetime(1970, 1, 1, 0, 40, 0))
		end_req = self.timezone.localize(datetime(1970, 1, 1, 0, 50, 0))
		slot_request = ScheduledItem(feeder=self.feeder, receiver=self.receiver, start=start_req, end=end_req)
		self.assertTrue(slot_request.slot_available())


	# Internal Functions

	def create_feeder(self):
		feeder = Feeder(name='Dave')
		feeder.save()
		return feeder

	def create_user(self):
		return User.objects.create_user(username='client_1',
			email='client1@as.com',
			password='client_1')

	def create_receiver(self, client):
		receiver = Receiver(name='Dave', client=client)
		receiver.save()
		return receiver

	def create_scheduled_item(self, feeder, receiver):
		scheduledItem = ScheduledItem(
			feeder=feeder,
			receiver=receiver,
			start=self.timezone.localize(datetime(1970, 1, 1, 0, 0, 0)),
			end=self.timezone.localize(datetime(1970, 1, 1, 0, 30, 0)))
		scheduledItem.save()
		return scheduledItem

	def create_client_feeder_receiver(self):
		self.client = self.create_user()
		self.feeder = self.create_feeder()
		self.receiver = self.create_receiver(self.client)