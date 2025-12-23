# 🚀 Deploy to Render

## Quick Deploy (5 minutes)

1. **Go to Render**: [render.com](https://render.com)

2. **Sign up** with GitHub

3. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect repository: `kishorep26/automobile-price-prediction`

4. **Configure**:
   - **Name**: `automobile-price-prediction`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python train_model.py && python generate_visualizations.py`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

5. **Deploy**: Click "Create Web Service"

⏱️ First deployment takes 5-7 minutes (installs ML libraries, trains model, generates charts)

✅ Your app will be live at: `https://automobile-price-prediction.onrender.com`

---

## Why Render (not Vercel)?

- ✅ No size limits for ML dependencies
- ✅ Free tier includes 512MB RAM
- ✅ Perfect for scikit-learn, pandas, matplotlib
- ✅ Persistent storage for model files

---

## Local Development

```bash
pip install -r requirements.txt
python train_model.py
python generate_visualizations.py
python app.py
```

Visit: `http://localhost:5001`

---

## Troubleshooting

**Build fails?**
- Check build logs in Render dashboard
- Ensure all dependencies in `requirements.txt`

**App crashes?**
- Increase instance RAM in settings
- Check application logs

**Slow first load?**
- Free tier spins down after inactivity
- First request takes 30-60 seconds to wake up
