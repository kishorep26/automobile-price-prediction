# 🚀 Deployment Guide

## Deploy to Vercel (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Sign in with GitHub
3. Import: `kishorep26/automobile-price-prediction`
4. Click Deploy

Done! Live in 3-4 minutes.

---

## Deploy to Render

1. Go to [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Select repository
4. Configure:
   - Build: `./build.sh`
   - Start: `gunicorn app:app`
5. Deploy

---

## Local Development

```bash
pip install -r requirements.txt
python train_model.py
python generate_visualizations.py
python app.py
```

Visit: `http://localhost:5001`
