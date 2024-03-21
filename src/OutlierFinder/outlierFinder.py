from io import BytesIO
import json
import os

from pandas import read_csv

from OutlierFinder.core.crawler import CSV_KEYS, RELEVANT_JSON_KEYS
from OutlierFinder.core.outlier_detection import *
from OutlierFinder.core.preprocessing import *
from OutlierFinder.core.variables import *

from scipy import stats


def write_summary(algo, params, features_mode, path):
    with open(path + "/summary.txt", 'a+') as file:
        file.write('###' + algo + '###' + '\n')
        file.write('# features mode: ' + FEATURE_MODES_STR[features_mode] + "\n")
        file.write('# model params:\n')
        for k, v in params.items():
            file.write('\t' + str(k) + ' >>> ' + str(v) + '\n')
        file.write('\n')


def start_LOF(matchesJson):
    matchesAsCsv = matchJsonsToCsv(matchesJson)
    df = preprocess_data(targetCsv=matchesAsCsv, features_mode=COUNT_ONLY)
    df_pred, _ = classify_outliers(df, algorithm=LOF, model_params=lof_opt_model_params)
    
    outlierIds = df_pred.query('outlier == -1').get('id').tolist()

    if(len(outlierIds) >= 10):
        outlierIds = outlierIds[:10]

    return outlierIds


def start_IF(matchesJson):
    matchesAsCsv = matchJsonsToCsv(matchesJson)
    df = preprocess_data(targetCsv=matchesAsCsv, features_mode=COUNT_ONLY)
    df_pred, _ = classify_outliers(df, algorithm=IF, model_params=if_opt_model_params)

    outlierIds = df_pred.query('outlier == -1').get('id').tolist()

    if(len(outlierIds) >= 10):
        outlierIds = outlierIds[:10]

    return outlierIds


def matchJsonsToCsv(matchesJson):
    csvFileBuffer = BytesIO()
    csv_header = ','.join(CSV_KEYS) + '\n'
    csvFileBuffer.write(str.encode(csv_header))

    for json_sample in matchesJson:
        line = ''
        for key in RELEVANT_JSON_KEYS:
            if isinstance(json_sample[key], list):
                if 'pass_chains' in key:
                    line += str(len(json_sample[key])) + ','
                    continue

                if len(json_sample[key]) == 0:
                    json_sample[key] = [0]
                    count = 0

                else:
                    count = len(json_sample[key])

                mean = np.mean(json_sample[key])
                skew = stats.skew(json_sample[key])
                kurtosis = stats.kurtosis(json_sample[key])
                var = np.var(json_sample[key])
                median = np.median(json_sample[key])

                line += ','.join([str(val) for val in [mean, skew, kurtosis, var, median, count]]) + ','

            else:
                line += str(json_sample[key]) + ','

        csvFileBuffer.write(str.encode(line[:-1] + '\n'))
    
    # To make pandas be able to read the csv from the bytebuffer we need to set the filepointer back to the start of the file
    csvFileBuffer.seek(0)
    return read_csv(csvFileBuffer)