# Postmortem: <short incident title>

> Copy this file to `docs/postmortems/YYYY-MM-DD-<slug>.md` and fill it in after
> any incident that impacted users or burned meaningful error budget.

**Postmortems are blameless.** The goal is to fix *systems and processes*, not
to assign fault. People act reasonably given the information they had; if a
human could cause this, the system allowed it to happen.

---

## Summary

_One or two sentences: what happened, who was affected, for how long._

## Impact

- **Duration:** <start time> → <end time> (<total>)
- **User impact:** _e.g. ~X% of requests returned errors; feature Y unavailable._
- **Error budget spent:** _e.g. consumed ~Z% of the monthly availability budget._

## Timeline

_All times in one timezone. Facts only._

| Time | Event |
|------|-------|
| 00:00 | _Deploy of vX.Y.Z to main_ |
| 00:03 | _`ErrorBudgetFastBurn` alert fired_ |
| 00:05 | _On-call acknowledged; began investigating_ |
| 00:12 | _Rolled back to previous image_ |
| 00:15 | _Error rate back to baseline; alert resolved_ |

## Root cause

_What actually caused it. Go beyond the trigger to the underlying reason
(the "5 whys" can help). Example: "A null config value wasn't validated, so
the new release crashed on the first request to /work."_

## Detection

- How was it detected (alert / dashboard / user report)?
- Did detection work well? Could it have been faster?

## Resolution

_What actually fixed it (mitigation) and what the permanent fix is._

## What went well

- _e.g. The burn-rate alert fired within 3 minutes._

## What went poorly

- _e.g. We had no quick rollback command documented._

## Action items

_Concrete, assigned, and tracked. Prevent recurrence and improve response._

| Action | Owner | Due | Tracking |
|--------|-------|-----|----------|
| _Add config validation on startup_ | | | #issue |
| _Document one-command rollback in the runbook_ | | | #issue |
| _Add an alert for dependency errors_ | | | #issue |
