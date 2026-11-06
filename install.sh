#!/usr/bin/env bash
# Bash 3.2+; no writes outside the selected skill directories and their receipts.
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[[ "$KIT_DIR" != *$'\n'* && "$KIT_DIR" != *$'\t'* ]] || { echo 'Distribution path contains tabs or line breaks.' >&2; exit 1; }
NAMES=(ndd-setup ndd-spec ndd-plan ndd-do)
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
CODEX_DIR="$HOME/.agents/skills"
WANT_CLAUDE=0 WANT_CODEX=0 UNINSTALL=0 DRY_RUN=0 REPLACE=0
MODE=copy
TARGETS=() LOCKS=() STAGES=() DESTS=() BACKUPS=() RECEIPTS=()
OLD_MOVED=() RECORD_MOVED=() NEW_INSTALLED=() NEW_RECORDED=()
SUCCESS=0

usage() {
  cat <<'HELP'
Usage: bash install.sh [--claude | --codex | --all] [options]
  --dry-run           show actions without writing anything
  --uninstall         permanently remove owned NDD skills and all NDD install state
  --replace           explicitly back up and replace conflicting/modified skills
  --link              development mode: link skills to this checkout
  --claude-dir PATH   select a custom Claude skills directory
  --codex-dir PATH    select a custom Codex skills directory
  -h, --help          show help
Without a target, detect existing agent directories; if none exist, use --all
or choose one agent explicitly. Receipts/backups live beside each skills
folder in <skills-directory>.ndd-kit. No project files are changed.
HELP
}
fail() { echo "Error: $*" >&2; exit 1; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude) WANT_CLAUDE=1 ;;
    --codex) WANT_CODEX=1 ;;
    --all) WANT_CLAUDE=1; WANT_CODEX=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --replace) REPLACE=1 ;;
    --link) MODE=link ;;
    --claude-dir|--codex-dir)
      [[ $# -ge 2 && -n "$2" && "$2" != --* ]] || fail "$1 needs a path"
      if [[ "$1" == --claude-dir ]]; then CLAUDE_DIR="$2"; WANT_CLAUDE=1
      else CODEX_DIR="$2"; WANT_CODEX=1; fi
      shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown option: $1 (use --help)" ;;
  esac
  shift
done
[[ $UNINSTALL -eq 0 || $REPLACE -eq 0 ]] || fail "--replace cannot be used with --uninstall; preserve modified files manually."
[[ $UNINSTALL -eq 0 || "$MODE" == copy ]] || fail "--link is an install option."
if [[ $WANT_CLAUDE -eq 0 && $WANT_CODEX -eq 0 ]]; then
  [[ -d "${CLAUDE_DIR%/skills}" ]] && WANT_CLAUDE=1
  [[ -d "${CODEX_HOME:-$HOME/.codex}" || -d "$HOME/.agents" ]] && WANT_CODEX=1
fi
[[ $WANT_CLAUDE -eq 1 || $WANT_CODEX -eq 1 ]] || fail "No agent detected. Select --claude, --codex, or --all."
[[ $WANT_CLAUDE -eq 0 ]] || TARGETS+=("$CLAUDE_DIR")
[[ $WANT_CODEX -eq 0 ]] || TARGETS+=("$CODEX_DIR")

if command -v shasum >/dev/null 2>&1; then
  hash() { shasum -a 256 | awk '{print $1}'; }
elif command -v sha256sum >/dev/null 2>&1; then
  hash() { sha256sum | awk '{print $1}'; }
else fail "SHA-256 utility missing (shasum or sha256sum)."; fi
exists() { [[ -e "$1" || -L "$1" ]]; }
# Reject symlinks and unusual names instead of following them during ownership checks.
fingerprint() (
  cd "$1" || exit 1
  find . -print | LC_ALL=C sort | while IFS= read -r path; do
    [[ "$path" == . ]] && continue
    [[ "$path" != *$'\t'* && ! -L "$path" ]] || exit 1
    if [[ -d "$path" ]]; then printf 'D\t%s\n' "$path"
    elif [[ -f "$path" ]]; then
      digest=$(hash < "$path") || exit 1
      printf 'F\t%s\t%s\n' "$digest" "$path"
    else exit 1; fi
  done | hash
)
# Ownership is enough for an explicitly requested uninstall, including local edits.
owned_receipt() {
  local record="$1" mode
  [[ -f "$record" && ! -L "$record" ]] || return 1
  [[ "$(sed -n '1p' "$record")" == ndd-kit-install-v1 ]] || return 1
  [[ "$(wc -l < "$record" | tr -d '[:space:]')" == 5 ]] || return 1
  mode=$(sed -n '3p' "$record")
  [[ "$mode" == copy || "$mode" == link ]]
}
# Receipts are data, never sourced as shell code.
owned_unchanged() {
  local dest="$1" record="$2" format mode source digest
  [[ -f "$record" && ! -L "$record" ]] || return 1
  format=$(sed -n '1p' "$record"); mode=$(sed -n '3p' "$record")
  source=$(sed -n '4p' "$record"); digest=$(sed -n '5p' "$record")
  [[ "$format" == ndd-kit-install-v1 ]] || return 1
  if [[ "$mode" == link ]]; then
    [[ -L "$dest" && "$(readlink "$dest")" == "$source" ]]
  elif [[ "$mode" == copy && -d "$dest" && ! -L "$dest" ]]; then
    local current
    current=$(fingerprint "$dest") || return 1
    [[ "$current" == "$digest" ]]
  else return 1; fi
}
# Do not traverse redirected destination parents or metadata directories.
check_path() {
  local path="$1" current="$1"
  [[ "$path" == /* && "$path" != / && "$path" != *$'\n'* && "$path" != *$'\t'* ]] || fail "Use an absolute, non-root path: $path"
  [[ "$path" != *//* ]] || fail "Use a path without repeated separators: $path"
  [[ "/$path/" != */../* && "/$path/" != */./* ]] || fail "Use a path without . or ..: $path"
  while [[ "$current" != / ]]; do
    [[ ! -L "$current" ]] || fail "Destination parent is a symlink: $current. Use its real path."
    [[ ! -e "$current" || -d "$current" ]] || fail "Not a directory: $current"
    current=$(dirname "$current")
  done
  current="$path"
  while [[ ! -d "$current" ]]; do current=$(dirname "$current"); done
  [[ -w "$current" ]] || fail "Directory is not writable: $current"
}
VERSION=unknown
if [[ $UNINSTALL -eq 0 ]]; then
  [[ -f "$KIT_DIR/skills/ndd-setup/VERSION" ]] || fail "Incomplete distribution: VERSION missing."
  VERSION=$(tr -d '[:space:]' < "$KIT_DIR/skills/ndd-setup/VERSION")
  [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail "Invalid VERSION."
  for name in "${NAMES[@]}"; do
    src="$KIT_DIR/skills/$name"
    [[ ! -L "$src" && -f "$src/SKILL.md" && -f "$src/agents/openai.yaml" ]] || fail "Incomplete or linked distribution: $name"
    fingerprint "$src" >/dev/null || fail "Unsupported source entry in $src"
  done
  for asset in spec.md plan.md; do
    [[ -f "$KIT_DIR/skills/ndd-setup/assets/$asset" ]] || fail "Missing asset: $asset"
  done
fi
# Preflight every selected target before the first write.
for i in "${!TARGETS[@]}"; do
  target="${TARGETS[$i]%/}"; TARGETS[$i]="$target"
  check_path "$target"; check_path "$target.ndd-kit"
  if [[ $UNINSTALL -eq 0 ]]; then check_path "$target.ndd-kit/backups"; fi
  case "$target/" in "$KIT_DIR/"*) fail "Cannot install inside the distribution." ;; esac
  for name in "${NAMES[@]}"; do
    case "$KIT_DIR/" in "$target/$name/"*|"$target.ndd-kit/"*) fail "Distribution overlaps the installation destination." ;; esac
  done
  for other in "${TARGETS[@]:0:$i}"; do
    case "$target/" in "$other/"*|"$other.ndd-kit/"*) fail "Targets must not overlap." ;; esac
    case "$other/" in "$target/"*|"$target.ndd-kit/"*) fail "Targets must not overlap." ;; esac
  done
  echo "Target: $target"
  for name in "${NAMES[@]}"; do
    dest="$target/$name"; record="$target.ndd-kit/$name.receipt"
    [[ ! -L "$record" && ( ! -e "$record" || -f "$record" ) ]] || fail "Invalid receipt: $record"
    if [[ $UNINSTALL -eq 1 ]]; then
      if exists "$dest"; then
        owned_receipt "$record" || fail "Cannot establish NDD ownership: $dest. No files removed."
        echo "  Permanently remove (including local edits): $name"
      else echo "  Absent: $name"; fi
    elif exists "$dest" && ! owned_unchanged "$dest" "$record"; then
      [[ $REPLACE -eq 1 ]] || fail "Unowned or modified skill: $dest. Back it up/move it manually, or install with --replace after reviewing --dry-run."
      echo "  BACK UP and replace: $name"
    else echo "  Install $VERSION ($MODE): $name"; fi
  done
  if [[ $UNINSTALL -eq 1 && -d "$target.ndd-kit" ]]; then
    echo "  Permanently remove all receipts, backups and staging files: $target.ndd-kit"
  fi
done
[[ $DRY_RUN -eq 0 ]] || { echo 'Dry run: no files changed.'; exit 0; }

# Uninstall deliberately has no backup or rollback. Keep the lock until all
# contents have been removed, then remove the empty metadata directory.
if [[ $UNINSTALL -eq 1 ]]; then
  cleanup_uninstall() {
    local result=$? path
    set +e
    if [[ $result -ne 0 ]]; then
      echo 'Uninstall incomplete; already deleted files have no backup. Fix the reported error and rerun.' >&2
    fi
    if [[ ${#LOCKS[@]} -gt 0 ]]; then
      for path in "${LOCKS[@]}"; do
        [[ -z "$path" ]] || rmdir "$path" || result=1
      done
    fi
    return "$result"
  }
  trap cleanup_uninstall EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  for target in "${TARGETS[@]}"; do
    [[ -d "$target.ndd-kit" ]] || continue
    mkdir "$target.ndd-kit/lock" 2>/dev/null || fail "Install lock exists: $target.ndd-kit/lock. Check for an active/interrupted install."
    LOCKS+=("$target.ndd-kit/lock")
  done
  for target in "${TARGETS[@]}"; do
    [[ -d "$target.ndd-kit" ]] || continue
    for name in "${NAMES[@]}"; do
      dest="$target/$name"
      if exists "$dest"; then
        owned_receipt "$target.ndd-kit/$name.receipt" || fail "Ownership changed: $dest"
        # rm never follows a removed symlink, including nested backup links.
        rm -rf -- "$dest"
        echo "  Removed: $name"
      fi
    done
    for entry in "$target.ndd-kit"/* "$target.ndd-kit"/.[!.]* "$target.ndd-kit"/..?*; do
      exists "$entry" || continue
      [[ "$entry" == "$target.ndd-kit/lock" ]] && continue
      rm -rf -- "$entry"
    done
    for i in "${!LOCKS[@]}"; do
      if [[ "${LOCKS[$i]}" == "$target.ndd-kit/lock" ]]; then
        rmdir "${LOCKS[$i]}"; LOCKS[$i]=''
      fi
    done
    rmdir "$target.ndd-kit"
  done
  echo 'NDD skills and install state removed. No backups retained. Project files and source checkout preserved.'
  exit 0
fi

cleanup() {
  local exit_status=$? i recovery_failed=0
  set +e
  if [[ $SUCCESS -ne 1 ]]; then
    echo 'Installation failed; restoring previous skills and receipts.' >&2
    for ((i=${#DESTS[@]}-1; i>=0; i--)); do
      [[ "${NEW_INSTALLED[$i]}" == 0 ]] || rm -rf "${DESTS[$i]}" || recovery_failed=1
      [[ "${NEW_RECORDED[$i]}" == 0 ]] || rm -f "${RECEIPTS[$i]}" || recovery_failed=1
      [[ "${OLD_MOVED[$i]}" == 0 ]] || mv "${BACKUPS[$i]}/skill" "${DESTS[$i]}" || recovery_failed=1
      [[ "${RECORD_MOVED[$i]}" == 0 ]] || mv "${BACKUPS[$i]}/receipt" "${RECEIPTS[$i]}" || recovery_failed=1
    done
  fi
  if [[ ${#STAGES[@]} -gt 0 ]]; then
    for path in "${STAGES[@]}"; do rm -rf "$path" || recovery_failed=1; done
  fi
  if [[ ${#LOCKS[@]} -gt 0 ]]; then
    for path in "${LOCKS[@]}"; do rmdir "$path" || recovery_failed=1; done
  fi
  if [[ $recovery_failed -ne 0 ]]; then
    echo 'Cleanup/restore incomplete. Inspect the printed backup paths before retrying.' >&2
    return 1
  fi
  return "$exit_status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Lock all targets before changing any skills. Never clear an existing lock.
for target in "${TARGETS[@]}"; do
  mkdir -p "$target.ndd-kit"
  mkdir "$target.ndd-kit/lock" 2>/dev/null || fail "Install lock exists: $target.ndd-kit/lock. Check for an active/interrupted install."
  LOCKS+=("$target.ndd-kit/lock")
done
for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for name in "${NAMES[@]}"; do
    dest="$target/$name"; record="$target.ndd-kit/$name.receipt"
    # Recheck after acquiring the lock; never silently adopt changed destinations.
    if exists "$dest" && ! owned_unchanged "$dest" "$record" && [[ $REPLACE -eq 0 ]]; then fail "Destination changed: $dest"; fi
    stage=$(mktemp -d "$target.ndd-kit/stage.XXXXXX"); STAGES+=("$stage")
    src="$KIT_DIR/skills/$name"
    if [[ "$MODE" == link ]]; then ln -s "$src" "$stage/skill"
    else cp -R "$src" "$stage/skill"; fi
    digest=$(fingerprint "$src")
    [[ "$(fingerprint "$stage/skill")" == "$digest" ]] || fail "Copy verification failed: $name"
    printf 'ndd-kit-install-v1\n%s\n%s\n%s\n%s\n' "$VERSION" "$MODE" "$src" "$digest" > "$stage/receipt"
    mkdir -p "$target.ndd-kit/backups"
    backup=$(mktemp -d "$target.ndd-kit/backups/$name.XXXXXX")
    idx=${#DESTS[@]}
    DESTS+=("$dest"); BACKUPS+=("$backup"); RECEIPTS+=("$record")
    OLD_MOVED+=(0); RECORD_MOVED+=(0); NEW_INSTALLED+=(0); NEW_RECORDED+=(0)
    if exists "$dest"; then mv "$dest" "$backup/skill"; OLD_MOVED[$idx]=1; fi
    if [[ -f "$record" ]]; then mv "$record" "$backup/receipt"; RECORD_MOVED[$idx]=1; fi
    mv "$stage/skill" "$dest"; NEW_INSTALLED[$idx]=1
    mv "$stage/receipt" "$record"; NEW_RECORDED[$idx]=1
    if [[ ${OLD_MOVED[$idx]} -eq 1 || ${RECORD_MOVED[$idx]} -eq 1 ]]; then
      echo "  Saved previous state: $backup"
    else echo "  Installed: $name"; fi
  done
done
SUCCESS=1
printf '\nInstalled NDD %s. In your project use /ndd-setup (Claude Code) or $ndd-setup (Codex).\n' "$VERSION"
echo 'Restart the agent if the skills do not appear.'
