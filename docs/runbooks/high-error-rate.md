# Runbook: High Error Rate / Error-Budget Burn

**Alerts:** `ErrorBudgetFastBurn` (page), `ErrorBudgetSlowBurn` (ticket)
**SLO affected:** Availability (99.9% of requests succeed) — see [`../../SLO.md`](../../SLO.md)

A runbook is the checklist you follow when an alert fires, so you don't have to
think from scratch at 3am. Keep it short, ordered, and action-oriented.

---

## 1. Acknowledge

- Acknowledge the page so teammates know it's being handled.
- Note the start time — you'll need it for the postmortem timeline.

## 2. Assess impact (is it real, how bad?)

- Open the **"SLO & Error Budget"** Grafana dashboard (<http://localhost:3000>).
  - How negative is the error budget? What's the current burn rate?
- Open the **"Golden Signals"** dashboard.
  - Which endpoint is erroring? Is latency up too? Is traffic abnormal?
- Check Prometheus directly if needed:
  ```
  sum(rate(http_requests_total{http_status=~"5.."}[5m])) by (endpoint)
  ```

## 3. Find the likely cause

Work from most to least recent change:

- **Did we just deploy?** Check recent merges to `main` / the latest published
  image tag. A spike right after a deploy points at the new release.
- **Dependency failing?** Check logs for errors talking to databases/APIs.
- **Resource saturation?** Check the "requests in progress" panel and container
  resource use.
- **Bad input / traffic spike?** Check whether one endpoint or client dominates.

## 4. Mitigate first, fix later

Stop the bleeding before root-causing:

- **Roll back** to the last known-good image:
  ```bash
  docker pull ghcr.io/sayaksatpathi/reliability-lab:<previous-good-sha>
  # redeploy that tag
  ```
- If a specific feature is at fault, disable it (feature flag / config).
- If a dependency is down, fail gracefully or shed load.

## 5. Verify recovery

- Watch the error rate return to baseline and the burn rate drop below 1.
- The alert will move from FIRING back to resolved once the condition clears.

## 6. Close out

- Record end time.
- If this was user-impacting or burned meaningful budget, **write a postmortem**
  using [`../postmortem-template.md`](../postmortem-template.md).

---

### Quick reference

| Thing | Where |
|-------|-------|
| SLO dashboard | <http://localhost:3000> → "SLO & Error Budget" |
| Firing alerts | <http://localhost:9090/alerts> |
| Alertmanager | <http://localhost:9093> |
| SLO definitions | [`SLO.md`](../../SLO.md) |
