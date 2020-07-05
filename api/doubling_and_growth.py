import pandas as pd
from . import rt_data_processing as rf

def get_new_doubling_and_growth_value():
    fileLoc = "static/data/newData.csv"
    datasetx = pd.read_csv(fileLoc)
    listing = datasetx.dis_name.unique()
    resultFinal = ""
    for elem in listing:
        result = pd.DataFrame()
        dataset = datasetx.loc[datasetx['dis_name'] == elem]
        dataset['tdate'] = pd.to_datetime(dataset['tdate'])
        dataset = dataset.sort_values(by='tdate')
        dataSeries = pd.Series(dataset['positive_cases'].values, index=dataset['tdate'])
        dataSeries = dataSeries.sort_index()
        dataSeries = dataSeries.cumsum()
        pd.to_numeric(dataSeries, errors="coerce")
        original, smoothed = rf.prepare_cases(dataSeries)
        original = pd.Series(smoothed.values, smoothed.index)
        date = original.index.values
        cases = original.values  
        allcases = [[date[0], cases[0], 0, 0]]
        for i in range(1, len(date)):
            allcases.append([date[i], allcases[-1][1] + cases[i], 0, 0])
            allcases[0][2] = allcases[1][1]/allcases[0][1]-1
            allcases[0][3] = 0.7/allcases[0][2]
        for i in range(len(allcases)):
            if allcases[i][2] == 0.0:
                allcases[i][2] = allcases[i][1]/allcases[i-1][1]-1
            if allcases[i][3] == 0.0:
                allcases[i][3] = 0.7/allcases[i][2]
        doublingtimes = [row[3] for row in allcases]
        dates = [row[0] for row in allcases]
        growth_value = [row[2] for row in allcases]
        dates = [row[0] for row in allcases]
        result['dates'] = dates
        result['doubling times'] = doublingtimes
        result['growth_value'] = growth_value
        result['district'] = elem
        result = result.to_json(orient="records")
        resultFinal += result
    resultFinal = resultFinal.replace("[","")
    resultFinal = resultFinal.replace("]",",")
    resultFinal = resultFinal[:-1]
    resultFinal = "["+resultFinal+"]"
    return resultFinal
    
def get_doubling_and_growth_value():
    fileLoc  = "https://gitlab.com/api/v4/projects/18229284/repository/files/Pipilika_Coronavirus_cases.xlsx/raw?ref=NewUpdate"
    sheetLoc = "Sheet1"
    datasetxl = rf.prepare_data(fileLoc, sheetLoc)
    datasetxl = rf.rolling_mean(datasetxl)
    resultFinal = ""
    for column in datasetxl:
        try:
            if(column != "Date"):
                result = pd.DataFrame()
                dataSeries = pd.Series(datasetxl[column].values, index=datasetxl['Date'])
                pd.to_numeric(dataSeries, errors="coerce")
                original, smoothed = rf.prepare_cases(dataSeries)
                original = pd.Series(smoothed.values, smoothed.index)
                date = original.index.values
                cases = original.values  
                allcases = [[date[0], cases[0], 0, 0]]
                for i in range(1, len(date)):
                    allcases.append([date[i], allcases[-1][1] + cases[i], 0, 0])
                    allcases[0][2] = allcases[1][1]/allcases[0][1]-1
                    allcases[0][3] = 0.7/allcases[0][2]
                for i in range(len(allcases)):
                    if allcases[i][2] == 0.0:
                        allcases[i][2] = allcases[i][1]/allcases[i-1][1]-1
                    if allcases[i][3] == 0.0:
                        allcases[i][3] = 0.7/allcases[i][2]
                doublingtimes = [row[3] for row in allcases]
                dates = [row[0] for row in allcases]
                growth_value = [row[2] for row in allcases]
                dates = [row[0] for row in allcases]
                result['dates'] = dates
                result['doubling times'] = doublingtimes
                result['growth_value'] = growth_value
                result['district'] = column
                result = result.to_json(orient="records")
                resultFinal += result
        except IndexError:
            pass
        except ValueError:
            pass
    resultFinal = resultFinal.replace("[","")
    resultFinal = resultFinal.replace("]",",")
    resultFinal = resultFinal[:-1]
    resultFinal = "["+resultFinal+"]"
    return resultFinal
                