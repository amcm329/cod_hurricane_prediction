# CECALT (Center of meteorologiCAL Technology) 
This is an integral project whose objective is to increase the sensitivity of hurricane prediction systems. It contains all the code and data needed to deploy an end-to-end machine learning project on a running CML instance.

![CECALT_APP](static/CECALT.PNG)

The primary goal of this repository is to build a XXXXXXXXXXXXXXXXx model to predict the wind speed based on geographical and meteorological conditions, like in the following example: 

![CECALT_OUTPUT](static/CECALT_2.PNG)

The data sources used in this project come from [National Hurricane Center](https://www.nhc.noaa.gov/) and the [Meteostat Project](https://meteostat.net/en/), with the aid of important analysis and transformations. 


## Project Structure

The project is organized with the following folder structure:

```
.
├── app/            # Sources needed to launch the application
├── scripts/        # Scripts used for the creation and deploy of the end-to-end solution
├── src/            # All the prebuilt models and datasets necessary for the project
├── static/         # All images used in the project
├── README.md
├── Documentation.doc
├── LICENSE.txt
└── requirements.txt

```

The file  `Documentation.doc` contains a deeper walk-through of the project. 

## Deploying on Cloudera

The ways of executing the project are the following ones: 

1. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/amcm329/cod_hurricane_prediction), click "Create Project", click "Configure Project"

3. **Manual Setup** - In a CML workspace, click "New Project", add a Project Name, select "Git" as the Initial Setup option, copy in the [repo URL](https://github.com/amcm329/cod_hurricane_prediction), click "Create Project". Then, follow the steps listed [in this document](scripts/README.md) in order

In general, the project contains mechanisms to guarantee a safe execution but if anything happens, it would be desirable to check both the documentation and the [technical configuration](scripts/README.md).
