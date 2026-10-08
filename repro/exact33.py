"""Necessary hitting condition for 33-change extensions of the 536 certificate.

The color of 537 must be 5.  Its 32 complementary color-5 pairs force at
least one change per pair.  A 33rd change can affect at most one entry outside
those 64 endpoints.  For every forced endpoint recoloring, each original
monochromatic triple with only that endpoint mutable must be hit by that same
extra entry.  This program checks whether any extra entry can serve all pairs.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path


def main() -> None:
    data = json.loads(Path(__file__).with_name("fredricksen_sweet_536.json").read_text())
    assert data["n"] == 536 and data["colors"] == 6
    color = [-1] * 538
    for c, group in enumerate(data["listed_sets"]):
        for x in group:
            assert color[x] == -1
            color[x] = c
            if x <= 268 and x != 179:
                assert color[537 - x] == -1
                color[537 - x] = c
    assert all(0 <= color[x] < 6 for x in range(1, 537))
    color[537] = 4

    pair_counts = [sum(color[x] == color[537-x] == c for x in range(1,269))
                   for c in range(6)]
    assert pair_counts == [64, 43, 55, 38, 32, 35]
    pairs = [(x, 537-x) for x in range(1,269)
             if color[x] == color[537-x] == 4]
    endpoints = {v for pair in pairs for v in pair}
    outside = set(range(1, 537)) - endpoints

    incident = {v: [] for v in endpoints}
    for x in range(1,537):
        for y in range(x,537-x):
            z = x+y
            for v in {x,y,z} & endpoints:
                incident[v].append((x,y,z))

    # Possible locations of the one extra change for each forced pair.  The
    # set for a possible endpoint/color is the intersection of all its fixed
    # blocker-entry sets.  A global location must occur in every pair set.
    pair_options = []
    blocker_witnesses = {}
    for a,b in pairs:
        options = set()
        for v in (a,b):
            for c in range(6):
                if c == 4:
                    continue
                blocker_sets = []
                for triple in incident[v]:
                    others = set(triple) - {v}
                    if others <= outside and all(color[u] == c for u in others):
                        blocker_sets.append(others)
                blocker_witnesses[(v, c+1)] = blocker_sets
                # A fixed-safe recolor would have defeated the earlier exact
                # 32 shell test.  With no blockers, any extra location works.
                if blocker_sets:
                    options.update(set.intersection(*blocker_sets))
                else:
                    options.update(outside)
        pair_options.append(((a,b), options))

    global_options = set.intersection(*(options for _,options in pair_options))
    zero_pairs = [pair for pair, options in pair_options if not options]

    # Compact, independently checkable obstruction for the first zero pair:
    # for each endpoint and alternative color, at most three fixed-entry
    # blocker sets have empty intersection (sets have at most two elements).
    first_pair_witness = {}
    if zero_pairs:
        for v in zero_pairs[0]:
            for c in (1,2,3,4,6):
                blockers = blocker_witnesses[(v,c)]
                short = next((choice for size in (2,3)
                              for choice in combinations(blockers, size)
                              if not set.intersection(*choice)), None)
                assert short is not None
                first_pair_witness[f"{v}->{c}"] = [sorted(s) for s in short]
    print(json.dumps({
        "candidate_color_for_537": 5,
        "pair_counts_for_537_colors_1_to_6": pair_counts,
        "forced_pairs": len(pairs),
        "outside_positions": len(outside),
        "pairs_with_no_single_extra_recolor_option": zero_pairs,
        "first_zero_pair_fixed_blocker_sets": first_pair_witness,
        "global_extra_recolor_options": sorted(global_options),
        "radius_33_shell_excluded": not global_options,
    }, indent=2))


if __name__ == "__main__":
    main()
