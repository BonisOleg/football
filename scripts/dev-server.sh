#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PORT="${DEV_PORT:-8001}"
HOST="${DEV_HOST:-127.0.0.1}"
PID_FILE="$ROOT/.dev-server.pid"
PORT_FILE="$ROOT/.dev-port"
LOG_FILE="$ROOT/.dev-server.log"

if [[ ! -f "$ROOT/.env" ]]; then
  cp .env.example .env
fi

# shellcheck source=/dev/null
source "$ROOT/.venv/bin/activate"

find_free_port() {
  local port="$1"
  while lsof -iTCP:"$port" -sTCP:LISTEN -P -n >/dev/null 2>&1; do
    port=$((port + 1))
  done
  echo "$port"
}

stop_server() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid="$(cat "$PID_FILE")"
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid"
      echo "Зупинено dev-сервер (PID $pid)."
    fi
    rm -f "$PID_FILE"
  fi
}

start_server() {
  stop_server

  PORT="$(find_free_port "$PORT")"
  echo "$PORT" > "$PORT_FILE"

  nohup python manage.py runserver "$HOST:$PORT" >>"$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"

  echo "Dev-сервер запущено: http://$HOST:$PORT/"
  echo "PID: $(cat "$PID_FILE"), лог: $LOG_FILE"
}

status_server() {
  if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    local port
    port="$(cat "$PORT_FILE" 2>/dev/null || echo "?")"
    echo "Працює (PID $(cat "$PID_FILE")): http://$HOST:$port/"
  else
    echo "Dev-сервер не запущено."
    exit 1
  fi
}

case "${1:-start}" in
  start) start_server ;;
  stop) stop_server ;;
  restart) stop_server; start_server ;;
  status) status_server ;;
  *)
    echo "Використання: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac
