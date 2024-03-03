# CECALT (Center of meteorologiCAL Technology) 
This is an integral project whose objective is to increase the sensitivity of hurricane prediction systems. It contains all the code and data needed to deploy an end-to-end machine learning project on a running CML instance.

![CECALT_APP](static/CECALT.PNG)

The primary goal of this repository is to build a gradient boosted (XGBoost) classification model to predict the likelihood of a flight being canceled based on years of historical records. To achieve that goal, this project demonstrates the end-to-end processing needed to take a large, raw dataset and transform it into a clean, stripped down dataset for model training and inference using Spark on CML. Additionally, this project deploys a hosted model and front-end application to allow users to interact with the trained model. 

The dataset used in this project come from [Kaggle](https://www.kaggle.com/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018).

## Project Structure

The project is organized with the following folder structure:

```
.
├── app/            # Sources needed to launch the application
├── scripts/        # Scripts used for the creation and deploy of the end-to-end solution
├── src/            # All the prebuilt models and datasets necessary for the project
├── static/         # All images used in the project
├── README.md
├── Documentation.md
├── LICENSE.txt
└── requirements.txt

```

In case it is needed, a more accurate documentation i

We will focus our attention on working within CML, using all it has to offer, while glossing over the details that are simply standard data science, and in particular, pay special attention to data ingestion and processing at scale with Spark.

## Deploying on CML

There are three ways to launch the this prototype on CML:

1. **From Prototype Catalog** - Navigate to the Prototype Catalog on a CML workspace, select the "Airline Delay Prediction" tile, click "Launch as Project", click "Configure Project"
2. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/cloudera/CML_AMP_Canceled_Flight_Prediction), click "Create Project", click "Configure Project"

3. **Manual Setup** - In a CML workspace, click "New Project", add a Project Name, select "Git" as the Initial Setup option, copy in the [repo URL](CML_AMP_Canceled_Flight_Prediction), click "Create Project". Then, follow the steps listed [in this document](code/README.md) in order

If you deploy this project as an Applied ML Prototype (AMP) (options 1 or 2 above), you will need to specify whether to run the project with `STORAGE_MODE` set to `local` or `external`. Running in external mode requires having access to a Virtual Warehouse that has the flights dataset available. Running in local mode will bypass the data access and manipulation steps by using the `data/preprocessed_flight_data.tgz` file to train a model and deploy the application. While running the project as an AMP will install, setup, and build all project artifacts for you, it may still be instructive to review the documentation and files in the [code](code/) directory.


----
### **Note**
This project may fail to complete automated setup on a CML workspace for certain hardware configurations.  If this happens, simply follow the **Manual Setup** steps above to enable the project artefacts. 
