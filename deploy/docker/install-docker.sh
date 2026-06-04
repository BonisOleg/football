#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  echo "Docker already installed: $(docker --version)"
  exit 0
fi

curl -fsSL https://get.docker.com | sh
usermod -aG docker "${SUDO_USER:-$USER}" 2>/dev/null || true
echo "Docker installed. Re-login or run: newgrp docker"
