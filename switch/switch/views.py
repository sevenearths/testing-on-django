from django.shortcuts import render, redirect
from django.template import RequestContext
import api

def handler404(request, *args, **argv):
	if '/api/' in request.build_absolute_uri('?'):
		return api.views.default404(request)
	return redirect('login')

def handler500(request, *args, **argv):

	if '/api/' in request.build_absolute_uri('?'):
		return api.views.default500(request)

	response = render(request, '500.html', {}, RequestContext(request))
	response.status_code = 500
	return response