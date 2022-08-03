import pm4py
import pandas as pd
from dateutil.relativedelta import relativedelta
import sys


def create_model_matrix(resource_list, model_dictionary, matrix, data_extracted, replay_fitness_method):
    try:
        for i in range(len(resource_list)):
            resource_list[i] = resource_list[i].lower()
        data_resource = data_extracted[data_extracted['ResourceId'].isin(resource_list)]
        data_resource["FileId"] = data_resource[["UserId", "FileId"]].apply(lambda x: "/".join(x), axis=1)
        file_list = data_resource["FileId"].unique()
        matrix_list = []
        for file_id in file_list:
            data_file_filtered = data_resource[data_resource.FileId == file_id]
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
                data_to_mine = pm4py.format_dataframe(data_time_filtered, case_id='FileId',
                                                      activity_key='Operation', timestamp_key='Timestamp')
                current_event_log = pm4py.convert_to_event_log(data_to_mine)
                key = file_id + "/" + end_time
                resource_id = data_file_filtered.loc[data_file_filtered["FileId"] == file_id, 'ResourceId'].unique()
                fitness_list = [key, resource_id[0]]
                for traces, event_log in model_dictionary.items():
                    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
                    if replay_fitness_method.lower() == "token":
                        fitness = pm4py.fitness_token_based_replay(current_event_log, net, initial_marking,
                                                                   final_marking)
                    elif replay_fitness_method.lower() == "alignment":
                        fitness = pm4py.fitness_alignments(current_event_log, net, initial_marking, final_marking)
                    fitness_list.append(round(fitness['average_trace_fitness'], 3))
                matrix.loc[len(matrix)] = fitness_list
                trace_length = trace_length + len(trace)
                row_length = len(data_file_filtered.index)
                data_file_filtered = data_file_filtered.iloc[trace_length:row_length]
                matrix_list.append(fitness_list)
        return matrix
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in creating model matrix.")
