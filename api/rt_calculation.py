import pandas as pd
import numpy as np
from . import rt_data_processing as rf
import logging
from IPython.display import clear_output
from django.contrib.staticfiles import finders
import re


def get_new_data():
    fileLoc = "static/data/newData.csv"
    datasetx = pd.read_csv(fileLoc)
    listing = datasetx.dis_name.unique()
    resultFinal = ""
    for elem in listing:
        dataset = datasetx.loc[datasetx['dis_name'] == elem]
        dataset['Date'] = pd.to_datetime(dataset['tdate'])
        dataset = dataset.sort_values(by='Date')
        dataSeries = pd.Series(dataset['positive_cases'].values, index=dataset['Date'])
        dataSeries = dataSeries.sort_index()
        dataSeries = dataSeries.cumsum()
        try:
            pd.to_numeric(dataSeries, errors="coerce")
            R_T_MAX = 12
            r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)
            GAMMA = 1/7
            original, smoothed = rf.prepare_cases(dataSeries)
            posteriors, log_likelihood = rf.get_posteriors(smoothed, GAMMA, r_t_range, sigma=.25)
            sigmas = np.linspace(1/20, 1, 20)
            new, smoothed = rf.prepare_cases(dataSeries, cutoff=5)
            if len(smoothed) == 0:
                new, smoothed = rf.prepare_cases(dataSeries, cutoff=10)
            result = {}
            result['posteriors'] = []
            result['log_likelihoods'] = []
            for sigma in sigmas:
                posteriors, log_likelihood = rf.get_posteriors(smoothed, GAMMA, r_t_range, sigma=sigma)
                result['posteriors'].append(posteriors)
                result['log_likelihoods'].append(log_likelihood)
            clear_output(wait=True)
            sigma = sigmas[np.argmax(result['log_likelihoods'])]
            posteriors = result['posteriors'][np.argmax(result['log_likelihoods'])]
            logging.debug(f"Sigma: {sigma} has highest log likelihood")
            logging.debug('Done.')
            hdis = rf.highest_density_interval(posteriors, p=.9)
            most_likely = posteriors.idxmax().rename('ML')
            result = pd.concat([most_likely, hdis], axis=1)
            result['district'] = elem
            result = result.reset_index().to_json(orient='records')
            resultFinal += result
        except IndexError:
            pass
    resultFinal = resultFinal.replace("[","")
    resultFinal = resultFinal.replace("]",",")
    resultFinal = resultFinal[:-1]
    resultFinal = "["+resultFinal+"]"
    return resultFinal

def get_data():
    fileLoc  = "https://gitlab.com/api/v4/projects/18229284/repository/files/Pipilika_Coronavirus_cases.xlsx/raw?ref=NewUpdate"
    sheetLoc = "Sheet1"
    datasetxl = rf.prepare_data(fileLoc, sheetLoc)
    resultFinal = ""
    for column in datasetxl:
        try:
            if(column != "Date"):
                dataSeries = pd.Series(datasetxl[column].values, index=datasetxl['Date'])
                pd.to_numeric(dataSeries, errors="coerce")
                R_T_MAX = 12
                r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)
                GAMMA = 1/7
                original, smoothed = rf.prepare_cases(dataSeries)
                posteriors, log_likelihood = rf.get_posteriors(smoothed, GAMMA, r_t_range, sigma=.25)
                sigmas = np.linspace(1/20, 1, 20)
                new, smoothed = rf.prepare_cases(dataSeries, cutoff=5)
                if len(smoothed) == 0:
                    new, smoothed = rf.prepare_cases(dataSeries, cutoff=10)
                result = {}
                result['posteriors'] = []
                result['log_likelihoods'] = []
                for sigma in sigmas:
                    posteriors, log_likelihood = rf.get_posteriors(smoothed, GAMMA, r_t_range, sigma=sigma)
                    result['posteriors'].append(posteriors)
                    result['log_likelihoods'].append(log_likelihood)
                clear_output(wait=True)
                sigma = sigmas[np.argmax(result['log_likelihoods'])]
                posteriors = result['posteriors'][np.argmax(result['log_likelihoods'])]
                logging.debug(f"Sigma: {sigma} has highest log likelihood")
                logging.debug('Done.')
                hdis = rf.highest_density_interval(posteriors, p=.9)
                most_likely = posteriors.idxmax().rename('ML')
                result = pd.concat([most_likely, hdis], axis=1)
                result['district'] = column
                result = result.reset_index().to_json(orient='records')
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