#!/usr/bin/env bash
# Deploy the portfolio to the droplet: build the frontend locally, copy the
# backend (with the frontend build baked in), rebuild the container.
#
# Usage:  bash deploy/deploy.sh          (from the Portfolio folder)

set -euo pipefail

DROPLET="root@137.184.200.179"
REMOTE_DIR="/opt/portfolio"
HERE="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Building frontend (production, same origin API)"
cd "$HERE/frontend"
VITE_API_BASE="" npm run build

echo "==> Staging frontend build into backend/frontend_dist"
rm -rf "$HERE/backend/frontend_dist"
cp -r "$HERE/frontend/dist" "$HERE/backend/frontend_dist"

echo "==> Copying to the droplet"
ssh "$DROPLET" "mkdir -p $REMOTE_DIR"
tar czf - -C "$HERE" \
  --exclude='backend/venv' --exclude='backend/__pycache__' \
  --exclude='backend/*/__pycache__' --exclude='backend/*/*/__pycache__' \
  --exclude='backend/db.sqlite3' --exclude='backend/media' \
  --exclude='backend/staticfiles' \
  backend deploy/docker-compose.yml \
  | ssh "$DROPLET" "tar xzf - -C $REMOTE_DIR && mv -f $REMOTE_DIR/deploy/docker-compose.yml $REMOTE_DIR/docker-compose.yml && rmdir $REMOTE_DIR/deploy 2>/dev/null || true"

echo "==> Rebuilding and restarting the container"
ssh "$DROPLET" "cd $REMOTE_DIR && docker compose build && docker compose up -d"

echo ""
echo "Done. First-time checklist (once, on the droplet):"
echo "  1. Put a filled-in .env at $REMOTE_DIR/.env (see env.production.example)"
echo "  2. docker exec portfolio-web python manage.py seed_portfolio"
echo "  3. Create your admin user"
echo "  4. Append deploy/Caddyfile.snippet to /opt/lewa/deploy/Caddyfile and reload Caddy"
