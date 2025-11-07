import json
from pathlib import Path
from flask import Blueprint, render_template, abort
from .scoring import compute_score

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    # For now, just show the sample report
    return render_template("index.html")

@bp.route("/scan/sample")
def scan_sample():
    sample_path = Path(__file__).parent / "sample_results" / "scan_sample.json"
    if not sample_path.exists():
        abort(404, "sample_results/scan_sample.json not found")

    data = json.loads(sample_path.read_text(encoding="utf-8"))

    # Recompute score from checks (source of truth = scoring.py)
    data["score"] = compute_score(data.get("checks", {}))
    return render_template("report.html", result=data)
