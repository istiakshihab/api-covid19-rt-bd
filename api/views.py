from django.http import HttpResponse
from . import rt_calculation, doubling_and_growth
from django.core.files import File
from django.contrib.staticfiles import finders
import pandas as pd

# Create your views here.
def get_rt_value(request):
    json = finders.find('data/data.json')
    file = open(json,'r')
    return HttpResponse(file, content_type = 'application/json')

def generate_json(request):
    rt_json = rt_calculation.get_data()
    doubling_and_growth_data_json = doubling_and_growth.get_doubling_and_growth_value()
    with open('static/data/data.json','w') as f:
        myFile = File(f)
        myFile.write(rt_json)
        myFile.closed
        f.closed
    with open('static/data/doubling_and_growth_data.json','w') as f:
        myFile = File(f)
        myFile.write(doubling_and_growth_data_json)
        myFile.closed
        f.closed
    return HttpResponse(doubling_and_growth_data_json, content_type = 'application/json')

def latest_rt(request):
    json = finders.find('data/data.json')
    data = pd.read_json(json)
    data = data.sort_values(by=['Date'], ascending= False)
    data = data.drop_duplicates('district')
    data = data.sort_values(by=['ML'], ascending= False)
    json = data.to_json(orient="records")
    return HttpResponse(json, content_type = 'application/json')

def before_15_rt(request):
    json = finders.find('data/data.json')
    data = pd.read_json(json)
    data = data.sort_values(by=['Date'], ascending= False)
    tempData15 = data.drop_duplicates('Date')
    tempData15 = tempData15[15:]
    tempData15 = data.loc[data['Date'] == tempData15['Date'].iloc[0]]
    data = data.drop_duplicates('district')
    data = data.sort_values(by=['ML'], ascending= False)
    data = data[:15]
    merged_df = data.merge(tempData15, how = 'outer', on = ['district'])
    merged_df = merged_df[:15]
    merged_df["ML_y"] = merged_df["ML_y"].fillna(0)
    merged_df["Low_90_y"] = merged_df["Low_90_y"].fillna(0)
    merged_df["High_90_y"] = merged_df["High_90_y"].fillna(0)
    merged_df["Date_y"] = merged_df["Date_y"].fillna(0)
    del merged_df["ML_x"]
    del merged_df["Low_90_x"]
    del merged_df["High_90_x"]
    del merged_df["Date_x"]
    data = merged_df
    data.columns = ['district','Date','ML','Low','High']
    json = data.to_json(orient="records")
    return HttpResponse(json, content_type = 'application/json')


def doubling_growth_data(request):
    json = finders.find('data/doubling_and_growth_data.json')
    file = open(json,'r')
    return HttpResponse(file, content_type = 'application/json')

def latest_doubling_value(request):
    json = finders.find('data/doubling_and_growth_data.json')
    data = pd.read_json(json)
    data = data.sort_values(by=['dates'], ascending= False)
    data = data.drop_duplicates('district')
    del data['growth_value']
    data = data.sort_values(by=['doubling times'], ascending= False)
    json = data.to_json(orient="records")
    return HttpResponse(json, content_type = 'application/json')