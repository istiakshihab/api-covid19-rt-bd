from django.http import HttpResponse
from . import pyFiling
from django.core.files import File
from django.contrib.staticfiles import finders
import pandas as pd

# Create your views here.
def get_rt_value(request):
    json = finders.find('data/data.json')
    file = open(json,'r')
    return HttpResponse(file, content_type = 'application/json')

def generate_json(request):
    json = pyFiling.get_data()
    with open('static/data/data.json','w') as f:
        myFile = File(f)
        myFile.write(json)
        myFile.closed
        f.closed
    return HttpResponse(json, content_type = 'application/json')

def latest_rt(request):
    json = finders.find('data/data.json')
    data = pd.read_json(json)
    data = data.sort_values(by=['Date'], ascending= False)
    data = data.drop_duplicates('district')
    del data['Date']
    data = data.sort_values(by=['ML'], ascending= False)
    json = data.to_json(orient="records")
    return HttpResponse(json, content_type = 'application/json')