#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="${ROOT_DIR}/backups"
mkdir -p "${BACKUP_DIR}"

source "${ROOT_DIR}/.env"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="${BACKUP_DIR}/team_signup_${STAMP}.sql.gz"

docker compose -f "${ROOT_DIR}/docker-compose.yml" exec -T mysql \
  mysqldump -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}" \
  | gzip > "${OUT}"

echo "Backup written: ${OUT}"
