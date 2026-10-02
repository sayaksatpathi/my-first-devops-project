#!/usr/bin/env bash
#
# Chaos experiment: inject elevated errors + latency, then watch the system.
#
# The scientific method applied to reliability:
#   1. Steady-state hypothesis: "the service stays within its SLO."
#   2. Inject a real-world fault (here: a burst of 5xx errors + slow responses).
#   3. Observe whether the hypothesis holds — and whether your alerts catch it.
#   4. Stop the fault and confirm the system recovers.
#   5. Write down what you learned (see docs/postmortem-template.md).
#
# While this runs, watch:
#   - Grafana  http://localhost:3000  ("SLO & Error Budget" + "Golden Signals")
#   - Prometheus alerts  http://localhost:9090/alerts   (PENDING -> FIRING)
#   - Alertmanager  http://localhost:9093                (grouped firing alerts)
#
# Usage:  ./load/chaos.sh            # defaults below
#         FAIL_RATE=0.5 DURATION=180 ./load/chaos.sh
set -euo pipefail

TARGET="${TARGET:-http://localhost:8080}"
FAIL_RATE="${FAIL_RATE:-0.3}"   # 30% of requests fail — far above the 0.1% budget
MAX_MS="${MAX_MS:-800}"         # latency up to 800ms (SLO is 500ms)
DURATION="${DURATION:-120}"     # seconds of chaos

echo "💥 Injecting chaos at ${TARGET} for ${DURATION}s"
echo "   fail_rate=${FAIL_RATE}  max_ms=${MAX_MS}"
echo "   Watch Grafana / Prometheus /alerts / Alertmanager now..."

end=$((SECONDS + DURATION))
reqs=0
while [ $SECONDS -lt $end ]; do
  curl -s -o /dev/null "${TARGET}/work?fail_rate=${FAIL_RATE}&max_ms=${MAX_MS}" || true
  reqs=$((reqs + 1))
done

echo "✅ Chaos finished after ${reqs} requests."
echo "   Now send healthy traffic to watch the error budget recover, e.g.:"
echo "   while true; do curl -s \"${TARGET}/work?fail_rate=0&max_ms=100\" >/dev/null; done"
