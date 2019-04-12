from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

handler404 = 'switch.views.handler404'
handler500 = 'switch.views.handler500'

urlpatterns = [
    path('', lambda request: redirect('login', permanent=False)),
    path('login/', include('login.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
