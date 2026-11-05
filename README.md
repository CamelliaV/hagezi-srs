# hagezi-srs

Sing-box rule-sets built from the official [HaGeZi DNS blocklists](https://github.com/hagezi/dns-blocklists).

- Source: `https://hagezi-mirror.dnsbunker.org/adblock/` (official mirror, rebuilt every 4-8 h)
- Build: `build.py` extracts `||domain^` entries, emits a sing-box source rule-set
  (`domain_suffix`), then compiles it with `sing-box rule-set compile`.
- CI: GitHub Actions runs daily at 03:17 UTC, plus on demand; artifacts are force-pushed
  to the orphan `ruleset` branch.

## Files

| File | Domains (approx.) | Purpose |
|---|---:|---|
| `pro.srs` | 222k | HaGeZi Multi PRO: ads, trackers, telemetry, malware/phishing |
| `tif.srs` | 1.71M | HaGeZi Threat Intelligence Feeds: malware, phishing, C2 |

Raw URLs:

```
https://raw.githubusercontent.com/CamelliaV/hagezi-srs/ruleset/pro.srs
https://raw.githubusercontent.com/CamelliaV/hagezi-srs/ruleset/tif.srs
```

## Usage (sing-box / Karing)

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "hagezi-pro",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/CamelliaV/hagezi-srs/ruleset/pro.srs",
        "download_detour": "direct"
      }
    ],
    "rules": [{ "rule_set": ["hagezi-pro"], "action": "reject" }]
  }
}
```

## License

The blocklists are © HaGeZi and licensed under GPL-3.0. This repository only
converts them to the sing-box rule-set format; see [LICENSE](LICENSE).
