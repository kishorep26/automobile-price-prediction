# 🚀 Deploy to Vercel - Quick Guide

## Option 1: One-Click Deploy (Easiest)

1. **Go to Vercel**: Visit [vercel.com](https://vercel.com)

2. **Sign Up/Login**: Use your GitHub account

3. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `kishorep26/automobile-price-prediction`
   - Click "Import"

4. **Configure Project**:
   - **Framework Preset**: Other
   - **Build Command**: `./build.sh`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

5. **Deploy**: Click "Deploy" and wait 2-3 minutes

6. **Done!** Your app will be live at: `https://automobile-price-prediction-[your-id].vercel.app`

---

## Option 2: Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
cd /Users/kishoreprashanth/Developer/automobile-price-prediction-main
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? automobile-price-prediction
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

---

## Important Notes

⚠️ **First Deployment**: The first build will take 3-5 minutes because it needs to:
- Install all Python dependencies
- Train the ML model
- Generate all visualizations

✅ **Subsequent Deployments**: Much faster (~1 minute)

🔄 **Auto-Deploy**: Every push to `main` branch will automatically deploy

📊 **Visualizations**: All charts are generated during build time

---

## Troubleshooting

### Build fails with "command not found"
Make sure `build.sh` is executable:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Model files not found
The build script automatically trains the model. If it fails:
1. Check Vercel build logs
2. Ensure all dependencies are in `requirements.txt`
3. Verify `train_model.py` runs locally

### Images not loading
Visualizations are generated during build. Check:
1. `generate_visualizations.py` runs without errors
2. `static/visualizations/` directory is created
3. All matplotlib/seaborn dependencies are installed

---

## Environment Variables (Optional)

No environment variables needed! The app works out of the box.

---

## Custom Domain (Optional)

1. Go to your Vercel project dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

---

## Your Deployment URLs

After deployment, you'll get:
- **Production**: `https://automobile-price-prediction.vercel.app`
- **Preview**: Unique URL for each commit
- **Development**: Local testing at `http://localhost:5001`

---

**Need help?** Check [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
