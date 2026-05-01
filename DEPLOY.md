# Deployment Instructions

## Option 1: Railway (Recommended - Easiest)
1. Push this repository to GitHub
2. Go to https://railway.app and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Your app will be live at: `https://your-app.up.railway.app`

**Environment Variables** (set in Railway dashboard):
- None required - app works out of the box

## Option 2: Render
1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Name**: any name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Deploy

## Option 3: PythonAnywhere (Free tier)
1. Create account at https://pythonanywhere.com
2. Upload files via dashboard
3. Create a new web app → Manual setup → Python 3.10
4. Edit WSGI config to point to `app:app`
5. Reload web app

---

## GitHub Pages Note
This is a Flask backend app with a database - it **cannot** run on GitHub Pages (static hosting only). The GitHub Pages site shows a message directing users to the live deployed app.
