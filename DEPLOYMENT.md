# 🚀 Deployment Guide

## Quick Deploy to Render (Recommended)

1. **Sign up for Render**: Go to [render.com](https://render.com) and create a free account

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `kishorep26/automobile-price-prediction`
   - Configure:
     - **Name**: `automobile-price-prediction`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python generate_visualizations.py`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free

3. **Deploy**: Click "Create Web Service" and wait for deployment (5-10 minutes)

4. **Access**: Your app will be live at `https://automobile-price-prediction.onrender.com`

## Deploy to Heroku

1. **Install Heroku CLI**: 
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login and Create App**:
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

4. **Generate Visualizations** (one-time):
   ```bash
   heroku run python generate_visualizations.py
   ```

5. **Open App**:
   ```bash
   heroku open
   ```

## Deploy to Railway

1. **Sign up**: Go to [railway.app](https://railway.app)

2. **New Project**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `kishorep26/automobile-price-prediction`

3. **Configure**:
   - Railway auto-detects Python
   - Add build command: `python generate_visualizations.py`
   - Start command: `gunicorn app:app`

4. **Deploy**: Automatic deployment starts

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python train_model.py

# Generate visualizations
python generate_visualizations.py

# Run locally
python app.py
# or
PORT=5001 python app.py
```

Visit: `http://localhost:5001`

## Environment Variables

No environment variables required! The app works out of the box.

## Troubleshooting

### Visualizations not showing
Run the visualization generation script:
```bash
python generate_visualizations.py
```

### Port already in use
Change the port:
```bash
PORT=8000 python app.py
```

### Model not found
Train the model first:
```bash
python train_model.py
```

## Features

✅ Random Forest ML model (93.4% accuracy)  
✅ Interactive web interface  
✅ Real-time predictions  
✅ Data visualizations & insights  
✅ Responsive design  
✅ No database required  

## Tech Stack

- **Backend**: Flask + scikit-learn
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Visualizations**: Matplotlib + Seaborn
- **Deployment**: Gunicorn WSGI server

---

**Need help?** Open an issue on [GitHub](https://github.com/kishorep26/automobile-price-prediction/issues)
