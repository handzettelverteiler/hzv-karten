#!/usr/bin/env bash
# Veroeffentlicht Karten-HTML auf GitHub Pages.
# Aufruf: tools/publish.sh <datei.html> [weitere.html ...]
# Ergebnis: https://handzettelverteiler.github.io/hzv-karten/<dateiname>.html (nach 1-2 Min.)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
git pull -q --rebase origin main || true
for f in "$@"; do
  name="$(basename "$f")"
  [ "$(realpath "$f")" = "$REPO/$name" ] || cp "$f" "$REPO/$name"
  git add "$name"
done
if git diff --cached --quiet; then echo "Keine Aenderungen."; exit 0; fi
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "Karte(n): $*

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin HEAD:main
for f in "$@"; do echo "https://handzettelverteiler.github.io/hzv-karten/$(basename "$f")"; done
