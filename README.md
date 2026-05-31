# Flask POC 1

A minimal Flask backend that serves static files and exposes a `/calculate-risk` API.

## Run locally

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python PythonCode.py
```

The API will be available at `http://127.0.0.1:5000/calculate-risk` and the site at `http://127.0.0.1:5000/`.

## Deploy to Render

1. Push this repository to GitHub/GitLab.
2. Create a new Web Service on Render and connect your repo.
3. Use the following settings:
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn PythonCode:app --bind 0.0.0.0:$PORT`

You can set the service ID to `srv-d8e2o4v7f7vs73cofong` if you want to target the existing service `flask-poc-1`.
