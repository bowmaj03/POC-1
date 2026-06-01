# Step-by-Step: Deploy Flask POC 1 to Render

## Project Overview

**Flask POC 1** is a lightweight web application combining:
- **Backend**: Flask Python server that serves both static files and a REST API
- **Frontend**: HTML/CSS/JS pages (index.html, risk.html, about.html, etc.)
- **API Endpoint**: `/calculate-risk` – calculates risk scores based on likelihood and impact

**Architecture**:
```
User Browser
    ↓
Render (Web Service) runs gunicorn
    ↓
PythonCode.py (Flask app)
    ├── Serves static files (index.html, risk.html, app.js, etc.)
    └── Exposes /calculate-risk API endpoint
```

**Key Files**:
- `PythonCode.py` – Main Flask application with static file serving
- `requirements.txt` – Python dependencies (Flask, Gunicorn)
- `Procfile` – Render startup command (tells Render how to launch the app)
- `render.yaml` – Optional Render configuration file
- `app.js` – Frontend JavaScript (calls the risk calculation API)
- `risk.html` – Risk analysis page with "Calculate Risk" button
- `DEPLOY_RENDER.md` – This deployment guide

## Prerequisites

- **GitHub or GitLab account** (to host your repository)
  - Render will clone your repo, so code must be version-controlled
- **Render account** (free tier available at https://render.com)
  - Free tier includes one free web service with auto-sleep after 15 min of inactivity
- **Git installed locally** (https://git-scm.com/download/win for Windows)
  - Required to push code from your machine to GitHub
- **Your code repository** (already initialized in `c:\Development Work\POC 1`)
  - Contains all files needed for deployment

## Step 1: Prepare Your Local Repository

**Purpose**: Git tracks your code and allows Render to pull it during deployment. This step ensures all files are properly versioned.

### 1.1 Initialize Git (if not already done)

**What it does**: Creates a `.git` folder to track code changes locally.

```bash
cd "c:\Development Work\POC 1"
git init
git add .
git commit -m "Initial commit: Flask POC with static site serving"
```

**Expected output**:
```
Initialized empty Git repository in c:/Development Work/POC 1/.git/
[main (root-commit) abc1234] Initial commit: Flask POC with static site serving
 8 files changed, 2000 insertions(+)
```

### 1.2 Create a `.gitignore` file

**Purpose**: Prevents large/sensitive files from being pushed to GitHub.

Create file: `c:\Development Work\POC 1\.gitignore`

```
.venv/
__pycache__/
*.pyc
*.pyo
.env
.DS_Store
*.egg-info/
dist/
build/
```

**Why these files?**:
- `.venv/` – Virtual environment (~100+ MB, regenerated on Render)
- `__pycache__/` – Python compiled bytecode (auto-generated)
- `.env` – Secrets like API keys (should never be in Git)

### 1.3 Verify Required Files Exist

**Location**: All should be in `c:\Development Work\POC 1\`

| File | Purpose | Status |
|------|---------|--------|
| `PythonCode.py` | Flask app - serves HTML and `/calculate-risk` API | ✓ Created |
| `requirements.txt` | Lists Python packages: Flask, Gunicorn | ✓ Created |
| `Procfile` | Tells Render how to start: `web: gunicorn PythonCode:app --bind 0.0.0.0:$PORT` | ✓ Created |
| `render.yaml` | Optional Render config with service ID | ✓ Created |
| `index.html` | Home page | ✓ Original |
| `risk.html` | Risk calculation page with button | ✓ Original |
| `app.js` | JavaScript that calls `/calculate-risk` API | ✓ Original |
| `about.html` | About page | ✓ Original |
| `services.html` | Services page | ✓ Original |
| `contact.html` | Contact page | ✓ Original |
| `home.html` | Home page alternate | ✓ Original |

**Verify all files are tracked**:

```bash
git status
```

**Expected output**:
```
On branch main
nothing to commit, working tree clean
```

If you see "Untracked files" or "Changes not staged", run:

```bash
git add .
git commit -m "Add all project files"
```

## Step 2: Push to GitHub or GitLab

### 2.1 Create a repository on GitHub

1. Go to https://github.com/new
2. Name it (e.g., `flask-poc-1`)
3. Do NOT initialize with README (you have local files)
4. Click "Create repository"

### 2.2 Link and push your local repo

Copy the HTTPS URL from GitHub (looks like `https://github.com/YOUR_USERNAME/flask-poc-1.git`), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/flask-poc-1.git
git branch -M main
git push -u origin main
```

Verify on GitHub that all files are there.

## Step 3: Connect Render to Your Repository

### 3.1 Sign up or log in to Render

Go to https://render.com and create/log into your account.

### 3.2 Create a new Web Service

1. Click **+ New** → **Web Service**
2. Click **Connect a repository**
3. Authorize Render to access your GitHub/GitLab account
4. Select your repository (e.g., `flask-poc-1`)
5. Click **Connect**

## Step 4: Configure the Service

### 4.1 Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `flask-poc-1` |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you (e.g., `Ohio` for US East) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn PythonCode:app --bind 0.0.0.0:$PORT` |

### 4.2 Advanced Settings (optional)

- **Auto-Deploy**: Toggle **ON** to auto-deploy on every Git push
- **Health Check Path**: `/` (or leave blank)
- **Environment Variables**: Leave empty for now (add API keys/secrets here if needed)

### 4.3 Plan

- Free tier is fine for testing
- Upgrade later if needed

## Step 5: Deploy

### 5.1 Click Deploy

Once settings are configured, click the **Deploy** button at the bottom right.

### 5.2 Monitor Build Logs

Render will:

1. Clone your repository
2. Run `pip install -r requirements.txt`
3. Start the app with `gunicorn PythonCode:app --bind 0.0.0.0:$PORT`

Watch the logs panel on the left. You should see:

```
Build started...
Building in /var/task/src...
Running pip install...
Build succeeded.
Service is running at https://flask-poc-1.onrender.com
```

### 5.3 Access Your App

Once deployed, your app is available at:

```
https://flask-poc-1.onrender.com
```

Click the link or visit the URL to see your site.

## Step 6: Test Your App

### 6.1 Visit the home page

```
https://flask-poc-1.onrender.com/
```

You should see `index.html`.

### 6.2 Test the Risk page

```
https://flask-poc-1.onrender.com/risk.html
```

Click **Calculate Risk** button. It should call the Flask API and display results.

## Step 7: Troubleshooting

### Issue: Build fails with "No such file or directory"

**Solution**: Ensure all files are pushed to Git. Run:

```bash
git status
git add .
git commit -m "Add missing files"
git push
```

### Issue: App crashes after deploy

**Check logs on Render**:

1. Go to your service on Render
2. Click **Logs** tab
3. Look for error messages
4. Common issues:
   - Missing `Procfile`
   - Wrong start command in `Procfile`
   - Missing dependencies in `requirements.txt`

### Issue: Static files return 404

**Ensure** all `.html`, `.js`, and `.css` files are:

1. In the repo root directory
2. Pushed to GitHub
3. Listed in Render's file explorer

### Issue: API calls fail (CORS errors)

**Solution**: `PythonCode.py` already has CORS headers. If issues persist:

1. Open browser DevTools (F12)
2. Check Network tab for failed requests
3. Verify the URL matches your Render domain

## Step 8: Update and Redeploy

To deploy changes:

```bash
# Make changes locally
git add .
git commit -m "Fix or add feature"
git push origin main
```

If auto-deploy is enabled, Render will automatically rebuild and restart your app. Otherwise, click **Manual Deploy** on the Render dashboard.

## Step 9: Custom Domain (Optional)

To use your own domain:

1. On Render, go to your service → **Settings**
2. Scroll to **Custom Domain**
3. Enter your domain (e.g., `flask-poc-1.example.com`)
4. Follow DNS instructions from your domain provider
5. Update your HTML/JS to use the new domain if needed

## Helpful Links

- [Render Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Gunicorn Docs](https://gunicorn.org/)
- [GitHub Desktop](https://desktop.github.com/) (easier UI if Git CLI is unfamiliar)
