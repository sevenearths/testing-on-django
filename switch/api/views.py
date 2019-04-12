from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import viewsets
from scheduler.models import ScheduledItem, Feeder, Receiver
from django.core import serializers
from datetime import timezone, datetime
from switch import settings
from django.utils.timezone import make_naive
import pytz
import json

import logging
logger = logging.getLogger(__name__)

def default200(request):
	return JsonResponse({'status':'200'})

def default201(request):
	return JsonResponse({'status':'201'})

def default400(request):
	return JsonResponse({'status':'400'})

def default404(request):
	return JsonResponse({'status':'404'})

def default500(request):
	return JsonResponse({'status':'500'})


def api_login(request):

	if request.method == "POST":
		json_data = json.loads(request.body.decode('utf-8'))

		if 'username' in json_data and 'password' in json_data:

			username = json_data['username']
			password = json_data['password']
			user = authenticate(username=username, password=password)

			if user is not None:

				login(request, user)
				return default200(request)

	return default404(request)


def api_logout(request):

    logout(request)
    return default200(request)


def api_feeders(request):

	if request.user.is_authenticated:
		feeders = []

		for feeder in Feeder.objects.all():
			feeders.append({'id': feeder.id, 'name': feeder.name})

		return JsonResponse({'status': 200, 'data': feeders})

	return default404(request)


def api_receivers(request):

	if request.user.is_authenticated:
		receivers = []

		for receiver in Receiver.objects.filter(client=request.user):

			receivers.append({
				'id': receiver.id, 
				'client_id': receiver.client.id, 
				'name': receiver.name})

		return JsonResponse({'status': 200, 'data': receivers})

	return default404(request)


def api_scheduled_items(request, receiver_id):

	if request.user.is_authenticated:
		receiver = Receiver.objects.get(id=receiver_id)

		if request.user.id != receiver.client.id:
			return JsonResponse({'status': 400, 'data': 'you are not the client for this receiver'})

		scheduled_items = []

		for scheduled_item in ScheduledItem.objects.filter(receiver=receiver):

			scheduled_items.append({
				'id': scheduled_item.id, 
				'client_id': scheduled_item.receiver.client.id, 
				'feeder_id': scheduled_item.feeder.id,
				'feeder_name': scheduled_item.feeder.name, 
				'receiver_id': scheduled_item.receiver.id, 
				'receiver_name': scheduled_item.receiver.name, 
				'start': make_naive(scheduled_item.start).strftime('%Y-%m-%d %H:%M:%S'), 
				'end': make_naive(scheduled_item.end).strftime('%Y-%m-%d %H:%M:%S')})

		return JsonResponse({'status': 200, 'data': scheduled_items})

	return default404(request)


def api_scheduled_item_add(request, feeder_id, receiver_id):

	if request.method == 'POST' and request.user.is_authenticated:

		timezone = pytz.timezone(settings.TIME_ZONE)

		try:
			post_data = json.loads(request.body.decode('utf-8'))
		except ValueError as error:
			return JsonResponse({'status': 400, 'data': 'data not in json format'})

		if set(['start','end']).issubset(post_data) == False:
			return default400(request)

		receiver = Receiver.objects.get(id=receiver_id)

		if request.user.id != receiver.client.id:
			return JsonResponse({'status': 400, 'data': 'you are not the client for this receiver'})

		feeder = Feeder.objects.get(id=feeder_id)

		try:
			start = timezone.localize(datetime.strptime(post_data['start'], '%Y/%m/%d %H:%M:%S'))
			end = timezone.localize(datetime.strptime(post_data['end'], '%Y/%m/%d %H:%M:%S'))
		except ValueError as error:
			return JsonResponse({'status': 400, 'data': str(error)})

		scheduledItem = ScheduledItem(feeder=feeder, receiver=receiver, start=start, end=end)

		if scheduledItem.save() == False:
			return JsonResponse({'status': 400, 'data': 'slot unavailable'})

		return default201(request)

	return default404(request)
