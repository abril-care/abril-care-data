#!/usr/bin/env python3
"""Split providers JSON into per-state files."""

import json
from pathlib import Path

# Input file
input_file = Path("/Users/bhali/Documents/abril/hackathons/digitalocean/data/providers_all.json")
out_dir = Path("/Users/bhali/Documents/abril-care-data/data/providers")

out_dir.mkdir(parents=True, exist_ok=True)

# Load data
with open(input_file) as f:
    data = json.load(f)

providers = data["providers"]
stats = data["stats"]

print(f"Total providers: {stats['total_providers']}")
print(f"By state: {stats['by_state']}")

# Group by state
by_state = {}
for p in providers:
    state = p.get("state", "unknown")
    if state not in by_state:
        by_state[state] = []
    by_state[state].append(p)

# Write each state file
for state, state_providers in by_state.items():
    out_file = out_dir / f"{state.lower()}_providers.json"
    with open(out_file, "w") as f:
        json.dump({
            "state": state,
            "count": len(state_providers),
            "fetch_date": stats["fetch_date"],
            "providers": state_providers
        }, f)
    print(f"  {state}: {len(state_providers):,} providers -> {out_file.name}")

# Write combined stats
stats_file = out_dir / "README.md"
with open(stats_file, "w") as f:
    f.write("# Provider Data\n\n")
    f.write(f"**Total providers:** {stats['total_providers']:,}\n\n")
    f.write(f"**Fetch date:** {stats['fetch_date']}\n\n")
    f.write("## By State\n\n")
    f.write("| State | Providers |\n")
    f.write("|-------|----------:|\n")
    for state, count in sorted(stats['by_state'].items(), key=lambda x: -x[1]):
        f.write(f"| {state} | {count:,} |\n")
    f.write(f"\n**With coordinates:** {stats['with_coordinates']:,}\n")
    f.write(f"**With quality rating:** {stats['with_quality_rating']:,}\n")

print(f"\nStats written to {stats_file}")
