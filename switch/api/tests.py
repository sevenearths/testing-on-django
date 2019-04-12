from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from scheduler.models import ScheduledItem, Feeder, Receiver
from datetime import timezone, datetime
import pytz


class APIResourceTest(TestCase):

	client1 = 'client-1'
	client2 = 'client-2'
	feeder1 = 'Feeder 1'
	feeder2 = 'Feeder 2'
	feeder3 = 'Feeder 3'
	feeder4 = 'Feeder 4'
	client1Receiver1 = 'Client 1 Receiver 1'
	client1Receiver2 = 'Client 1 Receiver 2'
	client1Receiver3 = 'Client 1 Receiver 3'
	client2Receiver1 = 'Client 2 Receiver 1'
	client1Receiver1ScheduledItem1_start = datetime(1970, 1, 1, 0, 0, 0)
	client1Receiver1ScheduledItem1_end = datetime(1970, 1, 1, 0, 30, 0)
	client1Receiver1ScheduledItem2_start = datetime(1970, 1, 1, 1, 0, 0)
	client1Receiver1ScheduledItem2_end = datetime(1970, 1, 1, 1, 30, 0)
	client2Receiver1ScheduledItem1_start = datetime(1970, 1, 1, 0, 0, 0)
	client2Receiver1ScheduledItem1_end = datetime(1970, 1, 1, 0, 30, 0)

	def setUp(self):
		self.client = Client()
		self.timezone = pytz.timezone('Europe/London')
		# clients
		user_client_1 = User.objects.create_user(
			username=self.client1, email=self.client2+'@as.com', password=self.client1)
		user_client_2 = User.objects.create_user(
			username=self.client2, email=self.client2+'@as.com', password=self.client2)
		# feeders
		feeder1_obj = Feeder.objects.create(name=self.feeder1)
		feeder2_obj = Feeder.objects.create(name=self.feeder2)
		feeder3_obj = Feeder.objects.create(name=self.feeder3)
		feeder4_obj = Feeder.objects.create(name=self.feeder4)
		# receivers
		client1Receiver1_obj = Receiver.objects.create(name=self.client1Receiver1, client=user_client_1)
		client1Receiver2_obj = Receiver.objects.create(name=self.client1Receiver2, client=user_client_1)
		client1Receiver3_obj = Receiver.objects.create(name=self.client1Receiver3, client=user_client_1)
		client2Receiver1_obj = Receiver.objects.create(name=self.client2Receiver1, client=user_client_2)
		# scheduled items
		client1Receiver1ScheduledItem1_obj = ScheduledItem.objects.create(
			feeder=feeder1_obj,
			receiver=client1Receiver1_obj,
			start=self.timezone.localize(self.client1Receiver1ScheduledItem1_start),
			end=self.timezone.localize(self.client1Receiver1ScheduledItem1_end))
		client1Receiver1ScheduledItem2_obj = ScheduledItem.objects.create(
			feeder=feeder1_obj,
			receiver=client1Receiver1_obj,
			start=self.timezone.localize(self.client1Receiver1ScheduledItem2_start),
			end=self.timezone.localize(self.client1Receiver1ScheduledItem2_end))
		client2Receiver1ScheduledItem1_obj = ScheduledItem.objects.create(
			feeder=feeder1_obj,
			receiver=client2Receiver1_obj,
			start=self.timezone.localize(self.client2Receiver1ScheduledItem1_start),
			end=self.timezone.localize(self.client2Receiver1ScheduledItem1_end))

		self.client1Receiver1_obj = client1Receiver1_obj
		self.client1_obj = user_client_1
		self.client2_obj = user_client_2
		self.feeder1_obj = feeder1_obj
		self.feeder2_obj = feeder2_obj
		self.feeder3_obj = feeder3_obj
		self.feeder4_obj = feeder4_obj
		self.client1Receiver1_obj = client1Receiver1_obj
		self.client1Receiver2_obj = client1Receiver2_obj
		self.client1Receiver3_obj = client1Receiver3_obj
		self.client2Receiver1_obj = client2Receiver1_obj
		self.client1Receiver1ScheduledItem1_obj = client1Receiver1ScheduledItem1_obj
		self.client1Receiver1ScheduledItem2_obj = client1Receiver1ScheduledItem2_obj
		self.client2Receiver1ScheduledItem1_obj = client2Receiver1ScheduledItem1_obj

	# Routes

	def test_get_route_that_doesnt_exist_returns_404(self):
		response = self.client.get('/api/dave/', format='json')
		self.assert404response(response)


	# Login

	def test_get_login_returns_404(self):
		response = self.client.get('/api/login/', format='json')
		self.assert404response(response)

	def test_post_login_with_no_data_returns_404(self):
		data = {}
		response = self.client.post('/api/login/', data, content_type='application/json')
		self.assert404response(response)

	def test_post_login_with_bad_data_returns_404(self):
		data = {'username': 'client-1', 'password': 'client'}
		response = self.client.post('/api/login/', data, content_type='application/json')
		self.assert404response(response)

	def test_post_login_with_correct_data_returns_200(self):
		response = self.loginClientOne()
		self.assert200response(response)


	# Logout

	def test_get_logout_not_logged_in_returns_200(self):
		response = self.client.get('/api/logout/', format='json')
		self.assert200response(response)

	def test_get_logout_returns_200(self):
		self.loginClientOne()
		response = self.client.get('/api/logout/', format='json')
		self.assert200response(response)


	# Feeders

	def test_get_feeders_not_logged_in_404(self):
		response = self.client.get('/api/feeders/', format='json')
		self.assert404response(response)

	def test_get_feeders_200(self):
		self.loginClientOne()
		response = self.client.get('/api/feeders/', format='json')
		self.assert200response(response)
		self.assertEqual(4, len(response.json()['data']))
		self.assertEqual(self.feeder1, response.json()['data'][0]['name'])
		self.assertEqual(self.feeder1_obj.id, int(response.json()['data'][0]['id']))
		self.assertEqual(self.feeder2, response.json()['data'][1]['name'])
		self.assertEqual(self.feeder2_obj.id, int(response.json()['data'][1]['id']))
		self.assertEqual(self.feeder3, response.json()['data'][2]['name'])
		self.assertEqual(self.feeder3_obj.id, int(response.json()['data'][2]['id']))
		self.assertEqual(self.feeder4, response.json()['data'][3]['name'])
		self.assertEqual(self.feeder4_obj.id, int(response.json()['data'][3]['id']))


	# Receivers

	def test_get_receivers_not_logged_in_404(self):
		response = self.client.get('/api/receivers/', content_type='application/json')
		self.assert404response(response)

	def test_get_receivers_client1_200(self):
		self.loginClientOne()
		response = self.client.get('/api/receivers/', content_type='application/json')
		self.assert200response(response)

		client_id = self.client1_obj.id
		self.assertEqual(3, len(response.json()['data']))

		self.assertEqual(self.client1Receiver1, response.json()['data'][0]['name'])
		self.assertEqual(self.client1Receiver1_obj.id, int(response.json()['data'][0]['id']))
		self.assertEqual(client_id, int(response.json()['data'][0]['client_id']))

		self.assertEqual(self.client1Receiver2, response.json()['data'][1]['name'])
		self.assertEqual(self.client1Receiver2_obj.id, int(response.json()['data'][1]['id']))
		self.assertEqual(client_id, int(response.json()['data'][0]['client_id']))

		self.assertEqual(self.client1Receiver3, response.json()['data'][2]['name'])
		self.assertEqual(self.client1Receiver3_obj.id, int(response.json()['data'][2]['id']))
		self.assertEqual(client_id, int(response.json()['data'][0]['client_id']))

	def test_get_receivers_client2_200(self):
		self.loginClientTwo()
		response = self.client.get('/api/receivers/', content_type='application/json')
		self.assert200response(response)

		client_id = self.client2_obj.id
		self.assertEqual(1, len(response.json()['data']))

		self.assertEqual(self.client2Receiver1, response.json()['data'][0]['name'])
		self.assertEqual(self.client2Receiver1_obj.id, int(response.json()['data'][0]['id']))
		self.assertEqual(client_id, int(response.json()['data'][0]['client_id']))


	# Scheduled Items

	def test_get_scheduled_items_not_logged_in_404(self):
		receiver_id = str(self.client1Receiver1_obj.id)
		response = self.client.get('/api/scheduleditems/'+receiver_id+'/', content_type='application/json')
		self.assert404response(response)

	def test_get_scheduled_items_wrong_client_logged_in_400(self):
		self.loginClientTwo()
		receiver_id = str(self.client1Receiver1_obj.id)
		response = self.client.get('/api/scheduleditems/'+receiver_id+'/', content_type='application/json')
		self.assert400response(response)

		self.assertEqual('you are not the client for this receiver', response.json()['data'])

	def test_get_scheduled_items_200(self):
		self.loginClientOne()
		receiver_id = str(self.client1Receiver1_obj.id)
		response = self.client.get('/api/scheduleditems/'+receiver_id+'/', content_type='application/json')
		self.assert200response(response)

		self.assertEqual(2, len(response.json()['data']))

		client1Receiver1ScheduledItem1_start_str = self.timezone.localize(self.client1Receiver1ScheduledItem1_start).strftime('%Y-%m-%d %H:%M:%S')
		client1Receiver1ScheduledItem1_end_str = self.timezone.localize(self.client1Receiver1ScheduledItem1_end).strftime('%Y-%m-%d %H:%M:%S')
		self.assertEqual(self.client1Receiver1ScheduledItem1_obj.id, response.json()['data'][0]['id'])
		self.assertEqual(self.client1_obj.id, response.json()['data'][0]['client_id'])
		self.assertEqual(self.feeder1_obj.id, response.json()['data'][0]['feeder_id'])
		self.assertEqual(self.client1Receiver1_obj.id, response.json()['data'][0]['receiver_id'])
		self.assertEqual(client1Receiver1ScheduledItem1_start_str, response.json()['data'][0]['start'])
		self.assertEqual(client1Receiver1ScheduledItem1_end_str, response.json()['data'][0]['end'])


	# Scheduled Item Add

	def test_post_scheduled_item_add_not_logged_in_404(self):
		receiver_id = str(self.client1Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert404response(response)

	def test_post_scheduled_item_add_no_data_400(self):
		self.loginClientOne()
		receiver_id = str(self.client1Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert400response(response)

	def test_post_scheduled_item_add_start_date_wrong_format_400(self):
		self.loginClientOne()
		receiver_id = str(self.client1Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {'start': 'dave', 'end': '1970/01/01 00:00:00'}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert400response(response)
		self.assertIn("time data 'dave' does not match format", response.json()['data'])

	def test_post_scheduled_item_add_wrong_receiver_400(self):
		self.loginClientOne()
		receiver_id = str(self.client2Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {'start': 'dave', 'end': 'dave'}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert400response(response)
		self.assertIn('you are not the client for this receiver', response.json()['data'])

	def test_post_scheduled_item_add_slot_taken_400(self):
		self.loginClientOne()
		receiver_id = str(self.client1Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {'start': '1970/01/01 00:15:00', 'end': '1970/01/01 00:45:00'}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert400response(response)
		self.assertIn('slot unavailable', response.json()['data'])

	def test_post_scheduled_item_add_slot_available_201(self):
		self.loginClientOne()
		receiver_id = str(self.client1Receiver1_obj.id)
		feeder_id = str(self.feeder1_obj.id)
		data = {'start': '1970/01/01 03:00:00', 'end': '1970/01/01 04:00:00'}
		response = self.client.post('/api/scheduleditem/add/'+feeder_id+'/'+receiver_id+'/', data, content_type='application/json')
		self.assert201response(response)


	# Funtions Internal
	
	def assert200response(self, response):
		self.assertEqual(response.status_code, 200)
		self.assertEqual(200, int(response.json()['status']))
	
	def assert201response(self, response):
		self.assertEqual(response.status_code, 200)
		self.assertEqual(201, int(response.json()['status']))
	
	def assert400response(self, response):
		self.assertEqual(response.status_code, 200)
		self.assertEqual(400, int(response.json()['status']))
	
	def assert404response(self, response):
		self.assertEqual(response.status_code, 200)
		self.assertEqual(404, int(response.json()['status']))

	def loginClientOne(self):
		data = {'username': self.client1, 'password': self.client1}
		return self.client.post('/api/login/', data, content_type='application/json')

	def loginClientTwo(self):
		data = {'username': self.client2, 'password': self.client2}
		return self.client.post('/api/login/', data, content_type='application/json')