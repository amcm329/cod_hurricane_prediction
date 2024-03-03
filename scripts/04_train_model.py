"""
In this code both the Feature Engineering and the Training steps take place.
"""

#---------------------------------------------------------
################### Variables section ####################
#---------------------------------------------------------

import os

full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"

import joblib   
import pandas as pd
import xgboost as xgb
from sklearn.pipeline import Pipeline
from sklearn.decomposition import  PCA
from sklearn.ensemble import VotingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

input = os.getenv("OPERATING_SYSTEM_PATH") + "src/data/semi_raw_meteorological_dataset.csv"
pipeline_file = os.getenv("OPERATING_SYSTEM_PATH") + "src/models/pipeline.pkl"
ensemble_model3_file = os.getenv("OPERATING_SYSTEM_PATH") + "src/models/ensemble_model3.pkl"

#---------------------------------------------------------
############### Feature Engineering section ##############
#---------------------------------------------------------

# Reading dataframe.
df = pd.read_csv(input)

# Separating features and target.
df=df.fillna(0)
X = df.drop(['wind_speed','sequential_id','name','timestamp_utc','closest_stations'], axis=1)
y= df['wind_speed']

# Splitting data.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

# Creating the pipeline
pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('selector', SelectKBest(mutual_info_regression, k=10)),
    ('pca', PCA(n_components=0.95))
])

# Fitting the pipeline to the training data.
X_train_transformed = pipeline.fit_transform(X_train,y_train)

# Transforming the test data using the fitted pipeline.
X_test_transformed = pipeline.transform(X_test)

X_train_transformed_df = pd.DataFrame(X_train_transformed)

# Saving current training_set to the respective folder.
X_train_transformed_df.to_csv( os.getenv("OPERATING_SYSTEM_PATH") + "src/data/X_train_selected_reduced.csv", index=False)

#---------------------------------------------------------
#################### Training section ####################
#---------------------------------------------------------

# Combining Random Forest, XGB and SNN to predict wind speed in X_train_selected_reduced.

# Define the Random Forest model.
rf_model = RandomForestRegressor(n_estimators=100, min_samples_split=2, min_samples_leaf= 2,random_state=42)

# Defining the XGB model.
xgb_model = xgb.XGBRegressor(subsample= 0.7, n_estimators=200, min_child_weight=5, max_depth=41, learning_rate=0.1, colsample_bytree=0.7,random_state=42)

# Defining the neural network model.
nn_model = MLPRegressor(hidden_layer_sizes=(500,), activation='relu', solver='adam',max_iter=500)

# Combining the models using an ensemble method.
ensemble_model3 = VotingRegressor(estimators=[('rf', rf_model), ('xgb', xgb_model),('nn', nn_model)])

# Training the ensemble model.
ensemble_model3.fit(X_train_transformed, y_train)

# Making predictions.
y_pred = ensemble_model3.predict(X_train_transformed)

# Evaluating the model with training dataset.
print("Mean squared error:", mean_squared_error(y_train, y_pred))
print("Mean absolute error:", mean_absolute_error(y_train, y_pred))
print("R2 score:", r2_score(y_train, y_pred))
print("RMSE :", np.sqrt(mean_squared_error(y_train, y_pred)))

#---------------------------------------------------------
#################### Testing section #####################
#---------------------------------------------------------

# Evaluating the model with testing dataset.
y_pred_test = ensemble_model3.predict(X_test_transformed)
print("Mean squared error:", mean_squared_error(y_test, y_pred_test))
print("Mean absolute error:", mean_absolute_error(y_test, y_pred_test))
print("R2 score:", r2_score(y_test, y_pred_test))
print("RMSE :", np.sqrt(mean_squared_error(y_test, y_pred_test)))

#---------------------------------------------------------
#################### Saving section #####################
#---------------------------------------------------------

# Saving both pipeline and model objects. 
joblib.dump(pipeline, pipeline_file)
joblib.dump(ensemble_model3, ensemble_model3_file)
