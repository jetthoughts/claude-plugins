#!/usr/bin/env bash
# Install the skill-estate validator as a local pre-commit hook.
#
#   bash scripts/install-hooks.sh
#
# The hook runs `python3 scripts/validate_skills.py` and aborts the commit on any
# ERROR (warnings are printed but do not block). Bypass a single commit with
# `git commit --no-verify` when you have a reason you can name out loud.
#
# This is the local half of the guardrail; .github/workflows/validate-skills.yml
# is the half that runs for everyone else.
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
hook="$root/.git/hooks/pre-commit"

if [ -e "$hook" ] && ! grep -q "validate_skills.py" "$hook"; then
  backup="$hook.bak-$(date +%Y%m%d-%H%M%S)"
  cp "$hook" "$backup"
  echo "existing pre-commit hook backed up to $backup"
fi

cat > "$hook" <<'HOOK'
#!/usr/bin/env bash
# Installed by scripts/install-hooks.sh — validates the skill estate before commit.
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "pre-commit: python3 not found; skipping skill validation" >&2
  exit 0
fi
if ! python3 -c "import yaml" >/dev/null 2>&1; then
  echo "pre-commit: PyYAML missing; skipping skill validation" >&2
  echo "            install it with: python3 -m pip install pyyaml" >&2
  exit 0
fi
cd "$root"
python3 scripts/validate_skills.py
HOOK

chmod +x "$hook"
echo "installed pre-commit hook at $hook"
echo "test it now:  python3 scripts/validate_skills.py"
