# da4rdm-recsys

## Description
The da4rdm-recsys is a python based package that allows retreiving recommendation based on the resource interaction pattern analyzed based on either trace or model approach. Normalized similarity based distance information can be extracted and vizualized. 


## Installation
The package is built using Python as a programming language and utilizes basic python packages. It uses the visualization package matplotlib . Please make sure the necessary packages are installed before execution. Few other packages include sklearn, scipy, seaborn, json etc. The test package can be installed using the pip command provided below.

pip install -i https://test.pypi.org/simple/ da4rdm-recsys

## Usage and Examples
The package provides recommendation based on user inputs for the parameters.

Function Inputs:<br />
1. The function **get_model_based_recommendations** accepts three mandatory positional arguments namely the path for the event log, the resource data and the resource ID to be used as a key. The optional arguments include distance metric, the output formats and specifically for model approach the replay fitness method can be selected from the availabe option of alighnment and token.

Example Usage:<br />
Below is an execution of the function with all parameters provided.
```python
import da4rdm_recsys
from da4rdm_recsys import ModelRecommendation
ModelRecommendation.get_model_based_recommendations("21-06-2022.csv", "tomography.csv", "1faa54d3-122b-41fd-ace3-2b698fc1326f", "alignment", "euclidean", "csv")
````

Below is an execution of the function with only the required parameters provided.
```python
import da4rdm_recsys
from da4rdm_recsys import ModelRecommendation
ModelRecommendation.get_model_based_recommendations("21-06-2022.csv", "tomography.csv", "1faa54d3-122b-41fd-ace3-2b698fc1326f")
```
2. The function **get_trace_based_recommendations** accepts three mandatory positional arguments namely the path for the event log, the resource data and the resource ID to be used as a key. The optional arguments include distance metric and the oitput formats.

Example Usage:<br />
Below is an execution of the function with all parameters provided.
```python
import da4rdm_recsys
from da4rdm_recsys import TraceRecommendation
TraceRecommendation.get_trace_based_recommendations("21-06-2022.csv", "tomography.csv", "1faa54d3-122b-41fd-ace3-2b698fc1326f", "alignment", "euclidean", "csv")
```

## Project status
The project is currently in test phase.

