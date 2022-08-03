from dateutil.relativedelta import relativedelta
import pandas as pd
from da4rdm_recsys.TraceMatrix import create_trace_matrix
from da4rdm_recsys.Extract import extract_data
import sys


def create_trace_features(dataset_user_interactions, resource_list):
    data_extracted = extract_data(dataset_user_interactions)
    data_extracted = data_extracted[data_extracted.FileId.notnull()]
    data_extracted = data_extracted[["UserId", "ResourceId", "FileId", "Operation", "Timestamp"]]
    data_resource = data_extracted[data_extracted['ResourceId'].isin(resource_list)]
    data_resource["FileId"] = data_resource[["UserId", "FileId"]].apply(lambda x: "/".join(x), axis=1)
    if data_resource.empty:
        sys.exit("There were no records retrieved for the any of the resources")
    filelist = data_resource["FileId"].unique()
    resource_lists = []
    for val in filelist:
        resource_id = data_resource.loc[data_resource["FileId"] == val, 'ResourceId'].unique()
        resource_lists.append(resource_id[0])
    matrix_dictionary = {'Key': filelist, 'Resource': resource_lists}
    trace_matrix = pd.DataFrame(matrix_dictionary)

    trace_feature_dictionary = {}
    for resourceid in resource_list:
        try:
            data_resource_filtered = data_resource[data_resource.ResourceId == resourceid]
        except Exception as e:
            sys.exit("Oops! " + str(e.__class__) + "occurred. There were no records for resource " + str(resourceid))
        file_list = data_resource_filtered["FileId"].unique()
        try:
            for fileid in file_list:
                data_file_filtered = data_resource_filtered[data_resource_filtered.FileId == fileid]
                data_file_filtered = data_file_filtered[["ResourceId", "FileId", "Operation", "Timestamp"]]
                data_file_filtered = data_file_filtered.sort_values(['Timestamp'], ascending=True)
                trace_dictionary = {}
                while len(data_file_filtered.Operation.value_counts()) > 0:
                    trace_length = 0
                    start_time = data_file_filtered['Timestamp'].iloc[0]
                    added_time_window = pd.to_datetime(start_time) + relativedelta(minutes=+15)
                    end_time = added_time_window.strftime('%Y-%m-%d %H:%M:%S.%f')
                    data_time_filtered = data_file_filtered.loc[(data_file_filtered['Timestamp'] >= start_time) &
                                                            (data_file_filtered['Timestamp'] <= end_time)]
                    trace = data_time_filtered["Operation"].to_list()
                    trace_count = 1
                    trace_name = ' '.join(trace)
                    if trace_name in trace_dictionary.keys():
                        trace_count_old = trace_dictionary.get(trace_name)
                        trace_count = trace_count_old + trace_count
                    trace_dictionary.update({trace_name: trace_count})
                    trace_length = trace_length + len(trace)
                    row_length = len(data_file_filtered.index)
                    data_file_filtered = data_file_filtered.iloc[trace_length:row_length]
                trace_feature_dictionary.update({fileid: trace_dictionary})
        except Exception as e:
            sys.exit("Oops! " + str(e.__class__) + "occurred. Error in creating trace feature")
    try:
        matrix = create_trace_matrix(trace_feature_dictionary, trace_matrix)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error retrieving matrix data based on models")
    return matrix
