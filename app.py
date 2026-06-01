from flask import Flask, jsonify, request, send_from_directory, abort
import os

app = Flask(__name__)

def compute_risk(likelihood: float, impact: float) -> float:
    """Return a simple normalized risk score between 0 and 1."""
    return max(0.0, min(1.0, likelihood * impact))

def risk_level(score: float) -> str:
    if score >= 0.7:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/calculate-risk", methods=["GET"])
def calculate_risk():
    likelihood = request.args.get("likelihood", default=0.45, type=float)
    impact = request.args.get("impact", default=0.65, type=float)
    score = compute_risk(likelihood, impact)

    return jsonify({
        "likelihood": likelihood,
        "impact": impact,
        "risk_score": score,
        "risk_level": risk_level(score)
    })

# Serve static files (HTML/JS/CSS) from the project root so the same service
# can host the front-end and the API on Render.
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/<path:filename>", methods=["GET"])
def static_files(filename):
    # Prevent accidental exposure of Python files or API endpoints
    if filename.startswith("calculate-risk"):
        abort(404)

    allowed_ext = (".html", ".js", ".css", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_ext:
        abort(404)

    file_path = os.path.join(STATIC_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(STATIC_DIR, filename)
    abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
