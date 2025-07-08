# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# Load the dataset
df = pd.read_csv('Salary_Data.csv')

# Handle missing values
df.dropna(inplace=True)

# Preprocessing
# Encode categorical variables
categorical_features = ['Gender', 'Education Level', 'Job Title']
one_hot = OneHotEncoder()
transformer = ColumnTransformer(
    [("one_hot", one_hot, categorical_features)],
    remainder="passthrough"
)

# Transform features
X = df.drop('Salary', axis=1)
y = df['Salary']
X_transformed = transformer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_transformed, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(f"MAE: {mean_absolute_error(y_test, y_pred)}")
print(f"MSE: {mean_squared_error(y_test, y_pred)}")
print(f"R2 Score: {r2_score(y_test, y_pred)}")

# Save model and preprocessor
with open('models/salary_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/preprocessor.pkl', 'wb') as f:
    pickle.dump(transformer, f)

print("Model and preprocessor saved successfully!")
