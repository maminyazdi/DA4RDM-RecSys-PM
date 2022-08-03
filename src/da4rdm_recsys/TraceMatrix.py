import numpy as np
import sys


def create_trace_matrix(feature_dictionary, trace_matrix):
    try:
        for file_id, trace_dict in feature_dictionary.items():
            for key in trace_dict:
                if key in trace_matrix.columns:
                    trace_matrix[key].loc[trace_matrix['Key'] == file_id] = trace_dict[key]
                else:
                    trace_matrix[key] = np.where(trace_matrix['Key'] == file_id, trace_dict[key], 0)
        return trace_matrix
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in creating trace matrix.")

