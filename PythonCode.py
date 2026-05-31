from flask import Flask, jsonify, request

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
