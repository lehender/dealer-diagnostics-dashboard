# app/scoring.py

from __future__ import annotations
from typing import Dict, Any

# ---- Tunable weights (v0) ----
LINKS_PENALTY_PER_404 = 10     # cap 30
LINKS_PENALTY_CAP = 30

PERF_TIME_THRESHOLD_MS = 2500
PERF_PENALTY_OVER_THRESHOLD = 10

ANALYTICS_PENALTY_MISSING = 20
# (reserved) ANALYTICS_PENALTY_BAD_PLACEMENT = 10

SEO_PENALTY_NO_META_DESC = 10
SEO_PENALTY_NO_H1 = 5
SEO_PENALTY_TITLE_ISSUE = 5  # missing/too short/too long

def clamp(value: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, value))

def _int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default

def _bool(v: Any, default: bool = False) -> bool:
    return bool(v) if v is not None else default

def compute_score(checks: Dict[str, Dict[str, Any]]) -> int:
    """
    Input: checks dict keyed by category ("links", "perf", "analytics", "seo"),
           each value is a Check Result per docs/contracts.md
    Output: integer score 0..100
    """
    score = 100

    # LINKS
    links = checks.get("links") or {}
    lm = (links.get("metrics") or {})
    broken = _int(lm.get("broken_links"), 0)
    if broken > 0:
        score -= min(LINKS_PENALTY_PER_404 * broken, LINKS_PENALTY_CAP)

    # PERF
    perf = checks.get("perf") or {}
    pm = (perf.get("metrics") or {})
    elapsed_ms = _int(pm.get("elapsed_ms"), 0)
    if elapsed_ms > PERF_TIME_THRESHOLD_MS:
        score -= PERF_PENALTY_OVER_THRESHOLD

    # ANALYTICS
    analytics = checks.get("analytics") or {}
    am = (analytics.get("metrics") or {})
    ga4_found = _bool(am.get("ga4_found"), False)
    gtm_found = _bool(am.get("gtm_found"), False)
    if not (ga4_found or gtm_found):
        score -= ANALYTICS_PENALTY_MISSING
    # (Placement penalties can be added later)

    # SEO
    seo = checks.get("seo") or {}
    sm = (seo.get("metrics") or {})
    title_len = sm.get("title_len")
    meta_desc_len = sm.get("meta_description_len")
    h1_count = sm.get("h1_count")

    # meta description
    if meta_desc_len is None or _int(meta_desc_len, 0) == 0:
        score -= SEO_PENALTY_NO_META_DESC

    # h1 present
    if h1_count is None or _int(h1_count, 0) < 1:
        score -= SEO_PENALTY_NO_H1

    # title length checks
    title_issue = False
    if title_len is None or _int(title_len, 0) == 0:
        title_issue = True
    else:
        tlen = _int(title_len, 0)
        if tlen < 10 or tlen > 65:
            title_issue = True
    if title_issue:
        score -= SEO_PENALTY_TITLE_ISSUE

    return clamp(int(score))
