"""Independent audit of a short obstruction to 32 or 33 recolorings.

The blocker sets below are hard-coded, not imported from exact32.py or
exact33.py.  Each row gives two disjoint sets of *other* entries that make a
monochromatic x+y=z triple after changing the named endpoint to that color.
"""

import hashlib
import json
from pathlib import Path


# (endpoint, new color): two disjoint sets of other triple entries.
WITNESSES = {
    (9, 1): ((1, 8), (5, 14)),
    (9, 2): ((25, 34), (63, 72)),
    (9, 3): ((60, 69), (241, 250)),
    (9, 4): ((4, 13), (64, 73)),
    (9, 6): ((18,), (148, 157)),
    (528, 1): ((1, 529), (5, 523)),
    (528, 2): ((25, 503), (63, 465)),
    (528, 3): ((60, 468), (241, 287)),
    (528, 4): ((4, 524), (64, 464)),
    (528, 6): ((148, 380), (199, 329)),
}


def main() -> None:
    raw = Path(__file__).with_name("fredricksen_sweet_536.json").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == "423b50378ca8c09b5909c244216a857b30d577ff6bef6e98635329ff432e0912"
    groups = json.loads(raw)["listed_sets"]
    assert len(groups) == 6
    colors = {}
    for number in range(1, 537):
        matches = []
        for c, group in enumerate(groups, 1):
            if number in group or (
                number >= 269 and number != 358 and 537 - number in group
                and 537 - number != 179
            ):
                matches.append(c)
        assert len(matches) == 1, (number, matches)
        colors[number] = matches[0]

    # Recheck the source certificate without using the other checkers.
    triples = 0
    for result in range(2, 537):
        for first in range(1, result // 2 + 1):
            second = result - first
            assert not (colors[first] == colors[second] == colors[result])
            triples += 1
    assert triples == 71824

    pair_counts = [sum(colors[x] == colors[537-x] == c for x in range(1,269))
                   for c in range(1,7)]
    assert pair_counts == [64,43,55,38,32,35]
    pairs = [(x,537-x) for x in range(1,269)
             if colors[x] == colors[537-x] == 5]
    endpoints = {x for pair in pairs for x in pair}
    assert len(pairs) == 32 and (9,528) in pairs
    assert set(WITNESSES) == {(v,c) for v in (9,528)
                             for c in (1,2,3,4,6)}
    checked = 0
    for (v,c), (a,b) in WITNESSES.items():
        assert set(a).isdisjoint(b), (v,c,a,b)
        for others in (a,b):
            assert not (set(others) & endpoints), (v,c,others)
            assert all(colors[x] == c for x in others), (v,c,others)
            terms = sorted((*others, v, v) if len(others) == 1
                           else (*others, v))
            assert len(terms) == 3 and terms[0] + terms[1] == terms[2], (
                v,c,others,terms
            )
            checked += 1

    print(json.dumps({
        "result": "PASS",
        "source_json_sha256": digest,
        "source_triples_checked": triples,
        "pair_counts": pair_counts,
        "hard_coded_blocker_triples_checked": checked,
        "short_obstruction_pair": [9,528],
        "proven_lower_bound_on_prior_recolors": 34,
    }, indent=2))


if __name__ == "__main__":
    main()
