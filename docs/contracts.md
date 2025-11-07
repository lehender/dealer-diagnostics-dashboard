# JSON Contracts

## 1) Check Result (per category)
- `category`: "links" | "perf" | "analytics" | "seo"
- `severity`: "pass" | "warn" | "fail"
- `metrics`: object with numeric/boolean fields relevant to the category
- `items`: array of detail objects or strings (URLs, messages, etc.)
- `suggestions`: array of short action texts (1–2 sentences max)

### Field constraints
- `severity` must be one of: pass, warn, fail.
- Strings are UTF-8; timestamps are ISO 8601.
- Each category must be present in `checks` even if it’s a pass with empty items.

### Category field guide
**links.metrics**
- `total_links` (int), `broken_links` (int)
- `items` (on warn/fail): `[ { "url": "...", "status": 404, "referrer": "..." } ]`

**perf.metrics**
- `elapsed_ms` (int), `bytes` (int)

**analytics.metrics**
- `ga4_found` (bool), `gtm_found` (bool)

**seo.metrics**
- `title_len` (int), `meta_description_len` (int), `h1_count` (int)

---

## 2) Scan Result (overall)
- `scan_id`: string
- `url`: normalized input string
- `started_at`: ISO 8601
- `finished_at`: ISO 8601
- `status`: "running" | "done" | "error"
- `score`: integer 0–100
- `checks`: object with keys: links, perf, analytics, seo → each is a Check Result
- `errors`: array of strings (network/TLS/timeout notes)