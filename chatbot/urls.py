from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    url('', views.get_info, name='get_info'),
]


