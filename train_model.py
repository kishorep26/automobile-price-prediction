import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('Automobile price data _Raw_.csv')

# Replace '?' with NaN
df = df.replace('?', np.nan)

# Handle missing values
# For numeric columns, fill with mean
numeric_cols = ['normalized-losses', 'bore', 'stroke', 'horsepower', 'peak-rpm', 'price']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].mean(), inplace=True)

# For categorical columns, fill with mode
categorical_cols = ['num-of-doors']
for col in categorical_cols:
    if col in df.columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

# Convert text numbers to numeric (manual mapping)
number_map = {
    'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 
    'eight': 8, 'twelve': 12
}

def convert_to_number(val):
    if isinstance(val, str):
        return number_map.get(val.lower(), val)
    return val

df['num-of-doors'] = df['num-of-doors'].apply(convert_to_number)
df['num-of-cylinders'] = df['num-of-cylinders'].apply(convert_to_number)

# Select features for the model
feature_columns = [
    'symboling', 'normalized-losses', 'wheel-base', 'length', 'width', 
    'height', 'curb-weight', 'engine-size', 'bore', 'stroke', 
    'compression-ratio', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg',
    'num-of-doors', 'num-of-cylinders'
]

# Encode categorical variables
label_encoders = {}
categorical_features = ['make', 'fuel-type', 'aspiration', 'body-style', 
                        'drive-wheels', 'engine-location', 'engine-type', 'fuel-system']

for col in categorical_features:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    feature_columns.append(col)

# Prepare features and target
X = df[feature_columns]
y = df['price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model (better performance)
model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R² Score: {train_score:.4f}")
print(f"Testing R² Score: {test_score:.4f}")

# Save the model and encoders
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

# Save feature columns
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

# Save statistics for the frontend
stats = {
    'train_score': train_score,
    'test_score': test_score,
    'feature_importance': dict(zip(feature_columns, model.feature_importances_)),
    'categorical_features': categorical_features,
    'numeric_features': [col for col in feature_columns if col not in categorical_features]
}

with open('model_stats.pkl', 'wb') as f:
    pickle.dump(stats, f)

print("\nModel and encoders saved successfully!")
print(f"Feature columns: {len(feature_columns)}")
