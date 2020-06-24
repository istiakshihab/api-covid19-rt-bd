from django.urls import path

from . import views

urlpatterns = [
    path('rt_value', views.get_rt_value),
    path('generate_json',views.generate_json),
    path('latest_rt_value', views.latest_rt),
    path('doubling_growth_value', views.doubling_growth_data),
]
