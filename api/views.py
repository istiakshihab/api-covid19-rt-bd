from django.http import HttpResponse
from . import rt_calculation, doubling_and_growth, covid_percentages
from django.core.files import File
from django.contrib.staticfiles import finders
import pandas as pd

# Create your views here.
def get_rt_value(request):
    json = finders.find('data/data.json')
    file = open(json,'r')
    return HttpResponse(file, content_type = 'application/json')

def generate_json(request):
    rt_json = rt_calculation.get_new_data()
    doubling_and_growth_data_json = doubling_and_growth.get_new_doubling_and_growth_value()
    percentage_data_json = covid_percentages.get_percentages()
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
    with open('static/data/percentages.json','w') as f:
        myFile = File(f)
        myFile.write(percentage_data_json)
        myFile.closed
        f.closed
    return HttpResponse(rt_json, content_type = 'application/json')

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
    merged_df = data.merge(tempData15, how = 'outer', on = ['district'])
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

def get_percentages(request):
    json = finders.find('data/percentages.json')
    file = open(json,'r')
    return HttpResponse(file, content_type = 'application/json')

def get_comparison_doubling(request):
    json = finders.find('data/doubling_and_growth_data.json')
    data = open(json,'r')
    data = pd.read_json(data)
    data = data.sort_values(by=['dates'], ascending= False)
    tempData15 = data.drop_duplicates('dates')
    tempData15 = tempData15[15:]
    tempData15 = data.loc[data['dates'] == tempData15['dates'].iloc[0]]
    data = data.drop_duplicates('district')
    data = data.sort_values(by=['doubling times'], ascending= False)
    del data['growth_value']
    merged_df = data.merge(tempData15, how = 'outer', on = ['district'])
    del merged_df["dates_y"]
    del merged_df["growth_value"]
    data = merged_df
    json = data.to_json(orient='records')
    return HttpResponse(json, content_type = 'application/json')

def get_comparison_growth(request):
    json = finders.find('data/doubling_and_growth_data.json')
    data = open(json,'r')
    data = pd.read_json(data)
    data = data.sort_values(by=['dates'], ascending= False)
    tempData15 = data.drop_duplicates('dates')
    tempData15 = tempData15[15:]
    tempData15 = data.loc[data['dates'] == tempData15['dates'].iloc[0]]
    data = data.drop_duplicates('district')
    data = data.sort_values(by=['growth_value'], ascending= False)
    del data['doubling times']
    merged_df = data.merge(tempData15, how = 'outer', on = ['district'])
    del merged_df["dates_y"]
    del merged_df["doubling times"]
    data = merged_df
    json = data.to_json(orient='records')
    return HttpResponse(json, content_type = 'application/json')
