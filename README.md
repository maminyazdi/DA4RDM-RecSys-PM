# da4rdm-recsys

## Description
The da4rdm-recsys is a python based package that allows retreiving recommendation based on the resource interaction pattern analyzed based on either trace or model approach. Normalized similarity based distance information can be extracted and vizualized. 


## Installation
The package is built using Python as a programming language and utilizes basic python packages. It uses the visualization package matplotlib . Please make sure the necessary packages are installed before execution. Few other packages include sklearn, scipy, seaborn,json etc. The test package can be installed using the pip command provided below.

pip install -i https://test.pypi.org/simple/ da4rdm-recsys

## Usage and Examples
The package provides recommendation based on user inputs for the parameters.

Function Inputs:<br />
The function **get_model_based_recommendations** accepts three mandatory positional arguments namely the path for the event log, the resource data and the Resource ID to be used as a key. The optional arguments include distance metric, the oitput formats and specifically for model approach the replay fitness method can be selected from the availabe option of alighnment and token.

```

Example Usage:<br />
Below is an execution of the function with all parameters provided.
```python
import da4rdm_recsys
from da4rdm_recsys import ModelRecommendation
ModelRecommendation.get_model_based_recommendations("21-06-2022.csv", "tomography.csv",


2. Generating vizualizations or transforming the correlation data retreived using the eval_corr function as discussed in the sections above. To get a vizualization of the results the **visualize** function within the module Vizualize should be used.

Function Inputs:
 This function accepts a dataframe with correlation data and a vizualization format as required parameters and provides relevant visualizazio. The user can choose from the various allowed formats such are jpeg, png, pdf and json. If a user selects the format as jpeg, png or pdf, the result is a RadarChart vizualization of the correlation data. Please refer below for examples.

Example Usage:<br />
Below is an execution of the function with all parameters provided.
```python
from da4rdm_vis import Evaluate

correlation = Evaluate.eval_corr("RDM_lifecycle_analysis_-_28-04-2022.csv", 'BA1FD94A-CC71-4D32-80AE-67DD2C3BF19A')
Visualize.visualize(correlation, 'jpeg')
```

## Project status
The project is currently in test phase.

