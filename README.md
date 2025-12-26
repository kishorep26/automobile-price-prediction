# Automobile Price Prediction

## Overview
A machine learning web application that predicts automobile prices based on vehicle specifications. The system uses a trained Random Forest Regressor model to provide accurate price estimates, helping buyers and sellers make informed decisions in the automotive market.

## Key Features
- ML-powered price prediction using Random Forest algorithm
- Interactive web interface for inputting vehicle specifications
- Real-time prediction results with confidence metrics
- Support for multiple vehicle attributes (make, model, year, mileage, fuel type)
- Data preprocessing and feature engineering pipeline
- Model training and evaluation metrics visualization

## Technology Stack
- Backend: Python, Flask
- ML Framework: scikit-learn, pandas, numpy
- Frontend: HTML, CSS, Bootstrap
- Model: Random Forest Regressor
- Data Processing: pickle for model serialization

## Getting Started
1. Install dependencies: pip install -r requirements.txt
2. Train the model: python train_model.py
3. Run the application: python app.py
4. Access the web interface at http://localhost:5000
5. Enter vehicle specifications and get instant price predictions

## Deployment
Suitable for deployment on platforms like Heroku, AWS, or Railway with Python runtime support.
