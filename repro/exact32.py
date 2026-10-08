"""Test the radius-32 shell around the published 536-coloring for 537.

Exactly 32 changes require assigning 537 color 5 and changing exactly one
endpoint of each of its 32 monochromatic complementary pairs.  All other
entries are fixed.  A possible new color of an endpoint is ruled out if it
would create a monochromatic triple with two fixed entries in [1, 536].
"""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    data = json.loads(Path(__file__).with_name("fredricksen_sweet_536.json").read_text())
    color = [-1] * 538
    for label, group in enumerate(data["listed_sets"]):
        for x in group:
            color[x] = label
            if x <= 268 and x != 179:
                color[537 - x] = label
    assert all(0 <= color[x] < 6 for x in range(1, 537))
    color[537] = 4

    pairs = [(x, 537 - x) for x in range(1, 269)
             if color[x] == color[537 - x] == 4]
    assert len(pairs) == 32
    mutable = {v for pair in pairs for v in pair}

    # A triple may contain x twice.  For x+x=z, changing x alone can create
    # a violation if z is fixed; that is handled by the all-fixed-others test.
    triples = [(x, y, x + y) for x in range(1, 537)
               for y in range(x, 537 - x)]
    incident = {v: [] for v in mutable}
    for triple in triples:
        for v in set(triple) & mutable:
            incident[v].append(triple)

    domains = {}
    witnesses = {}
    for v in sorted(mutable):
        allowed = []
        for new_color in range(6):
            if new_color == 4:
                continue
            bad = next((triple for triple in incident[v]
                        if all(u == v or (u not in mutable and color[u] == new_color)
                               for u in triple)), None)
            if bad is None:
                allowed.append(new_color + 1)
            else:
                witnesses[(v, new_color + 1)] = bad
        domains[v] = allowed

    impossible = []
    for x, y in pairs:
        if not domains[x] and not domains[y]:
            impossible.append({
                "pair": [x, y],
                "x_color_blockers": {str(c): witnesses[(x, c)] for c in range(1, 7) if c != 5},
                "y_color_blockers": {str(c): witnesses[(y, c)] for c in range(1, 7) if c != 5},
            })

    print(json.dumps({
        "candidate_color_for_537": 5,
        "required_pairs": len(pairs),
        "mutable_endpoints": len(mutable),
        "pairs_with_no_fixed_safe_recolor_of_either_endpoint": len(impossible),
        "first_impossible_pair": impossible[0] if impossible else None,
        "endpoint_domain_sizes": {str(v): len(domain) for v, domain in domains.items()},
        "radius_32_shell_excluded": bool(impossible),
    }, indent=2))


if __name__ == "__main__":
    main()
