'''
The below function provides recommendation based on trace interpretation. The distance metric parameter can be set to any
value accepted as per sklearn.metrics.DistanceMetric. The available output formats are "csv", "png", "jpeg", "pdf" and
"json". The defaults for these parameters can be
seen in the function definition. The required parameters are user interaction dataset and the
resource dataset along with the reference key resource.
'''

import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np
import seaborn as sns
import json
import sys
import matplotlib.pylab as plt
from da4rdm_recsys.TraceFeatures import create_trace_features


def normalize(df):
    result = df.copy()
    max_value = df['Distance'].max()
    min_value = df['Distance'].min()
    result['Distance'] = (df['Distance'] - min_value) / (max_value - min_value)
    return result


def get_trace_based_recommendations(dataset_user_interactions, dataset_resources, key_resource,
                                    distance_metric="Euclidean", output_format="csv"):
    if key_resource == "" or key_resource is None:
        sys.exit("Please provide a reference resource is for getting recommendations")
    try:
        resource_data = pd.read_csv(dataset_resources, sep='\|')
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the dataset path with resource information")
    resource_list = resource_data.Resource.unique()
    resource_list = resource_list.tolist()
    if resource_list is None:
        sys.exit("The dataset does not have any resource information")
    for i in range(len(resource_list)):
        resource_list[i] = resource_list[i].lower()
    if key_resource.lower() not in resource_list:
        resource_list.append(key_resource.lower())
    try:
        matrix_data = create_trace_features(dataset_user_interactions, resource_list)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. The matrix data could be not be retrieved")
    if matrix_data.empty:
        sys.exit("There are no records in the matrix data")
    try:
        data_filtered = matrix_data[matrix_data['Resource'] == key_resource.lower()]
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred.  Records could not be retrieved for the key resource")
    data_filtered = data_filtered.loc[:, ~data_filtered.columns.isin(['Key', 'Resource'])]
    try:
        K_means_var = KMeans(n_clusters=1).fit(data_filtered)
        centroid_key_resource = K_means_var.cluster_centers_
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in calculating centroid for the key resource")
    distance_dictionary = {}
    for resourceid in resource_list:
        data_resource_filtered = matrix_data[matrix_data.Resource == resourceid.lower()]
        data_resource_filtered = data_resource_filtered.loc[:,
                                 ~data_resource_filtered.columns.isin(['Key', 'Resource'])]
        if data_resource_filtered.empty:
            continue
        else:
            try:
                K_means_var = KMeans(n_clusters=1).fit(data_resource_filtered)
                centroid_resource = K_means_var.cluster_centers_
            except Exception as e:
                sys.exit("Oops! " + str(e.__class__) + " occurred. Error in calculating centroid for the resource "
                         + str(resourceid))
            try:
                k_euclid = cdist(centroid_resource, centroid_key_resource, metric=distance_metric.lower())
                distance = np.min(k_euclid, axis=1)
                distance_dictionary.update({resourceid: distance[0]})
            except Exception as e:
                sys.exit("Oops! " + str(e.__class__) + " occurred. Error in calculating distance for the resource "
                         + str(resourceid))
    recommendations = pd.DataFrame(list(distance_dictionary.items()), columns=['ResourceId', 'Distance'])
    recommendations = recommendations.sort_values(['Distance'], ascending=True, ignore_index=True)
    try:
        recommendations = normalize(recommendations)
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in normalizing centroid data")
    recommendations_wide = recommendations.pivot_table(columns='ResourceId', values='Distance')

    try:
        fig, ax = plt.subplots(figsize=(15, 30))
        sns.heatmap(recommendations_wide, annot=True, ax=ax)
        if output_format.lower() == "png":
            plt.savefig("Data/Outputs/Trace_Recommendations_Heatmap.png")
        elif output_format.lower() == "jpeg":
            plt.savefig("Data/Outputs/Trace_Recommendations_Heatmap.jpeg")
        elif output_format.lower() == "pdf":
            plt.savefig("Data/Outputs/Trace_Recommendations_Heatmap.pdf")
        elif output_format.lower() == "json":
            details = {
                'Recommendations': dict(ResourceID=recommendations['ResourceId'].to_list(),
                                        Distance=recommendations['Distance'].to_list()),
            }
            with open('Data/Outputs/Trace_Recommendations.json', 'w') as json_file:
                json.dump(details, json_file)
        elif output_format.lower() == "csv":
            recommendations.to_csv("Data/Outputs/Trace_Recommendations.csv")
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Error in saving results")


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
