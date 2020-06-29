import pandas as pd

def get_percentages():
    k = []
    fileLoc  = "https://gitlab.com/api/v4/projects/18229284/repository/files/Pipilika_Coronavirus_cases.xlsx/raw?ref=NewUpdate"
    sheetLoc = "Sheet1"
    datasetxl = pd.read_excel(fileLoc,sheetLoc)
    datasetxl.rename( columns={'Unnamed: 0':'Location'}, inplace=True )
    datasetxl = datasetxl[66:67]
    tested = datasetxl[datasetxl.columns[::3]]
    del tested['Location']
    positive = datasetxl.loc[:, ~datasetxl.columns.str.contains('^Unnamed',na=False)]
    del positive['Location']
    tested = tested.loc[0:].values.flatten().tolist()
    positive = positive.loc[0:].values.flatten().tolist()
    for i, j in zip(tested, positive):
        try:
            k.append(j/i * 100)
        except ZeroDivisionError:
            k.append(0)
    datasetxl = datasetxl.loc[:, ~datasetxl.columns.str.contains('^Unnamed',na=False)]
    del datasetxl['Location']
    dates = list(datasetxl.columns.values)
    data = {'Date':dates, 'Percent':k}
    data = pd.DataFrame(data)
    data = data.to_json(orient='records')
    return data