import pandas as pd
import json
import sys

"""
This function returns the dataframe extracted from the log files(specifically message part)
"""


def extract_data(data_path):

    try:
        df = pd.read_csv(data_path, sep=";")
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the path provided for the data")
    try:
        res = df.Message.apply(json.loads) \
            .apply(pd.json_normalize) \
            .pipe(lambda x: pd.concat(x.values))
        key_column_list = ['Type', 'Operation', 'Timestamp', 'UserId', 'ProjectId', 'ResourceId', 'FileId']
        dataframe = res[key_column_list]
        dataframe = dataframe[dataframe.FileId != '']
        dataframe['FileId'] = dataframe['FileId'].str.extract(r'([^/]+$)')
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the data format")
    return dataframe
