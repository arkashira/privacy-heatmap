# Privacy‑Heatmap — Product Requirements Document (PRD)

**Document version**: 1.0  
**Last updated**: 2026‑06‑16  
**Owner**: Senior Product/Engineering Lead (Axentx)  
**Repo**: `privacy-heatmap`  

---  

## 1. Problem Statement  

WordPress site owners increasingly need actionable user‑behavior insights (heatmaps, funnels, session replay) to improve conversion rates. Existing analytics solutions (e.g., Google Analytics, Hotjar, Crazy Egg) either:

1. **Leak visitor data to third‑party cloud services**, violating GDPR, CCPA, and other privacy regulations.  
2. **Require a SaaS subscription**, adding recurring cost and vendor lock‑in.  
3. **Offer limited self‑hosted options** that lack a complete feature set or are difficult to install/maintain.

**Result**: Site owners either forgo deep analytics (missing optimization opportunities) or expose user data to external processors, risking compliance penalties and loss of user trust.

## 2. Target Users  

| Segment | Primary Persona | Pain Points | Desired Outcome |
|---------|----------------|-------------|-----------------|
| **WordPress SMBs** | *Emma, 32, Owner of a boutique e‑commerce store* | Limited budget, must stay GDPR‑compliant, no dev resources | Free/low‑cost, plug‑and‑play analytics that never leaves the server |
| **Agency‑managed sites** | *Liam, 28, Digital agency lead* | Needs to deploy analytics across dozens of client sites, maintain data isolation | Centralized self‑hosted solution, easy multi‑site provisioning |
| **Privacy‑first publishers** | *Dr. Chen, 45, Academic journal publisher* | Must guarantee no third‑party data transfer, audit‑ready logs | Fully self‑contained, exportable logs, transparent data handling |

## 3. Product Vision & Goals  

| Goal | Success Metric (KPIs) | Target |
|------|----------------------|--------|
| **Privacy‑first analytics** | % of data stored only on‑premises (no outbound requests) | 100 % |
| **Zero‑code deployment** | Avg. installation time for a fresh WP site | ≤ 15 min |
| **Actionable insights** | % of users who create at least one heatmap/funnel within 7 days | ≥ 70 % |
| **Revenue‑validated** | Paying conversions (annual) from free → paid tier | 150 + by month 12 |
| **Performance** | Avg. page‑load impact per tracked page | ≤ 150 ms (5 % of total load) |

## 4. Scope  

### 4.1 In‑Scope (Must‑Have)  

1. **Self‑hosted WordPress plugin**  
   - One‑click installer via WP admin.  
   - No external API keys or cloud services required.  

2. **Heatmap module**  
   - Click, scroll, mouse‑move heatmaps.  
   - Real‑time rendering in admin UI.  

3. **Funnel builder**  
   - Drag‑and‑drop step definition (URL patterns, events).  
   - Conversion rate reporting per funnel.  

4. **Session replay**  
   - Record anonymized DOM snapshots + mouse events.  
   - Playback UI with scrubber, speed control, and element masking.  

5. **Data storage & retention**  
   - SQLite (default) + optional MySQL/PostgreSQL.  
   - Configurable retention (e.g., 30 days, 90 days).  

6. **Privacy controls**  
   - Automatic IP anonymization.  
   - Opt‑out banner integration (GDPR/CCPA).  
   - Export‑to‑CSV/JSON for audit.  

7. **Admin dashboard**  
   - Overview cards (visits, heatmap count, funnel conversion).  
   - Role‑based access (admin vs. analyst).  

8. **Documentation & CI**  
   - Full README, installation guide, API reference.  
   - GitHub Actions CI (PHPUnit, PHPCS, static analysis).  

### 4.2 Out‑of‑Scope (Nice‑to‑Have)  

| Feature | Reason for deferment |
|---------|----------------------|
| **AI‑driven insight suggestions** | Requires model training pipeline; not needed for MVP validation. |
| **Cross‑domain tracking** | Complex setup; focus first on single‑site use‑cases. |
| **Real‑time streaming to external BI tools** | Contradicts privacy‑first premise; could be added as an opt‑in extension later. |
| **Mobile‑app SDK** | Current market focus is WordPress web sites; mobile SDK to be evaluated after product‑market fit. |
| **White‑label branding** | Will be offered in paid tier after core product stabilizes. |

## 5. Key Features & Prioritization  

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **One‑click WP installer** | Deploys plugin, creates DB tables, sets default config. | Installation completes without errors; plugin appears in WP admin > Plugins list. |
| **P1** | **Heatmap capture & rendering** | Records click/scroll/mouse‑move data; renders overlay on selected page. | Heatmap view matches recorded interactions; data stored locally; no external requests. |
| **P1** | **Funnel builder UI** | Allows defining steps via URL regex or custom JS event. | Funnel conversion % displayed; steps can be added/removed; data persists. |
| **P1** | **Session replay (anonymized)** | Stores DOM snapshots + mouse events; playback UI masks PII. | Replay runs smoothly for recordings ≤ 5 min; no raw IP or form data stored. |
| **P2** | **Retention policy UI** | Admin can set days to keep data; automatic purge job runs nightly. | Data older than configured days is deleted; job logs success/failure. |
| **P2** | **Export / audit logs** | CSV/JSON export of raw events; includes GDPR‑compliant metadata. | Export file matches selected date range; includes anonymized IP hash. |
| **P3** | **Role‑based access control** | Separate permissions for “Analyst” vs. “Admin”. | Analyst cannot change plugin settings; can view dashboards only. |
| **P3** | **Performance optimizer** | Lazy‑load script, debounce event capture, optional sampling. | Measured page‑load impact ≤ 150 ms on Lighthouse audit. |
| **P4** | **Paid tier – advanced storage** | Off‑site encrypted backup (self‑hosted S3 compatible). | Backup can be scheduled; data restored on demand. |
| **P4** | **White‑label branding** | Custom logo & color scheme for paid customers. | Admin can upload logo; UI reflects branding instantly. |

## 6. Success Metrics & Validation  

| Metric | Measurement Method | Target (Month 12) |
|--------|--------------------|-------------------|
| **Adoption** | # of active installations (unique WP sites) | 2,500 |
| **Engagement** | Avg. heatmaps created per site per month | 3 |
| **Conversion** | Free → Paid upgrade rate | 6 % |
| **Compliance** | % of sites passing automated GDPR audit (no outbound calls) | 100 % |
| **Performance** | Avg. additional page load time (Lighthouse) | ≤ 150 ms |
| **Support** | Avg. time to first response (GitHub Issues) | < 4 h |

**Validation plan**:  
1. Release **Beta** to 100 curated WordPress sites (via Axentx BD network).  
2. Collect usage telemetry (self‑hosted, opt‑in) for the above metrics.  
3. Iterate on P1 features until all acceptance criteria met.  
4. Open **General Availability (GA)** with free tier + paid “Pro” tier (monthly $9/site).  

## 7. Milestones & Timeline  

| Milestone | Deliverable | Owner | Due |
|-----------|-------------|-------|-----|
| **M1 – Foundations** | Repo scaffold, CI pipeline, basic plugin skeleton | Engineering Lead | 2026‑06‑30 |
| **M2 – Core Capture** | Heatmap + session capture library, local storage | Backend Engineer | 2026‑07‑21 |
| **M3 – UI MVP** | Admin dashboard, heatmap viewer, funnel builder UI | Frontend Engineer | 2026‑08‑15 |
| **M4 – Privacy Harden** | IP anonymization, opt‑out banner, data export | Security Engineer | 2026‑08‑31 |
| **M5 – Beta Launch** | Beta package, documentation, support channel | PM / Docs Lead | 2026‑09‑15 |
| **M6 – GA Release** | Full feature set, paid tier toggle, licensing | PM / Sales Lead | 2026‑10‑31 |
| **M7 – Post‑Launch** | Performance tuning, retention job, analytics dashboard | Ops / Engineering | Ongoing |

## 8. Risks & Mitigations  

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Data leakage via mis‑configured server** | Compliance breach | Medium | Include automated pre‑flight check that blocks outbound requests; ship with firewall rules example. |
| **Performance overhead on high‑traffic sites** | User churn | Medium | Implement sampling mode; provide clear docs on tuning. |
| **WordPress version compatibility** | Installation failures | Low | CI matrix testing across WP 6.2‑6.5; deprecate older versions in docs. |
| **Insufficient paid conversions** | Revenue shortfall | Medium | Early pricing experiments; bundle with premium support. |
| **Open‑source forking** | Competitive copycat | Low | License under GPL‑v3 with clear contribution guidelines; focus on premium services for revenue. |

## 9. Dependencies  

| Dependency | Reason | Status |
|------------|--------|--------|
| **WordPress ≥ 6.2** | Core platform | Confirmed |
| **PHP ≥ 8.1** | Language features, performance | Confirmed |
| **vLLM / SGLang** (optional for future AI insights) | Potential future AI module | Out‑of‑scope for MVP |
| **Axentx BRAIN vector store** | For future similarity search across heatmaps | Planned for Phase 2 |

---  

*Prepared for internal review. All sections are aligned with Axentx’s privacy‑first, revenue‑validated product development framework.*
