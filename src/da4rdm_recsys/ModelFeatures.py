import pandas as pd
import pm4py
from dateutil.relativedelta import relativedelta
from da4rdm_recsys.ModelMatrix import create_model_matrix
from da4rdm_recsys.Conformance import check_conformance
from da4rdm_recsys.Extract import extract_data
import sys


# The below function creates different process models for the selected resource
def create_model_features(dataset_user_interactions, key_resource, resource_list, replay_fitness_method):
    data_extracted = extract_data(dataset_user_interactions)
    data_extracted = data_extracted[data_extracted.FileId.notnull()]
    data_extracted = data_extracted[["UserId", "ResourceId", "FileId", "Operation", "Timestamp"]]
    data_resource_filtered = data_extracted[data_extracted['ResourceId'] == key_resource.lower()]
    if data_resource_filtered.empty:
        sys.exit("There were no records retrieved for the key resource")
    data_resource_filtered["FileId"] = data_resource_filtered[["UserId", "FileId"]].apply(lambda x: "/".join(x), axis=1)
    event_log_dictionary = {}
    file_list = data_resource_filtered["FileId"].unique()
    try:
        for file_id in file_list:
            data_file_filtered = data_resource_filtered[data_resource_filtered.FileId == file_id]
            data_file_filtered = data_file_filtered[["ResourceId", "FileId", "Operation", "Timestamp"]]
            data_file_filtered = data_file_filtered.sort_values(['Timestamp'], ascending=True)
            while len(data_file_filtered.Operation.value_counts()) > 0:
                trace_length = 0
                start_time = data_file_filtered['Timestamp'].iloc[0]
                added_time_window = pd.to_datetime(start_time) + relativedelta(minutes=+15)
                end_time = added_time_window.strftime('%Y-%m-%d %H:%M:%S.%f')
                data_time_filtered = data_file_filtered.loc[(data_file_filtered['Timestamp'] >= start_time) &
                                                            (data_file_filtered['Timestamp'] <= end_time)]
                trace = data_time_filtered["Operation"].to_list()
                trace_name = ' '.join(trace)
                data_to_mine = pm4py.format_dataframe(data_time_filtered, case_id='FileId',
                                                      activity_key='Operation', timestamp_key='Timestamp')
                current_event_log = pm4py.convert_to_event_log(data_to_mine)
                flag = 0
                '''
                The below lines of code loops over the stored event logs and checks if the current 
                event log is existing in the trace dictionary. It first creates a process model for each existing event
                log in trace dictionary and replays the current event log over the process model. If the fitness is same
                then the log is not added to trace dictionary, if different it adds the event log.
                '''
                for traces, log in event_log_dictionary.items():
                    trace_is_fit = check_conformance(log, current_event_log, replay_fitness_method)
                    if trace_is_fit:
                        flag = 1
                        break
                if flag == 0:
                    event_log_dictionary.update({trace_name: current_event_log})
                trace_length = trace_length + len(trace)
                row_length = len(data_file_filtered.index)
                data_file_filtered = data_file_filtered.iloc[trace_length:row_length]
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + "occurred. Error in creating model feature")
    matrix_columns = ["Key", "Resource"]
    for trace, event_log in event_log_dictionary.items():
        matrix_columns.append(trace)
    data_matrix = pd.DataFrame(columns=[matrix_columns])
    try:
        model_matrix = create_model_matrix(resource_list, event_log_dictionary, data_matrix, data_extracted,
                                           replay_fitness_method)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error retrieving matrix data based on traces")
    return model_matrix
