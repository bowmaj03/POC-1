from flask import Flask, jsonify, request, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Risk(db.Model):
    __tablename__ = 'risk_register'
    id = db.Column(db.Integer, primary_key=True)
    risk_name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'risk_name': self.risk_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

with app.app_context():
    db.create_all()
    if Risk.query.filter_by(risk_name='Fuel Pump Failure').first() is None:
        db.session.add(Risk(risk_name='Fuel Pump Failure'))
        db.session.commit()

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

@app.route("/api/risks", methods=["GET"])
def get_risks():
    risks = Risk.query.all()
    return jsonify([risk.to_dict() for risk in risks])

@app.route("/api/risks/<int:risk_id>", methods=["GET"])
def get_risk(risk_id):
    risk = Risk.query.get_or_404(risk_id)
    return jsonify(risk.to_dict())

STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/<path:filename>", methods=["GET"])
def static_files(filename):
    if filename.startswith("calculate-risk") or filename.startswith("api/"):
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

