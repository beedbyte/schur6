"""Independently check the published six-color Schur partition of [1, 536]."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


CERTIFICATE = Path(__file__).with_name("fredricksen_sweet_536.json")


def main() -> None:
    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    assert data["n"] == 536 and data["colors"] == 6
    assert data["symmetry_sum"] == 537
    sets = data["listed_sets"]
    assert len(sets) == 6

    listed = [x for group in sets for x in group]
    assert sorted(listed) == list(range(1, 269)) + [358], (
        "The paper must list each integer 1..268 once, plus exceptional 358"
    )
    assert 179 in sets[3] and 358 in sets[0]

    color = [-1] * 537
    for label, group in enumerate(sets):
        for x in group:
            positions = [x]
            if x <= 268 and x != 179:
                positions.append(537 - x)
            for value in positions:
                assert color[value] == -1, ("duplicate assignment", value)
                color[value] = label

    assert all(0 <= color[x] < 6 for x in range(1, 537)), "incomplete partition"
    assert color[179] == 3 and color[358] == 0

    tested = 0
    for x in range(1, 537):
        for y in range(x, 537 - x):
            z = x + y
            tested += 1
            assert not (color[x] == color[y] == color[z]), (
                "monochromatic Schur triple", x, y, z, color[x] + 1
            )
    assert tested == 71_824

    # For a fixed color of 537, each same-color pair x + y = 537
    # must be broken by recoloring at least one of its endpoints.
    # The pairs are disjoint because x ranges only over 1..268.
    blockers = []
    for label in range(6):
        pairs = [
            [x, 537 - x]
            for x in range(1, 269)
            if color[x] == color[537 - x] == label
        ]
        blockers.append({"color": label + 1, "pairs": len(pairs), "first_three": pairs[:3]})

    print(json.dumps({
        "result": "PASS",
        "source_json_sha256": hashlib.sha256(raw).hexdigest(),
        "n": 536,
        "colors": 6,
        "covered": 536,
        "sum_free_triples_checked": tested,
        "color_class_sizes": [color[1:].count(label) for label in range(6)],
        "537_fixed_extension_blockers": blockers,
        "complementary_pair_lower_bound_on_prior_recolors": min(
            item["pairs"] for item in blockers
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
