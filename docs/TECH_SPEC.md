# TECH_SPEC.md  

**Project:** privacy-heatmap  
**Owner:** Axentx – Product Engineering  
**Status:** MVP → Production (self‑hosted)  
**Target Audience:** WordPress site owners who need on‑premise, privacy‑first analytics (heatmaps, funnels, session replay).  

---  

## 1. Overview  

privacy‑heatmap is a self‑hosted analytics platform that runs entirely on the customer’s infrastructure. It captures user interaction events from a WordPress front‑end plugin, stores them in an encrypted PostgreSQL database, processes them into aggregate heatmaps, conversion funnels and session replay data, and serves visualisations via a secure React SPA. No data leaves the host environment, satisfying GDPR, CCPA, and other privacy regulations.

---  

## 2. Architecture Diagram  

```
+-------------------+        +-------------------+        +-------------------+
| WordPress Plugin  |  HTTPS|  Nginx Reverse    |  HTTP  |  API Service      |
| (JS + PHP)        |<------>|  Proxy (TLS off‑  |<------>|  (FastAPI /       |
|  - Event collector|        |  loading)         |        |  uvicorn)         |
+-------------------+        +-------------------+        +-------------------+
                                                               |
                                                               |  SQL (encrypted)
                                                               v
                                                      +-------------------+
                                                      | PostgreSQL (PGCrypto) |
                                                      +-------------------+
                                                               |
                                                               |  REST/WS
                                                               v
                                                      +-------------------+
                                                      | Worker Queue      |
                                                      | (Redis + RQ)       |
                                                      +-------------------+
                                                               |
                                                               v
                                                      +-------------------+
                                                      | Processing Workers|
                                                      | (Python)          |
                                                      +-------------------+
                                                               |
                                                               v
                                                      +-------------------+
                                                      | Heatmap / Funnel  |
                                                      | Generator (NumPy,|
                                                      | Pandas, OpenCV)   |
                                                      +-------------------+
                                                               |
                                                               v
                                                      +-------------------+
                                                      | Static Assets     |
                                                      | (React SPA)       |
                                                      +-------------------+
```

---  

## 3. Core Components  

| Component | Language / Framework | Responsibility |
|-----------|----------------------|----------------|
| **WordPress Plugin** | PHP 8.2 + vanilla JS | Injects tracking script, captures DOM events (click, scroll, mousemove), batches & sends to API over HTTPS. |
| **API Service** | Python 3.11, FastAPI, uvicorn | Authenticated JSON endpoint (`/api/v1/events`), health checks, admin CRUD. |
| **Database** | PostgreSQL 15 with pgcrypto | Encrypted storage of raw events and derived aggregates. |
| **Queue** | Redis 7 + RQ (Redis Queue) | Guarantees at‑least‑once delivery of event batches to workers. |
| **Workers** | Python 3.11 | De‑batch events, compute per‑page heatmap matrices, funnel step counts, session replay data, store results back to DB. |
| **Heatmap Generator** | OpenCV, NumPy, Pandas | Rasterises click/scroll intensity onto page screenshots (captured via headless Chrome on demand). |
| **Frontend SPA** | React 18, TypeScript, Vite, TailwindCSS | Dashboard UI: heatmap overlay, funnel builder, session replay timeline. |
| **Reverse Proxy** | Nginx 1.24 | TLS termination, HTTP/2, rate‑limiting, static asset serving. |
| **Metrics & Logging** | Prometheus + Grafana, Loki | Export API latency, queue depth, worker health; centralised logs for audit. |

---  

## 4. Data Model  

### 4.1 Raw Event (`events` table)

| Column | Type | Description |
|--------|------|-------------|
| `id` | `BIGSERIAL PK` | Unique identifier |
| `site_id` | `UUID` | Foreign key to `sites` |
| `session_id` | `UUID` | Anonymous session identifier |
| `timestamp` | `TIMESTAMPTZ` | Event time (UTC) |
| `event_type` | `VARCHAR(32)` | `click` / `scroll` / `mousemove` / `pageview` |
| `payload` | `JSONB ENCRYPTED` | Event‑specific data (coordinates, element selector, scroll depth) |
| `user_agent` | `TEXT ENCRYPTED` | Browser UA string |
| `ip_hash` | `BYTEA` | SHA‑256 hash of IP (non‑reversible) |

*Encryption is performed at the application layer using `cryptography` library with a per‑site key stored in the server’s KMS (e.g., HashiCorp Vault).*

### 4.2 Derived Heatmap (`heatmaps` table)

| Column | Type | Description |
|--------|------|-------------|
| `id` | `BIGSERIAL PK` |
| `site_id` | `UUID` |
| `page_url` | `TEXT` |
| `generated_at` | `TIMESTAMPTZ` |
| `heatmap_png` | `BYTEA` | PNG image (compressed) |
| `resolution` | `VARCHAR(16)` | e.g., `1920x1080` |
| `click_density` | `JSONB` | Sparse matrix of click counts (optional for API) |

### 4.3 Funnel Definition (`funnels` table)

| Column | Type | Description |
|--------|------|-------------|
| `id` | `BIGSERIAL PK` |
| `site_id` | `UUID` |
| `name` | `TEXT` |
| `steps` | `JSONB` | Ordered list of CSS selectors / URLs |
| `created_at` | `TIMESTAMPTZ` |

### 4.4 Funnel Metrics (`funnel_stats` view)

Aggregated per‑step conversion rates, stored as a materialised view refreshed nightly.

### 4.5 Session Replay (`sessions` table)

| Column | Type | Description |
|--------|------|-------------|
| `session_id` | `UUID PK` |
| `site_id` | `UUID` |
| `events` | `JSONB ENCRYPTED` | Ordered list of events for replay |
| `duration_ms` | `INTEGER` |
| `created_at` | `TIMESTAMPTZ` |

---  

## 5. Key APIs / Interfaces  

All API endpoints are versioned under `/api/v1/` and require a **Bearer token** generated per site in the admin UI.

### 5.1 Event Ingestion  

```
POST /api/v1/events
Headers:
  Authorization: Bearer <site-token>
  Content-Type: application/json
Body:
{
  "session_id": "c1a2…",
  "events": [
    {"type":"click","ts":1697041200,"payload":{"x":342,"y":210,"selector":"#buy-now"}},
    {"type":"scroll","ts":1697041205,"payload":{"depth":0.73}}
  ]
}
```

*Response:* `202 Accepted` + `{ "batch_id": "<uuid>" }`  

The endpoint validates payload size (< 64 KB), queues the batch in Redis (`event_queue:<site_id>`), and returns immediately.

### 5.2 Dashboard Data  

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sites/{site_id}/heatmap?url=…&res=1920x1080` | GET | Returns PNG heatmap (binary) and JSON meta. |
| `/api/v1/sites/{site_id}/funnels/{funnel_id}` | GET | Funnel conversion stats (JSON). |
| `/api/v1/sites/{site_id}/sessions/{session_id}` | GET | Session replay payload (JSON). |
| `/api/v1/sites/{site_id}/config` | GET/PUT | Retrieve or update site‑level config (privacy flags, retention). |

All responses are cached via **FastAPI‑Cache** (Redis) for 5 min where appropriate.

### 5.3 Admin UI  

The React SPA consumes the above endpoints and also provides a **WebSocket** (`/ws/updates`) for real‑time queue depth and worker health notifications.

---  

## 6. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | React 18 + TypeScript + Vite + TailwindCSS | Modern, fast dev cycle, small bundle, easy theming. |
| **Backend API** | FastAPI (Python 3.11) + uvicorn (ASGI) | High performance, automatic OpenAPI docs, async I/O for HTTP. |
| **Task Queue** | Redis 7 + RQ (Redis Queue) | Simple, reliable, no external broker needed; fits self‑hosted model. |
| **Data Processing** | Python (NumPy, Pandas, OpenCV) | Vectorised heatmap calculations, image compositing. |
| **Database** | PostgreSQL 15 + pgcrypto | Strong ACID guarantees, built‑in column‑level encryption. |
| **Containerisation** | Docker Compose (dev) / Helm chart (k8s prod) | Consistent environments, easy scaling. |
| **Observability** | Prometheus + Grafana (metrics), Loki (logs) | Industry‑standard monitoring, low overhead. |
| **TLS / Secrets** | Nginx (Let's Encrypt) + HashiCorp Vault (site keys) | End‑to‑end encryption, secret rotation. |
| **CI/CD** | GitHub Actions (lint, unit tests, integration tests, Docker build) | Automated quality gate before merge to `main`. |

---  

## 7. Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| fastapi | 0.110.0 | MIT |
| uvicorn | 0.27.0 | BSD-3 |
| redis | 5.0.3 | MIT |
| rq | 1.15.1 | BSD-3 |
| sqlalchemy | 2.0.23 | MIT |
| psycopg2-binary | 2.9.9 | LGPL-3.0 |
| numpy | 1.26.2 | BSD-3 |
| pandas | 2.2.0 | BSD-3 |
| opencv-python | 4.9.0.80 | MIT |
| react | 18.2.0 | MIT |
| typescript | 5.2.2 | Apache‑2.0 |
| tailwindcss | 3.3.3 | MIT |
| nginx | 1.24 | BSD-2 |
| prometheus-client | 0.20.0 | Apache‑2.0 |
| loki-client | 0.5.0 | Apache‑2.0 |
| cryptography | 42.0.2 | Apache‑2.0 |
| python‑dotenv | 1.0.0 | BSD-3 |

All dependencies are vetted for security (Snyk scan CI step) and are compatible with the company‑wide **C. Frameworks** policy (e.g., `vLLM` not required here).

---  

## 8. Deployment Architecture  

### 8.1 Docker Images  

| Service | Dockerfile Base | Image Tag |
|---------|----------------|-----------|
| api | `python:3.11-slim` | `axentx/privacy-heatmap-api:<git‑sha>` |
| worker | `python:3.11-slim` | `axentx/privacy-heatmap-worker:<git‑sha>` |
| frontend | `node:20-alpine` (build) → `nginx:1.24-alpine` (runtime) | `axentx/privacy-heatmap-ui:<git‑sha>` |
| redis | `redis:7-alpine` | `axentx/privacy-heatmap-redis:7-alpine` |
| postgres | `postgres:15-alpine` | `axentx/privacy-heatmap-db:15-alpine` |
| nginx‑proxy | `nginx:1.24-alpine` | `axentx/privacy-heatmap-proxy:1.24-alpine` |

Images are pushed to the internal **Axentx Container Registry** after successful CI.

### 8.2 Kubernetes Helm Chart (prod)

- **Namespace:** `privacy-heatmap`
- **StatefulSets:** `postgres`, `redis`
- **Deployments:** `api`, `worker`, `frontend`, `nginx-proxy`
- **Ingress:** TLS‑terminated, host `analytics.<customer‑domain>`
- **Resources:**  
  - API: `cpu 250m`, `mem 256Mi`  
  - Worker: `cpu 500m`, `mem 512Mi` (autoscale based on queue depth)  
  - DB: `cpu 500m`, `mem 1Gi` (PVC 20 Gi, encrypted at rest)  
- **PodDisruptionBudgets** to ensure high‑availability during upgrades.
- **ConfigMaps/Secrets:** site‑specific encryption keys, DB credentials, JWT secret.

### 8.3 Backup & Retention  

- **PostgreSQL**: Daily logical dump (`pg_dump`) stored on an off‑site NFS mount, retained 30 days.  
- **Redis**: RDB snapshot every 6 h, persisted to same NFS.  
- **Retention Policy**: Raw events older than 90 days are purged automatically via a nightly DB job; heatmaps/funnel stats are kept indefinitely (subject to storage quota).

---  

## 9. Security & Privacy  

| Concern | Mitigation |
|---------|------------|
| **Data exfiltration** | All inbound/outbound traffic forced through Nginx TLS (TLS 1.3). No external calls from workers. |
| **At‑rest encryption** | `pgcrypto` encrypts `payload`, `user_agent`, `events` JSON. Site‑level keys stored in Vault, rotated quarterly. |
| **IP privacy** | Store only SHA‑256 hash of IP (`ip_hash`). |
| **Access control** | Per‑site JWT bearer token with `site_id` claim; tokens signed with RSA‑4096 key stored in Vault. |
| **CSRF/XSS** | WordPress plugin injects a nonce; API validates `Origin` header. UI sanitises all user‑generated content. |
| **Audit logging** | Every admin action logged to Loki with request metadata (no payload). |
| **Compliance** | GDPR‑ready: data can be fully deleted via admin UI; retention settings configurable per site. |

---  

## 10. Testing Strategy  

| Layer | Tool | Scope |
|-------|------|-------|
| Unit | pytest + hypothesis | Core functions: event validation, encryption/decryption, heatmap rasterisation. |
| Integration | testcontainers (Postgres, Redis) + httpx | End‑to‑end API flow, queue processing, DB persistence. |
| UI | Cypress (headless) | Dashboard rendering, heatmap overlay accuracy, funnel builder. |
| Performance | locust | Simulate 10 k events/sec burst, verify <200 ms API latency, queue lag <5 s. |
| Security | bandit, OWASP ZAP | Static analysis, runtime scanning for XSS/SQLi. |
| CI | GitHub Actions | Lint (ruff, eslint), test matrix (py3.11, node 20), Docker build, Snyk scan, push artifacts. |

Coverage target: **≥85 %** for backend, **≥80 %** for frontend.

---  

## 11. Release & Versioning  

- **Semantic Versioning** (`MAJOR.MINOR.PATCH`).  
- **Release Cadence:** Bi‑weekly feature releases; monthly security patches.  
- **Changelog** generated automatically via `git-cliff`.  
- **Migration Scripts:** Alembic for DB schema changes; forward‑only migrations only (no destructive ops without explicit admin approval).  

---  

## 12. Open Issues & Future Work  

| Issue | Description | Priority |
|-------|-------------|----------|
| **Real‑time heatmap** | Stream live click density via WebSocket for premium tier. | Low |
| **Headless screenshot service** | Offload page screenshot generation to a separate microservice (Chromium). | Medium |
| **Multi‑site dashboard** | Aggregate analytics across multiple WordPress sites under one admin account. | High |
| **Plugin auto‑update** | Implement WP‑CLI based auto‑update mechanism for the tracking plugin. | Medium |
| **Compliance reports** | Export GDPR data‑subject request (DSR) bundles in JSON‑LD. | High |

---  

## 13. Glossary  

- **Site ID** – UUID that uniquely identifies a WordPress installation within privacy‑heatmap.  
- **Session ID** – Random UUID generated client‑side, stored in a first‑party cookie (`phm_sid`).  
- **Heatmap PNG** – Raster image where pixel intensity corresponds to aggregated click/scroll density.  
- **Funnel** – Ordered list of page elements or URLs representing a conversion path.  

---  

*Prepared by:* Senior Product/Engineering Lead – Axentx  
*Date:* 2026‑06‑16  

---
