#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

MODE="${1:-}"
COMPOSE=(docker compose -f docker-compose.yml)

if [[ "${MODE}" == "prod" ]]; then
  COMPOSE+=( -f docker-compose.prod.yml )
elif [[ -n "${MODE}" && "${MODE}" != "dev" ]]; then
  echo "Usage: $0 [dev|prod]" >&2
  exit 1
fi

echo "==> Stopping host nginx/gunicorn if present (free ports 80/443)"
systemctl stop nginx 2>/dev/null || true
systemctl disable nginx 2>/dev/null || true
for unit in $(systemctl list-units --type=service --all 2>/dev/null | awk '/gunicorn/ {print $1}'); do
  systemctl stop "${unit}" 2>/dev/null || true
  systemctl disable "${unit}" 2>/dev/null || true
done

echo "==> Building and starting containers"
"${COMPOSE[@]}" up -d --build

echo "==> Waiting for web healthcheck"
deadline=120
elapsed=0
while (( elapsed < deadline )); do
  if "${COMPOSE[@]}" ps web 2>/dev/null | grep -q '(healthy)'; then
    break
  fi
  sleep 3
  elapsed=$((elapsed + 3))
done

echo "==> HTTP healthcheck"
curl -sf "http://127.0.0.1/healthz/" >/dev/null && echo "HTTP /healthz/ OK"

if [[ "${MODE}" == "prod" ]]; then
  curl -sfk "https://127.0.0.1/healthz/" >/dev/null && echo "HTTPS /healthz/ OK" || \
    echo "WARN: HTTPS check failed — configure certbot and docker.prod.conf domain paths"
fi

"${COMPOSE[@]}" ps
