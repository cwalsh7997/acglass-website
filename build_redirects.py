#!/usr/bin/env python3
"""Merge new 301 redirects into existing vercel.json, preserving existing entries."""
import json, os

REPO = "/home/user/workspace/acglass-website"
vj_path = os.path.join(REPO, "vercel.json")

with open(vj_path) as f:
    cfg = json.load(f)

existing = cfg.get("redirects", [])
existing_sources = {r["source"] for r in existing}

# New redirects to add. Targets verified to exist in repo.
# (source, destination)
new_pairs = [
    # Ocean Prime case study + blog + folder variants  -> portfolio
    ("/case-study-ocean-prime-fort-lauderdale.html", "/portfolio.html"),
    ("/case-study-ocean-prime.html", "/portfolio.html"),
    ("/ocean-prime-fort-lauderdale/", "/portfolio.html"),
    ("/ocean-prime-fort-lauderdale", "/portfolio.html"),
    ("/ocean-prime-ft-lauderdale.html", "/portfolio.html"),
    ("/blog/ocean-prime-ft-lauderdale-glazing.html", "/portfolio.html"),
    # Cost data / calculator / estimator -> capabilities
    ("/commercial-glass-cost-data.html", "/capabilities.html"),
    ("/cost-calculator.html", "/capabilities.html"),
    ("/tools/storefront-cost-estimator/", "/capabilities.html"),
    ("/tools/storefront-cost-estimator", "/capabilities.html"),
    # Cost FL vs TN -> locations
    ("/commercial-glazing-cost-florida-vs-tennessee/", "/locations.html"),
    ("/commercial-glazing-cost-florida-vs-tennessee", "/locations.html"),
    # Legacy consolidated pages that are truly gone (pass residual equity)
    ("/commercial-glass-replacement.html", "/commercial-glass-replacement-vs-repair/"),
    ("/hvhz-glazing-requirements.html", "/florida-hvhz-glazing-requirements.html"),
    ("/trulite-installer-florida.html", "/commercial-storefront-installer-florida.html"),
    ("/why-acg.html", "/about.html"),
]

added = []
for src, dst in new_pairs:
    if src in existing_sources:
        continue
    existing.append({"source": src, "destination": dst, "permanent": True})
    existing_sources.add(src)
    added.append((src, dst))

cfg["redirects"] = existing

with open(vj_path, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")

print(f"Total redirects now: {len(existing)}")
print(f"Added {len(added)} new redirects:")
for s, d in added:
    print(f"  {s} -> {d}")

# Validate JSON
with open(vj_path) as f:
    json.load(f)
print("vercel.json is valid JSON")
