#!/usr/bin/env bash
# Status line for the lab: model, context used, session cost.
python3 -c '
import json, sys
d = json.load(sys.stdin)
cw = d.get("context_window", {})
model = d.get("model", {}).get("display_name", "?")
used = cw.get("used_percentage", "?")
size = cw.get("context_window_size", 0) // 1000
cost = d.get("cost", {}).get("total_cost_usd", 0)
print(f"{model} | context {used}% of {size}k | ${cost:.2f}")
'
