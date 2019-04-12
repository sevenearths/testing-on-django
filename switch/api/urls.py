from django.urls import path

from . import views

urlpatterns = [
	path('login/', views.api_login, name='api_login'),
	path('logout/', views.api_logout, name='api_logout'),
	path('feeders/', views.api_feeders, name='api_feeders'),
	path('receivers/', views.api_receivers, name='api_receivers'),
	path('scheduleditems/<int:receiver_id>/', views.api_scheduled_items, name='api_scheduled_items'),
	path('scheduleditem/add/<int:feeder_id>/<int:receiver_id>/', views.api_scheduled_item_add, name='api_scheduled_item_add'),
]