// k6 load test for the sample service.
//
// Ramps virtual users up, holds, then ramps down, hitting /work. The
// thresholds encode mini-SLOs: the test FAILS (non-zero exit) if too many
// requests error or get too slow — handy as a release gate in CI.
//
// Run with Docker (no install needed):
//   docker run --rm -i --add-host=host.docker.internal:host-gateway \
//     -e TARGET=http://host.docker.internal:8080 grafana/k6 run - < load/k6-load.js
//
// Or natively if you have k6 installed:
//   k6 run load/k6-load.js
//
// Tunables (env vars): TARGET, FAIL_RATE, MAX_MS
import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.TARGET || "http://localhost:8080";
const FAIL_RATE = __ENV.FAIL_RATE || "0.05";
const MAX_MS = __ENV.MAX_MS || "400";

export const options = {
  stages: [
    { duration: "30s", target: 20 }, // ramp up to 20 virtual users
    { duration: "1m", target: 20 }, // hold steady
    { duration: "30s", target: 0 }, // ramp down
  ],
  thresholds: {
    http_req_failed: ["rate<0.10"], // <10% of requests may fail
    http_req_duration: ["p(95)<800"], // 95th-percentile latency under 800ms
  },
};

export default function () {
  const res = http.get(`${BASE}/work?fail_rate=${FAIL_RATE}&max_ms=${MAX_MS}`);
  check(res, { "status is 200": (r) => r.status === 200 });
  sleep(0.5);
}
