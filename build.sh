#!/bin/bash
# Build script for Render deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Training model..."
python train_model.py

echo "Generating visualizations..."
python generate_visualizations.py

echo "Build complete!"
