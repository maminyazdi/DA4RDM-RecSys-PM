## Research Data Reusability with Modeling User Interaction Process Models
## Description
The da4rdm-recsys is a python based package that allows retreiving recommendation based on the resource interaction pattern analyzed based on either trace or process model approach. Normalized similarity based distance information can be extracted and vizualized. 

## Features
- **Resource Interaction Analysis:** Leverages both trace and process model approaches.
- **Normalized Similarity-Based Distance Information:** Easily extract and visualize distance information.
- **Flexible Recommendation Generation:** Provides recommendations based on user-specified parameters.

## Installation
### Prerequisites
Ensure that you have the following Python packages installed before proceeding:

- `matplotlib`
- `sklearn`
- `scipy`
- `seaborn`
- `json`

### Installing da4rdm-recsys
You can install `da4rdm-recsys` using `pip` with the following command:

```bash
pip install -i https://test.pypi.org/simple/ da4rdm-recsys
```
### Usage
- get_model_based_recommendations Function:
    - Mandatory Arguments:
      - Event log path
      - Resource data
      - Resource ID (used as a key)
    - Optional Arguments:
      - Distance metric
      - Output formats
      - Replay fitness method (for model approach only; choose between "alignment" and "token")
### Example
```bash
import da4rdm_recsys
from da4rdm_recsys import ModelRecommendation
ModelRecommendation.get_model_based_recommendations("SAMPLE_DATASET", "ResourceId")
```



## Project status
The is currently in the testing phase, and we appreciate your feedback to improve its functionality and performance.

