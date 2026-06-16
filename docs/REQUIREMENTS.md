# REQUIREMENTS.md  

**Project:** privacy-heatmap  
**Owner:** Axentx – Product & Engineering  
**Target Users:** WordPress site owners who require on‑premises, privacy‑preserving analytics (heatmaps, funnels, session replay).  
**Goal:** Deliver a self‑hosted analytics platform that runs entirely on the customer’s infrastructure, never transmits raw visitor data to external services, and complies with GDPR/CCPA‑style privacy mandates.  

---  

## 1. Functional Requirements  

| ID | Description | Acceptance Criteria |
|----|-------------|----------------------|
| **FR‑1** | **Self‑Hosted Deployment** – The platform must be installable on a typical WordPress hosting environment (Linux, PHP 8.2+, MySQL/MariaDB, optional Docker). | • One‑click installer script (`install.sh`) or Docker Compose file.<br>• Post‑install health check endpoint (`/healthz`) returns 200 OK.<br>• No external network calls required during normal operation. |
| **FR‑2** | **WordPress Plugin Integration** – Provide a WP plugin that injects the required front‑end tracking script into pages. | • Plugin appears in WP admin → “Privacy Heatmap”.<br>• Activation automatically creates required DB tables and config files.<br>• Deactivation removes only plugin‑specific tables (core WP tables untouched). |
| **FR‑3** | **Heatmap Generation** – Capture mouse movement, clicks, scroll depth, and viewport size per visitor session and render aggregated heatmaps per page. | • Heatmaps update in near‑real‑time (≤ 5 min latency).<br>• Admin UI shows selectable date range, device type, and traffic segment filters.<br>• Exportable as PNG/SVG. |
| **FR‑4** | **Funnel Analytics** – Define ordered steps (e.g., “Landing → Add to Cart → Checkout”) and compute conversion rates. | • UI for creating/editing funnels (drag‑and‑drop).<br>• Funnel report shows drop‑off percentages, average time per step, and trend over selectable periods. |
| **FR‑5** | **Session Replay** – Record anonymized session events (clicks, scrolls, keypresses masked) and allow playback in admin UI. | • Replay UI supports play, pause, speed control, and event highlighting.<br>• Sessions older than configurable retention period are automatically purged. |
| **FR‑6** | **Privacy Controls** – No personally identifiable information (PII) is stored; IP addresses are hashed, and optional consent banner integration is provided. | • IP stored as salted SHA‑256 hash.<br>• No raw URLs, form inputs, or keystrokes are persisted.<br>• Consent banner can be toggled; analytics only start after consent. |
| **FR‑7** | **Data Export / Import** – Allow owners to export raw aggregated data (CSV/JSON) and import into external BI tools. | • Export endpoint respects same‑origin policy and requires admin auth.<br>• Import utility validates schema before ingestion. |
| **FR‑8** | **User Management & RBAC** – Admins can create sub‑users with role‑based permissions (view‑only, analyst, super‑admin). | • Permissions matrix documented in UI.<br>• Audit log records all privileged actions. |
| **FR‑9** | **API** – Provide a RESTful API for programmatic access to reports (heatmaps, funnels, sessions). | • API follows OpenAPI 3.0 spec.<br>• Rate‑limited to 100 req/min per API key. |
| **FR‑10** | **Upgrade Path** – Seamless in‑place upgrades without data loss. | • `upgrade.sh` script migrates DB schema and assets.<br>• Rollback command restores previous version if migration fails. |

---  

## 2. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | • Heatmap aggregation must process ≤ 10 k events/sec on a single‑core VM (2 GB RAM).<br>• API response time ≤ 200 ms for report queries under typical load (100 concurrent admins). |
| **NFR‑2** | **Scalability** | • Architecture must support horizontal scaling of the event collector via a message queue (e.g., RabbitMQ or Redis Streams). |
| **NFR‑3** | **Security** | • All internal traffic encrypted with TLS 1.3.<br>• Admin UI protected by WordPress authentication + optional 2FA.<br>• OWASP Top 10 mitigations applied (CSRF tokens, input sanitization, CSP). |
| **NFR‑4** | **Privacy Compliance** | • No raw IPs, cookies, or fingerprint data stored.<br>• Data retention configurable (default 30 days) and automatically enforced.<br>• Provide Data‑Subject Access Request (DSAR) export endpoint. |
| **NFR‑5** | **Reliability** | • System uptime ≥ 99.5 % (excluding scheduled maintenance).<br>• Event collector must guarantee at‑least‑once delivery; duplicates are de‑duplicated during aggregation. |
| **NFR‑6** | **Observability** | • Expose Prometheus metrics (`event_ingest_rate`, `heatmap_build_time`, `db_query_latency`).<br>• Centralized logs in JSON format with correlation IDs. |
| **NFR‑7** | **Maintainability** | • Codebase follows PSR‑12 (PHP) and PEP‑8 (Python) where applicable.<br>• Unit test coverage ≥ 80 % for core modules; integration tests for end‑to‑end flows. |
| **NFR‑8** | **Portability** | • Must run on any Linux distribution with Docker 20+ or on bare‑metal PHP environment.<br>• No reliance on proprietary cloud services (e.g., AWS S3, GCP Pub/Sub). |
| **NFR‑9** | **Documentation** | • Developer docs (setup, API spec) hosted in `docs/` and versioned with the repo.<br>• End‑user guide (plugin installation, consent banner) included in `README.md`. |
| **NFR‑10** | **Legal** | • All third‑party libraries must be compatible with GPL‑3.0 or MIT licenses (no GPL‑2 only). |

---  

## 3. Constraints  

1. **Technology Stack** – Must use the existing Axentx tech stack where possible:  
   - Backend: PHP 8.2 (WordPress integration) + optional Python micro‑service for heavy aggregation (leveraging `vLLM` if needed for future ML‑based heatmap smoothing).  
   - Data store: MySQL 8 (or MariaDB 10.6) for relational data; Redis 7 for queueing and caching.  
2. **Resource Limits** – Target deployment on a typical shared‑hosting plan (2 CPU, 2 GB RAM). All components must stay within these limits.  
3. **No External SaaS** – No reliance on third‑party analytics APIs, CDNs for data processing, or cloud‑only databases.  
4. **Compliance Scope** – Only GDPR/CCPA‑style anonymization is required; HIPAA or other sector‑specific regulations are out of scope.  
5. **Release Cadence** – Must align with Axentx quarterly release schedule; first MVP due in 12 weeks.  

---  

## 4. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | WordPress sites will have at least PHP 8.2 and MySQL 8 available. |
| **A‑2** | Site owners are responsible for TLS termination at the web server level (e.g., Apache/Nginx). |
| **A‑3** | Users will allocate a dedicated sub‑directory or Docker network for the analytics service; no port conflicts. |
| **A‑4** | The volume of events per site will not exceed 10 k events/minute for the MVP; scaling beyond this will be addressed in later phases. |
| **A‑5** | Site owners will handle GDPR consent UI integration; the plugin provides a hook (`privacy_heatmap_consent_granted`) for developers. |
| **A‑6** | All third‑party libraries used are vetted and stored in the internal artifact registry; no on‑the‑fly downloads at runtime. |

---  

**Document History**  

| Date | Author | Change |
|------|--------|--------|
| 2026‑06‑16 | Senior Product/Eng Lead | Initial draft of REQUIREMENTS.md |
| 2026‑06‑20 | QA Lead | Added performance & reliability metrics |
| 2026‑06‑22 | Legal Counsel | Confirmed privacy compliance statements |
