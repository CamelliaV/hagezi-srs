#!/usr/bin/env python3
"""Build sing-box rule-sets from the official HaGeZi DNS blocklists.

Source: https://hagezi-mirror.dnsbunker.org/adblock/ (official mirror, 4-8h builds)
Output: dist/{pro,tif}.srs, published to the `ruleset` branch by CI.
"""
import json
import os
import subprocess
import sys
import urllib.request

BASE = os.environ.get("HAGEZI_BASE", "https://hagezi-mirror.dnsbunker.org/adblock")
LISTS = {
    # name: (source file, minimum sane domain count)
    "pro": ("pro.txt", 200_000),
    "tif": ("tif.txt", 1_600_000),
}


def fetch(name):
    with urllib.request.urlopen(f"{BASE}/{name}", timeout=180) as resp:
        return resp.read().decode("utf-8", "replace")


def domains(text):
    out = set()
    for line in text.splitlines():
        line = line.strip()
        if not (line.startswith("||") and line.endswith("^")):
            continue
        domain = line[2:-1].lower().rstrip(".")
        if not domain or "/" in domain or " " in domain or "@" in domain:
            continue
        out.add(domain)
    return out


def main():
    os.makedirs("dist", exist_ok=True)
    manifest = {}
    for name, (filename, minimum) in LISTS.items():
        found = domains(fetch(filename))
        if len(found) < minimum:
            sys.exit(f"{filename}: only {len(found)} domains (< {minimum}), refusing to publish")
        source_json = f"dist/{name}.json"
        with open(source_json, "w", encoding="utf-8") as handle:
            json.dump({"version": 3, "rules": [{"domain_suffix": sorted(found)}]}, handle)
        subprocess.run(
            ["sing-box", "rule-set", "compile", source_json, "-o", f"dist/{name}.srs"],
            check=True,
        )
        os.remove(source_json)
        manifest[name] = {
            "source": f"{BASE}/{filename}",
            "domains": len(found),
            "bytes": os.path.getsize(f"dist/{name}.srs"),
        }
        print(name, manifest[name], flush=True)
    with open("dist/manifest.json", "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=1)


if __name__ == "__main__":
    main()
