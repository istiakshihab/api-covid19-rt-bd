from django.urls import path

from . import views

urlpatterns = [
    path('rt_value', views.get_rt_value),
    path('generate_json',views.generate_json),
    path('latest_rt_value', views.latest_rt),
    path('before_15_rt', views.before_15_rt),
    path('doubling_growth_value', views.doubling_growth_data),
    path('latest_doubling_value', views.latest_doubling_value),
    path('get_percentages', views.get_percentages),
    path('get_comparison_doubling', views.get_comparison_doubling),
    path('get_comparison_growth', views.get_comparison_growth),
]
