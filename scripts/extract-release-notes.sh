#!/usr/bin/env bash
# Extracts the body of the top-most versioned section from CHANGELOG.md to stdout.
set -euo pipefail

notes=$(awk 'found && /^## \[/{exit} /^## \[/{found=1; next} found{print}' CHANGELOG.md)

if [ -z "${notes// }" ]; then
  echo "Could not extract release notes from CHANGELOG.md" >&2
  exit 1
fi

echo "$notes"
