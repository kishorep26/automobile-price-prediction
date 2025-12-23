from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the model and encoders
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

with open('model_stats.pkl', 'rb') as f:
    model_stats = pickle.load(f)

# Load original data for reference values
df = pd.read_csv('Automobile price data _Raw_.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Create feature array
        features = {}
        
        # Numeric features
        features['symboling'] = float(data.get('symboling', 0))
        features['normalized-losses'] = float(data.get('normalized_losses', 120))
        features['wheel-base'] = float(data.get('wheel_base', 98.8))
        features['length'] = float(data.get('length', 174.0))
        features['width'] = float(data.get('width', 65.9))
        features['height'] = float(data.get('height', 53.7))
        features['curb-weight'] = float(data.get('curb_weight', 2555))
        features['engine-size'] = float(data.get('engine_size', 127))
        features['bore'] = float(data.get('bore', 3.33))
        features['stroke'] = float(data.get('stroke', 3.25))
        features['compression-ratio'] = float(data.get('compression_ratio', 10.0))
        features['horsepower'] = float(data.get('horsepower', 104))
        features['peak-rpm'] = float(data.get('peak_rpm', 5125))
        features['city-mpg'] = float(data.get('city_mpg', 25))
        features['highway-mpg'] = float(data.get('highway_mpg', 31))
        features['num-of-doors'] = float(data.get('num_of_doors', 4))
        features['num-of-cylinders'] = float(data.get('num_of_cylinders', 4))
        
        # Categorical features - encode them
        categorical_mapping = {
            'make': data.get('make', 'toyota'),
            'fuel-type': data.get('fuel_type', 'gas'),
            'aspiration': data.get('aspiration', 'std'),
            'body-style': data.get('body_style', 'sedan'),
            'drive-wheels': data.get('drive_wheels', 'fwd'),
            'engine-location': data.get('engine_location', 'front'),
            'engine-type': data.get('engine_type', 'ohc'),
            'fuel-system': data.get('fuel_system', 'mpfi')
        }
        
        for col, value in categorical_mapping.items():
            try:
                features[col] = label_encoders[col].transform([value])[0]
            except:
                # If value not in encoder, use the most common value
                features[col] = 0
        
        # Create feature vector in correct order
        feature_vector = [features[col] for col in feature_columns]
        
        # Make prediction
        prediction = model.predict([feature_vector])[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction), 2),
            'currency': 'USD'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'train_score': model_stats['train_score'],
        'test_score': model_stats['test_score'],
        'top_features': sorted(
            model_stats['feature_importance'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
    })

@app.route('/api/options', methods=['GET'])
def get_options():
    """Get all unique values for categorical features"""
    options = {}
    
    categorical_features = ['make', 'fuel-type', 'aspiration', 'body-style', 
                           'drive-wheels', 'engine-location', 'engine-type', 'fuel-system']
    
    for feature in categorical_features:
        options[feature] = sorted(df[feature].unique().tolist())
    
    return jsonify(options)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
