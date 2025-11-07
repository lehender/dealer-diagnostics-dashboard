# Dealer Diagnostics Dashboard

A lightweight Flask web app that runs automated health checks on dealership websites. It simulates a simple diagnostic workflow a Customer Specialist might use: fetch a URL, run checks (links, performance, analytics tags, SEO basics), compute a score, and render a clean HTML report.

## What it does
- Checks for **broken links** on the same page
- Measures basic **performance** (request time and response size)
- Detects **Google Analytics GA4** and **Google Tag Manager (GTM)** tags
- Flags **SEO basics**: title length, meta description, H1 count
- Computes a **0–100 score** with simple, tunable penalties
- Renders a **Bootstrap** report page (printable)

## Tech stack
- Python (Flask, httpx, BeautifulSoup4, lxml)
- HTML/CSS with Bootstrap 5
- Simple in-memory store for scan results (DB can be added later)

## Quick start
```bash
git clone https://github.com/<your-username>/dealer-diagnostics-dashboard.git
cd dealer-diagnostics-dashboard

# Optional but recommended: virtual environment
python -m venv .venv
# Windows (Git Bash)
source .venv/Scripts/activate

pip install -r requirements.txt  # or: pip install flask httpx beautifulsoup4 lxml

# Run
python -m flask --app run run --debug
# Open http://127.0.0.1:5000
```

## How to use
1. Open the app and try **View Sample Report** to see the layout.
2. Enter a real website (e.g., `example.com`) and click **Run Scan**.
3. The app fetches the page, runs checks, and shows a **Links / Performance / Analytics / SEO** breakdown with a score.

## Scoring (v0 defaults)
Start at **100**, subtract:
- Links: 10 points per 404 (cap 30)
- Performance: 10 points if elapsed time > 2500 ms
- Analytics: 20 points if neither GA4 nor GTM found
- SEO: 10 if no meta description, 5 if no H1, 5 if title missing or out of 10–65 chars

All penalties are defined in `app/scoring.py` and easy to tweak.

## Checks overview
- **Links** (`app/checks/links.py`): parses anchors, normalizes to same-origin URLs, HEAD then GET on failure, collects 4xx/5xx.
- **Performance** (`app/checks/perf.py`): uses the main fetch’s elapsed time and byte size.
- **Analytics** (`app/checks/analytics.py`): scans HTML and script tags for GA4 hints (`gtag(` or `G-…`) and GTM loader (`googletagmanager.com/gtm.js`).
- **SEO** (`app/checks/seo.py`): validates title length, presence of meta description, and H1 count.

## Project layout
```
run.py
app/
  __init__.py
  routes.py
  scoring.py
  checks/
    links.py
    perf.py
    analytics.py
    seo.py
  templates/
    base.html
    index.html
    report.html
  static/
    css/bootstrap.min.css
  sample_results/
    scan_sample.json
docs/
  contracts.md
```

## Limitations and next steps
- Single-page scan by default (no crawler yet)
- Basic timing (request elapsed) without headless browser metrics
- Tag detection is heuristic; SPA-injected tags may require a headless run

**Planned enhancements**
- Optional headless timing (Playwright) for DOMContentLoaded / Load
- Same-origin mini-crawl (N pages) with politeness delays
- PostgreSQL storage for history and charts
- Insights tab (simple charts of recent scores/failures)
- Export report to PDF with a print stylesheet

## Why this is relevant
- Mirrors real website health checks: links, analytics tagging, and SEO basics
- Demonstrates practical troubleshooting, not just UI
- Clean, readable code with small, testable modules
