# -*- coding: utf-8 -*-
"""Ridge.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uZf9f18c6vahUPqfcno3dFcrBfybuNyh
"""

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
# Importing Libraries
import pandas as pd
# Importing Imputer
from sklearn.impute import SimpleImputer
# import column transform
from sklearn.compose import ColumnTransformer
# importing encoders
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# importing pipeline
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

test_df = pd.read_csv('/content/test.csv')
train_df = pd.read_csv('/content/train.csv')
test_df

# removing colums in df
train_df = train_df.drop(["ID","Quarter"], axis=1)
train_df.dropna(subset=['Sales'], inplace=True)

imputer = SimpleImputer(strategy='mean')
train_df['InventoryRatio'] = imputer.fit_transform(train_df[['InventoryRatio']])

scaler = StandardScaler()
train_df['InventoryRatio'] = scaler.fit_transform(train_df[['InventoryRatio']])

imputer = SimpleImputer(strategy='mean')
test_df['InventoryRatio'] = imputer.fit_transform(test_df[['InventoryRatio']])

scaler = StandardScaler()
test_df['InventoryRatio'] = scaler.fit_transform(test_df[['InventoryRatio']])

columns = ['Bond rating', 'Stock rating', 'Region', 'Industry', 'Company']

# Extract the columns you want to encode
data = train_df[columns]

# Initialize the OneHotEncoder
encoder = OneHotEncoder(handle_unknown='ignore')

# Fit and transform the data
encoded_data = encoder.fit_transform(data)

# Convert the encoded data into a DataFrame
encoded_df = pd.DataFrame(encoded_data.toarray(), columns=encoder.get_feature_names_out(columns))

# Now 'encoded_df' contains the one-hot encoded columns

data_test = test_df[columns]

test_encoded = encoder.transform(data_test)

test_encoded_df = pd.DataFrame(test_encoded.toarray(), columns=encoder.get_feature_names_out(columns))

df = pd.concat([train_df.drop(columns=columns), encoded_df], axis=1)

df_test = pd.concat([test_df.drop(columns=columns), test_encoded_df], axis=1)

df

df_test

df['Company_CMP32'].head()

X = df.drop(columns=["Sales"])
Y = df["Sales"]

test_pred = df_test.drop(columns=["ID", "Quarter"])

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
alpha_values = [0.001, 0.01, 0.1, 1, 10, 100]

# Define the grid search parameters
param_grid = {'alpha': alpha_values}

ridge_estimator = Ridge()

model = GridSearchCV(ridge_estimator, param_grid, cv=5, scoring='r2')

model.fit(X_train, Y_train)

best_regressor = model.best_estimator_
print("Best hyperparameters:", model.best_params_)

train_score = best_regressor.score(X_train, Y_train)
print(f"Training R^2 score: {train_score:.2f}")
test_score = model.score(X_test, Y_test)
print(f"Testing R^2 score: {test_score:.2f}")

alpha_values = [0.1]

# Define the grid search parameters
param_grid = {'alpha': alpha_values}

ridge_estimator = Ridge()

model = GridSearchCV(ridge_estimator, param_grid, cv=5, scoring='r2')

model.fit(X,Y)

predictions = model.predict(test_pred)

sales = pd.DataFrame(predictions, columns=["Sales"])
result = pd.concat([test_df['ID'], sales], axis=1)
result.to_csv("submission.csv", index=False)

# Read submission data
submission_data = pd.read_csv('submission.csv')
submission_data