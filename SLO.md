# Service Level Objectives (SLOs)

This document defines the reliability targets for the sample service. It's the
heart of the SRE approach: instead of chasing "100% uptime" (impossible and
pointless), you pick explicit targets, measure them, and spend the allowed
unreliability — the **error budget** — deliberately.

## The vocabulary (plain English)

| Term | Meaning |
|------|---------|
| **SLI** (Indicator) | A *measurement* of how well the service is doing, as a ratio of good events to total events. E.g. "fraction of requests that didn't fail." |
| **SLO** (Objective) | The *target* for an SLI over a time window. E.g. "99.9% of requests succeed over 30 days." |
| **Error budget** | The amount of failure the SLO *allows*. If the SLO is 99.9%, the budget is the remaining **0.1%**. |
| **Burn rate** | How fast you're spending the error budget. A burn rate of **1** means you'll use exactly the whole budget by the end of the window; **10** means you'll burn it 10× too fast. |

## Our SLOs

### 1. Availability

- **SLI:** proportion of HTTP requests that do **not** return a `5xx` error.
  ```
  good  = requests with status < 500
  total = all requests
  SLI   = good / total
  ```
- **SLO:** **99.9%** of requests succeed, measured over a rolling **30 days**.
- **Error budget:** `100% − 99.9% = 0.1%` of requests may fail.
  - Over 30 days that is roughly **43 minutes** of full downtime, or 0.1% of
    all requests failing — whichever way the failures arrive.

### 2. Latency

- **SLI:** proportion of requests served in **under 500 ms**.
  ```
  good  = requests faster than 500ms
  total = all requests
  SLI   = good / total
  ```
- **SLO:** **99%** of requests under 500 ms, over a rolling **30 days**.
- **Error budget:** 1% of requests may be slower than 500 ms.

## A note on windows (lab vs. production)

Real SLOs are measured over long windows (28–30 days). In this lab there's no
month of history and you want to *see* things move in minutes, so the Grafana
**SLO & Error Budget** dashboard uses a short **30-minute rolling window** as a
stand-in. The maths is identical — only the window is shorter. When you run a
real service, change the windows in `monitoring/prometheus/rules/slo_rules.yml`
and the dashboard queries to `30d`.

## How to watch the budget burn

1. Start the stack: `docker compose up --build`
2. Open Grafana → **SLO & Error Budget** dashboard (<http://localhost:3000>).
3. Drive failing traffic and watch the budget drop and the burn rate climb:
   ```bash
   # 30% of these requests fail — well above our 0.1% budget
   while true; do curl -s "http://localhost:8080/work?fail_rate=0.3" > /dev/null; done
   ```
4. Stop the bad traffic and send healthy traffic; the rolling window recovers.

This is exactly the signal that drives **alerting** (Phase 4): when the burn
rate is too high for too long, you get paged.
