# CECALT (Center of meteorologiCAL Technology) 
This is an integral project whose objective is to increase the sensitivity of hurricane prediction systems. It contains all the code and data needed to deploy an end-to-end machine learning project on a running CML instance.

![CECALT_APP](static/CECALT.PNG)

The primary goal of this repository is to build a XXXXXXXXXXXXXXXXx model to predict the wind speed based on geographical and meteorological conditions, like in the following example: 

The dataset used in this project comes from [Kaggle](https://www.kaggle.com/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018) and de API Meteostat 

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

The file  `Documentation.doc` contains a deeper and more accurate walk-through of the project. 

## Deploying on CML

The ways of executing the project are the following ones: 

1. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/amcm329/cod_hurricane_prediction), click "Create Project", click "Configure Project"

3. **Manual Setup** - In a CML workspace, click "New Project", add a Project Name, select "Git" as the Initial Setup option, copy in the [repo URL](CECALT (Center of meteorologiCAL Technology) ), click "Create Project". Then, follow the steps listed [in this document](scripts/README.md) in order

In general, the project contains if-selse para una ejecución segura, aunque si surge algo, refierase a la documentación o al documento de ejecución
