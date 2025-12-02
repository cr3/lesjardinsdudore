#!/usr/bin/env bash
set -euo pipefail

: "${SAMBA_USER:=smbuser}"
: "${SAMBA_PASS:=smbpass}"
: "${SAMBA_UID:=1000}"
: "${SAMBA_GID:=1000}"

# Ensure group/user exist with desired ids (so files on host have sane ownership)
if ! getent group "${SAMBA_GID}" >/dev/null 2>&1; then
  groupadd -g "${SAMBA_GID}" smbgroup
fi

if ! id -u "${SAMBA_USER}" >/dev/null 2>&1; then
  useradd -m -u "${SAMBA_UID}" -g "${SAMBA_GID}" -s /usr/sbin/nologin "${SAMBA_USER}"
fi

# Set Linux password (not strictly needed for Samba, but harmless)
echo "${SAMBA_USER}:${SAMBA_PASS}" | chpasswd

# Add to Samba user database (idempotent)
(echo "${SAMBA_PASS}"; echo "${SAMBA_PASS}") | smbpasswd -s -a "${SAMBA_USER}" || true
smbpasswd -e "${SAMBA_USER}" || true

# Make sure share folders exist and are owned by our forced user
mkdir -p /data/public /data/private
chown -R "${SAMBA_UID}:${SAMBA_GID}" /data

# Map “smbuser” used in smb.conf to our UNIX user
# (If SAMBA_USER ≠ smbuser, create an alias account named smbuser that shares the same uid/gid)
if [ "${SAMBA_USER}" != "smbuser" ]; then
  if ! id -u smbuser >/dev/null 2>&1; then
    useradd -M -u "${SAMBA_UID}" -g "${SAMBA_GID}" -s /usr/sbin/nologin smbuser
  fi
fi

exec "$@"
