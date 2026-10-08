# Reproducibility record

The original certificate is in `repro/fredricksen_sweet_536.json`. Its SHA-256
is `423b50378ca8c09b5909c244216a857b30d577ff6bef6e98635329ff432e0912`.
The six printed source lists were compared entry by entry with the
Fredricksen–Sweet paper, as recorded in `source-comparison.md`. That source
comparison is distinct from the Python checks below, which validate the
transcription as a mathematical coloring.

Run these four commands from the repository root:

```sh
python repro/verify.py
python repro/exact32.py
python repro/exact33.py
python repro/audit33.py
```

Expected fields:

| Command | Expected output |
| --- | --- |
| `verify.py` | `result: PASS`; `covered: 536`; `sum_free_triples_checked: 71824`; pair counts `64, 43, 55, 38, 32, 35` |
| `exact32.py` | `radius_32_shell_excluded: true` |
| `exact33.py` | `radius_33_shell_excluded: true` |
| `audit33.py` | `result: PASS`; `hard_coded_blocker_triples_checked: 20`; `proven_lower_bound_on_prior_recolors: 34` |

The scripts use the Python standard library and have no network or random
seed. `audit33.py` hard-codes its 20 witnesses rather than importing them from
the search scripts. It checks their arithmetic, colors, location outside the
32 forced complementary pairs, and pairwise disjointness in each row. The
captured machine output is in `checks.json`.

The supplied PDF was generated from `paper.en.md` by `build_pdf.py` with
ReportLab and Arial fonts on Windows. These packages and fonts are needed
only to rebuild the PDF, not to run the mathematical checks. The `.tex` file
is an alternate manuscript source; it was not used to generate the PDF.

