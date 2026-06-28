# breakeven.md  

## 1. Unit Economics (per **active WordPress site**)  

| Cost Component | Assumptions (per site / month) | Unit Cost | Monthly Cost per Site (USD) |
|----------------|--------------------------------|-----------|-----------------------------|
| **Compute** | • 1 vCPU & 2 GB RAM can serve ~200 sites (Docker container)  <br>• 1 vCPU ≈ $30 /mo (AWS t3.medium) | $30 / 200 sites = **$0.15** | **$0.15** |
| **Storage** | • Avg. 15 MB of raw event + heat‑map data per site <br>• 1 GB = $0.023 (S3‑Standard) | $0.023 / GB × 0.015 GB = **$0.00035** | **$0.0004** |
| **Bandwidth (egress)** | • 15 MB of data transferred out per site <br>• $0.09 / GB | $0.09 / GB × 0.015 GB = **$0.00135** | **$0.0014** |
| **Ops & Support Overhead** | 30 % of variable costs to cover monitoring, CI/CD, ticket triage | 0.30 × ($0.15+$0.0004+$0.0014) = **$0.045** | **$0.045** |
| **Total Variable Cost** |  |  | **$0.196 ≈ $0.20** |

> **Take‑away:** The marginal cost of adding a new paying site is **≈ $0.20 /mo**.  

---

## 2. Pricing Tiers  

| Tier | Monthly Price (USD) | Core Features | Monthly Revenue per Site |
|------|--------------------|----------------|--------------------------|
| **Starter** | **$9** | • Heatmap (up to 5 k page‑views) <br>• Funnel builder (up to 2 funnels) <br>• Session replay (up to 500 sessions) <br>• Email support (48 h) | $9 |
| **Growth** | **$29** | • Unlimited heatmaps (≤ 50 k page‑views) <br>• Unlimited funnels & sessions <br>• Advanced segmentation & filters <br>• Custom branding <br>• Slack/Chat support (24 h) | $29 |
| **Enterprise** | **$79** | • Unlimited usage (no caps) <br>• Multi‑site dashboard <br>• Dedicated account manager <br>• SLA 99.9 % uptime <br>• On‑premise install assistance & priority security patches | $79 |

*All tiers are **self‑hosted** – the platform runs on the customer’s own server; we only charge for the SaaS‑style licence, updates, and optional cloud‑backed analytics (if they opt‑in).*

---

## 3. Customer Acquisition Cost (CAC)  

| Channel | Typical Spend per Lead | Conversion Rate | CAC Estimate |
|---------|------------------------|-----------------|--------------|
| WordPress Plugin Marketplace (paid placement) | $0.30 per impression | 2 % → 1/50 leads become paying | **$15** |
| Content/SEO (blog, webinars) | $0.10 per click | 1 % → 1/100 leads become paying | **$10** |
| Paid Social (LinkedIn, Twitter) | $1.00 per click | 3 % → 1/33 leads become paying | **$33** |
| **Overall CAC range** | — | — | **$10 – $35** (average ≈ $22)** |

---

## 4. Lifetime Value (LTV)  

*Assumptions*  

- **Monthly churn**: 5 % (average SaaS churn for niche B2B tools) → **20 months** average lifetime.  
- **Revenue mix**: 60 % Starter, 30 % Growth, 10 % Enterprise → **Weighted ARPU** = (0.6×9)+(0.3×29)+(0.1×79) = **$22.2** per month.  

**LTV** = ARPU × Lifetime = $22.2 × 20 ≈ **$444**  

Subtract average CAC ($22) → **Net LTV ≈ $422** per customer.

---

## 5. Break‑Even Users Count  

| Item | Monthly Amount (USD) |
|------|----------------------|
| Fixed Costs* (dev salaries, core infra, marketing, legal) | **$5,000** |
| Variable Cost per User | **$0.20** |
| Revenue per User (average ARPU) | **$22.2** |
| **Contribution Margin per User** | $22.2 – $0.20 = **$22.0** |

**Break‑Even Users** = Fixed Costs ÷ Contribution per User  

\[
\frac{5{,}000}{22.0}\;\approx\;227\;\text{paying sites}
\]

Rounded up → **≈ 230 active paying sites** needed to cover all monthly outlays.

---

## 6. Path to $10 K MRR  

| Target MRR | Required Revenue Mix (example) | # of Sites per Tier |
|------------|--------------------------------|----------------------|
| **$10,000** | 40 % Starter, 45 % Growth, 15 % Enterprise | 44 × $9 = $396  <br>124 × $29 = $3,596  <br>13 × $79 = $1,027  <br>**Total Sites = 181** |
| **$10,000** (alternative) | 30 % Starter, 60 % Growth, 10 % Enterprise | 33 × $9 = $297  <br>207 × $29 = $6,003  <br>13 × $79 = $1,027  <br>**Total Sites = 253** |
| **$10,000** (all‑Growth) | 100 % Growth | 345 × $29 = $10,005  <br>**Total Sites = 345** |

*Key Insight*: Even a modest **Starter‑heavy** mix reaches $10 K MRR with **≈ 180–200** paying sites, well below the 230‑site break‑even point when we factor in the $5 K fixed cost baseline. Once the 230‑site threshold is crossed, each additional site contributes ~**$22** to profit, accelerating the climb to $10 K MRR.

---

### Quick Summary  

| Metric | Value |
|--------|-------|
| Variable cost per active site | **$0.20 /mo** |
| Average ARPU (blended) | **$22.2 /mo** |
| CAC (average) | **$22** |
| LTV (net of CAC) | **≈ $422** |
| Fixed monthly overhead | **$5,000** |
| Break‑even paying sites | **≈ 230** |
| Sites needed for $10 K MRR | **180 – 345** (depending on tier mix) |

These numbers give a concrete financial runway for **privacy‑heatmap** and a clear target for sales/marketing: acquire ~250 paying WordPress sites (mix of tiers) to become cash‑positive and hit the $10 K MRR milestone within the first 12 months.