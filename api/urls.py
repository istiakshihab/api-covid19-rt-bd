from django.urls import path

from . import views

urlpatterns = [
    path('rt_value', views.get_rt_value, name='location'),
]
