from django.http import HttpResponse
from . import pyFiling

# Create your views here.
def get_rt_value(request):
    json = pyFiling.get_data(request.GET['location'])
    return HttpResponse(json, content_type = 'application/json')