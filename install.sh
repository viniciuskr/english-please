#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DRY_RUN=0
PYTHON=python3

APT_PACKAGES=(
  python3-gi
  python3-gi-cairo
  gir1.2-gtk-4.0
  gir1.2-adw-1
  libgirepository-2.0-dev
  gcc
  libcairo2-dev
  pkg-config
  python3-venv
  python3-pip
)

usage() {
  cat <<'EOF'
English, Please — local installer (Ubuntu/Debian + GNOME)

Usage: ./install.sh [OPTIONS]

Options:
  --help, -h    Show this help
  --dry-run     Print planned actions without modifying the system

Installs system packages (apt), creates .venv, pip install -e ., and
registers the app in ~/.local for the GNOME applications menu.

Ollama is not installed by this script. After install, run:
  ollama serve
  ollama pull llama3.2

Manual install steps: see README.md
EOF
}

log() {
  echo "==> $*"
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] $*"
  else
    "$@"
  fi
}

die_non_debian() {
  echo "Error: This installer supports Debian/Ubuntu (apt) only." >&2
  echo "Install these packages manually, then follow README.md:" >&2
  printf '  %s\n' "${APT_PACKAGES[@]}" >&2
  exit 1
}

require_debian() {
  if [[ ! -f /etc/os-release ]]; then
    die_non_debian
  fi
  # shellcheck source=/dev/null
  source /etc/os-release
  case "${ID:-}:${ID_LIKE:-}" in
    ubuntu:*|debian:*|*:ubuntu*|*:debian*) return 0 ;;
  esac
  die_non_debian
}

resolve_python() {
  if "$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
    return 0
  fi
  if command -v python3.12 &>/dev/null; then
    PYTHON=python3.12
    if "$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
      return 0
    fi
  fi
  local ver
  ver="$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "unknown")"
  echo "Error: Python 3.12+ required (found ${ver})." >&2
  echo "Install python3.12 or upgrade python3, then re-run ./install.sh" >&2
  exit 1
}

install_apt_packages() {
  local missing=()
  local pkg
  for pkg in "${APT_PACKAGES[@]}"; do
    if ! dpkg -s "$pkg" &>/dev/null; then
      missing+=("$pkg")
    fi
  done
  if [[ ${#missing[@]} -eq 0 ]]; then
    log "All apt packages already installed"
    return 0
  fi
  log "Installing apt packages: ${missing[*]}"
  if ! command -v apt-get &>/dev/null; then
    echo "Error: apt-get not found." >&2
    die_non_debian
  fi
  run sudo apt-get update -qq
  run sudo apt-get install -y "${missing[@]}"
}

ensure_venv() {
  if [[ -d .venv ]]; then
    log "Virtualenv .venv already exists"
  else
    log "Creating virtualenv with ${PYTHON}"
    run "$PYTHON" -m venv .venv
  fi
}

pip_install_editable() {
  log "Installing english-please (editable) into .venv"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] .venv/bin/pip install -e ."
  else
    .venv/bin/pip install -q -e .
  fi
}

install_desktop_files() {
  local exec_path="${SCRIPT_DIR}/.venv/bin/english-please"
  local apps_dir="${HOME}/.local/share/applications"
  local icons_dir="${HOME}/.local/share/icons/hicolor/scalable/apps"
  local desktop_dst="${apps_dir}/com.viniciuskr.EnglishPlease.desktop"
  local icon_dst="${icons_dir}/com.viniciuskr.EnglishPlease.svg"

  log "Installing desktop entry (Exec=${exec_path})"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] mkdir -p ${apps_dir} ${icons_dir}"
    echo "[dry-run] write ${desktop_dst} with Exec=${exec_path}"
    echo "[dry-run] cp data/icons/com.viniciuskr.EnglishPlease.svg -> ${icon_dst}"
    echo "[dry-run] update-desktop-database ${apps_dir}"
    return 0
  fi

  mkdir -p "$apps_dir" "$icons_dir"
  sed "s|^Exec=.*|Exec=${exec_path}|" \
    data/com.viniciuskr.EnglishPlease.desktop >"$desktop_dst"
  cp data/icons/com.viniciuskr.EnglishPlease.svg "$icon_dst"
  if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$apps_dir"
  fi
}

print_success() {
  cat <<EOF

Install complete.

Run the app:
  ${SCRIPT_DIR}/.venv/bin/english-please

Or activate the venv:
  source ${SCRIPT_DIR}/.venv/bin/activate
  english-please

Optional: symlink for terminal use without activating the venv:
  ln -sf ${SCRIPT_DIR}/.venv/bin/english-please ~/.local/bin/english-please

Ollama (required for reviews):
  ollama serve
  ollama pull llama3.2

GNOME shortcut (optional): Settings → Keyboard → Custom Shortcuts
  Command: ${SCRIPT_DIR}/.venv/bin/english-please
  Suggested binding: Super+E

If you move this repository, re-run ./install.sh to refresh the desktop entry.
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help | -h)
        usage
        exit 0
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      *)
        echo "Unknown option: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
  done
}

main() {
  parse_args "$@"
  require_debian
  resolve_python
  install_apt_packages
  ensure_venv
  pip_install_editable
  install_desktop_files
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo
    echo "[dry-run] Install steps listed above; no changes made."
  else
    print_success
  fi
}

main "$@"
