"""Enrutador principal: envía las peticiones a la app equipos."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('equipos.urls')),
]
