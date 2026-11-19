#!/usr/bin/env python3
"""Dekodiert die in Chrome erzeugten Ortsteil-Polylines (Praezision 1e-4) -> JSON {"Stadt|Ortsteil": [ring, ...]}."""
import json, sys

def dec(s):
    pts = []; i = 0; x = y = 0
    while i < len(s):
        vals = []
        for _ in range(2):
            r = sh = 0
            while True:
                if i >= len(s):
                    return None
                b = ord(s[i]) - 63; i += 1; r |= (b & 0x1f) << sh; sh += 5
                if b < 0x20:
                    break
            vals.append(~(r >> 1) if r & 1 else r >> 1)
        y += vals[0]; x += vals[1]; pts.append((x / 1e4, y / 1e4))
    return pts

def ok(r):
    return r and len(r) > 3 and r[0] == r[-1]

def split(v):
    r = dec(v)
    if ok(r):
        return [r]
    for j, c in enumerate(v):          # '~' ist auch ein gueltiges Polyline-Zeichen -> Trennstelle suchen, an der alle Teile geschlossen sind
        if c == '~':
            a = dec(v[:j]); rest = split(v[j + 1:])
            if ok(a) and rest:
                return [a] + rest
    return None

res = {}
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.rstrip("\n")
    if "=" not in line:
        continue
    k, v = line.split("=", 1)
    rings = split(v)
    print(k, "ok" if rings else "FEHLER", [len(r) for r in rings] if rings else "")
    if rings:
        res[k] = rings
json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False)
