# CECALT Hurricane Behavior Predictor

CECALT **(CEnter of meteorologiCAL Technology)** is an integral project whose objective is to increase the sensitivity of hurricane prediction systems. It contains all the code and data needed to deploy an end-to-end machine learning project on a running CML instance.

![CECALT_APP](static/CECALT.PNG)

Its primary goal is to build an ensemble learning model that combines the predictors of three base models:

- Random Forest Regressor
- XGBoost Regressor
- Neuronal Network Regressor

To forecast the wind speed based on geographical and meteorological conditions, like in the following example: 

![CECALT_OUTPUT](static/CECALT_2.PNG)

The ensembling model uses a voting strategy to make its predictions, where each base model has an equal weight in the final prediction.

This model is trained on a dataset of wind speed data and evaluated using MSE (Mean Squared Error), MAE (Mean Absolute Error), R2 score and RMSE (Root Mean Square Error) metrics.

The dataset used in this project comes from the [National Hurricane Center](https://www.nhc.noaa.gov/) and the [Meteostat Project](https://meteostat.net/en/), with the aid of [analysis](scripts/exploratory_data_analysis.ipynb) and [transformations](scripts/transform_and_load_data.py).


## Project Structure

The project is organized with the following folder structure:

```
.
├── app/            # Sources needed to launch the application
├── scripts/        # Scripts used for the creation and deploy of the end-to-end solution
├── src/            # All the prebuilt models and datasets necessary for the project
├── static/         # All images used in the project
├── .gitignore
├── .project-metadata.yaml
├── CECALT Hurricane Behavior Predictor_SOP.pdf
├── LICENSE.txt
├── README.md
├── cdsw-build.sh  # This file is IMPORTANT for model deployment as additional libraries are installed here.
└── requirements.txt

```
The file  `CECALT Hurricane Behavior Predictor_SOP.pdf` contains a deeper walk-through of the project. 


## Deploying on Cloudera

The ways of executing the project are the following ones: 

1. **As AMP** - In a CML workspace, click "New Project", add a Project Name, select "AMPs" as the Initial Setup option, copy in the [repo URL](https://github.com/amcm329/cod_hurricane_prediction), click "Create Project", click "Configure Project"

2. **Manual Setup** - In a CML workspace, click "New Project", add a Project Name, select "Git" as the Initial Setup option, copy in the [repo URL](https://github.com/amcm329/cod_hurricane_prediction), click "Create Project". Then, follow the steps listed [in this document](scripts/README.md).

----
### **Note**
In general, the project contains mechanisms to guarantee a safe execution but if anything happens, it would be desirable to check both the [documentation](CECALT%20Hurricane%20Behavior%20Predictor_SOP.pdf) and the [technical configuration](scripts/README.md).

----
### **IMPORTANT**
DO NOT remove cdsw-build.sh as it will cause troubles in the model deployment.
