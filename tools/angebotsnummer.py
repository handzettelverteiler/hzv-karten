#!/usr/bin/env python3
"""Angebotsnummern + Angebotsregister für HZV (Stefan, 09.11.2026).

Format: JJMM-NN, z. B. 2611-03 = drittes Angebot im November 2026. Laufende Nummer beginnt jeden Monat bei 01.
Neue Fassung desselben Angebots (andere Menge, Korrektur): Versionssuffix -2, -3 … (z. B. 2611-09-2).
Register: daten/angebote_register.csv (eine Zeile je Angebotsnummer/Version). Status: offen | beauftragt | verloren | storniert.

Aufrufe (immer aus dem Repo heraus; synchronisiert per git pull/commit/push, damit parallele Sitzungen
– z. B. der Postfach-Check – keine Nummer doppelt vergeben):
  python3 tools/angebotsnummer.py neu --kunde "Kröhnke Ingenieure GmbH" [--gebiet "Essen"] [--datum 2026-11-09]
  python3 tools/angebotsnummer.py version --nr 2611-09 [--notiz "20.000 statt 10.000 Flyer"]
  python3 tools/angebotsnummer.py setze --nr 2611-41 --netto 1635,00 --flyer 15000 --kartenlink URL --datei "Angebot_…docx" --status beauftragt
  python3 tools/angebotsnummer.py offen [--tage 5]     # offene Angebote, älter als N Tage (Nachfassen)
  python3 tools/angebotsnummer.py zeige --nr 2611-41
Option --ohne-git: nur lokal schreiben (Tests).
"""
import argparse, csv, datetime, os, re, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REG = os.path.join(REPO, "daten", "angebote_register.csv")
COLS = ["nr", "datum", "kunde", "gebiet", "flyer", "netto", "kartenlink", "ordner", "datei", "status", "notiz"]


def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, check=check)


def lesen():
    if not os.path.exists(REG):
        return []
    with open(REG, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def schreiben(rows):
    os.makedirs(os.path.dirname(REG), exist_ok=True)
    with open(REG, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in sorted(rows, key=lambda r: nr_key(r["nr"])):
            w.writerow({c: r.get(c, "") for c in COLS})


def nr_key(nr):
    m = re.match(r"(\d{4})-(\d+)(?:-(\d+))?$", nr)
    return (m.group(1), int(m.group(2)), int(m.group(3) or 1)) if m else (nr, 0, 0)


def heute():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Berlin")).date()
    except Exception:
        return datetime.date.today()


def transaktion(fn, ohne_git=False, msg="Angebotsregister"):
    """pull -> fn(rows) -> schreiben -> commit -> push (bei Konflikt einmal neu)."""
    for versuch in range(3):
        if not ohne_git:
            git("pull", "-q", "--rebase", "origin", "main", check=False)
        rows = lesen()
        ergebnis = fn(rows)
        schreiben(rows)
        if ohne_git:
            return ergebnis
        git("add", REG)
        if git("diff", "--cached", "--quiet", check=False).returncode == 0:
            return ergebnis
        git("-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-qm",
            f"{msg}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
        if git("push", "-q", "origin", "HEAD:main", check=False).returncode == 0:
            return ergebnis
        git("reset", "-q", "--hard", "HEAD~1")  # Konflikt: lokalen Commit verwerfen, neu ziehen, neu vergeben
    sys.exit("Push fehlgeschlagen – Register nicht aktualisiert")


def finde(rows, nr):
    for r in rows:
        if r["nr"] == nr:
            return r
    sys.exit(f"Angebotsnummer {nr} nicht im Register")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("befehl", choices=["neu", "version", "setze", "offen", "zeige"])
    ap.add_argument("--nr"); ap.add_argument("--kunde"); ap.add_argument("--gebiet"); ap.add_argument("--datum")
    ap.add_argument("--flyer"); ap.add_argument("--netto"); ap.add_argument("--kartenlink"); ap.add_argument("--ordner")
    ap.add_argument("--datei"); ap.add_argument("--status"); ap.add_argument("--notiz"); ap.add_argument("--tage", type=int, default=5)
    ap.add_argument("--ohne-git", action="store_true")
    a = ap.parse_args()
    felder = {k: getattr(a, k) for k in ["kunde", "gebiet", "flyer", "netto", "kartenlink", "ordner", "datei", "status", "notiz"] if getattr(a, k) is not None}

    if a.befehl == "neu":
        if not a.kunde:
            sys.exit("--kunde fehlt")
        d = datetime.date.fromisoformat(a.datum) if a.datum else heute()
        jjmm = d.strftime("%y%m")

        def f(rows):
            n = max([int(r["nr"].split("-")[1]) for r in rows if r["nr"].startswith(jjmm + "-")] or [0]) + 1
            nr = f"{jjmm}-{n:02d}"
            rows.append({"nr": nr, "datum": d.isoformat(), "status": "offen", **felder})
            return nr
        print(transaktion(f, a.ohne_git, f"Angebotsnummer vergeben ({a.kunde})"))

    elif a.befehl == "version":
        basis = re.match(r"(\d{4}-\d+)", a.nr or "")
        if not basis:
            sys.exit("--nr fehlt (z. B. 2611-09)")
        basis = basis.group(1)

        def f(rows):
            alt = finde(rows, basis)
            v = max([nr_key(r["nr"])[2] for r in rows if re.match(re.escape(basis) + r"(-\d+)?$", r["nr"])]) + 1
            nr = f"{basis}-{v}"
            neu = {**alt, "nr": nr, "datum": (datetime.date.fromisoformat(a.datum) if a.datum else heute()).isoformat(),
                   "status": "offen", "notiz": "", **felder}
            rows.append(neu)
            return nr
        print(transaktion(f, a.ohne_git, f"Angebotsversion {basis}"))

    elif a.befehl == "setze":
        def f(rows):
            finde(rows, a.nr).update(felder)
            return a.nr
        print(transaktion(f, a.ohne_git, f"Angebotsregister {a.nr} aktualisiert"))

    elif a.befehl == "offen":
        if not a.ohne_git:
            git("pull", "-q", "--rebase", "origin", "main", check=False)
        grenze = heute() - datetime.timedelta(days=a.tage)
        for r in lesen():
            if r["status"] == "offen" and datetime.date.fromisoformat(r["datum"]) <= grenze:
                print(";".join(r.get(c, "") for c in COLS))

    elif a.befehl == "zeige":
        for r in lesen():
            if r["nr"].startswith(a.nr or ""):
                print(";".join(r.get(c, "") for c in COLS))


if __name__ == "__main__":
    main()
