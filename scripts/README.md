# Project Build Process

In order to execute the module manually, follow these steps. It is important to mention that, inside each one of the codes, there are explanations and hints on how to properly execute them.

### 01 - Install dependencies

**Note**: this step *must* be executed in the beginning.

Open the file `01_install_dependencies.py` in a normal workbench Python3 session. A 1 CPU / 2 GB instance is enough. Then **Run > Run All Lines**

### 02 - Download and clean data (Optional)

Open the file `022_transform_and_load_data.py` in a normal workbench Python3 session. A 2 CPU / 4 GB instance is desirable. Then **Run > Run All Lines**

**Note:** this step relies on the API Meteostat and because of it, a lag might be present.

### 03 - Exploratory Data Analysis (Optional)

This is a Jupyter Notebook that does some basic data exploration and visualization. It is here to show how this would be part of the data science workflow.

Open a **JupyterLab** session: Python3, 2 CPU, 4 GB and open the `03_exploratory_data_analysis.ipynb` file. 

At the top of the page click **Cells > Run All**.

### 5 - Model Train

To run the model training process as a job, create a new job by going to the Project window and clicking _Jobs > New Job_ and entering the following settings:

* **Name** : Train Model

* **Script** : 04_train_model.py

* **Arguments** : _Leave blank_

* **Kernel** : Python 3

* **Schedule** : Manual

* **Engine Profile** : 2 vCPU / 4 GiB

  The rest can be left as is. Once the job has been created, click **Run** to start a manual run for that job.

  **Note:**: an environment flag ** ** is related to this process.


### 5 - Model Serve

The **[Models](https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-creating-and-deploying-a-model.html)** feature is used to deploy a machine learning model into production for real-time prediction. To deploy the model that was trained in the previous step: from  to the Project page, click **Models > New Model** and create a new model with the following details:

* **Name**: Flight Delay Prediction Model
* **Description**: This model API endpoint predicts flight delays
* **File**: 6_model_serve.py
* **Function**: predict_cancelled
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory

### 7 - Application

The next step is to deploy the Flask application with the **[Applications](https://docs.cloudera.com/machine-learning/cloud/applications/topics/ml-applications.html)** feature in CML. For this project it is used to deploy a web based application that interacts with the underlying model created in the previous step.

Go to the **Applications** section and select "New Application" with the following:

* **Name**: Airline Delay Prediction App
* **Subdomain**: delay-app
* **Script**: 7_application.py
* **Kernel**: Python 3
* **Engine Profile**: 1vCPU / 2 GiB Memory
* **Set Environment Variables**: Enter `SHTM_ACCESS_KEY` as the *Name* and the Access Key you copied from the Model Settings page as the *Value*. Click Add.

Then click "Create Application". After the Application deploys, click on the blue-arrow next to the name to launch the application in a new window.
