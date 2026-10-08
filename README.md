# A local Schur S(6) extension obstruction

Fredricksen and Sweet published a sum-free six-color partition of the integers
1 through 536, proving the lower bound **S(6) ≥ 536**. This repository checks
their certificate and records a separate, local observation about extending
that **specific labeled coloring**.

Let `c` be the six-coloring transcribed from their paper. If a sum-free
six-coloring `d` of 1 through 537 exists, then `d` must assign a different
color from `c` at **at least 34 positions among 1 through 536**. The labels of
the six colors are held fixed; the distance is not minimized over color
permutations. This does **not** say whether such a `d` exists, give an exact
minimum distance, determine S(6), or improve the published global bound.

## Read the note

- [Research page in English](https://beedbyte.tech/research/schur-6/v/5),
  [German](https://beedbyte.tech/de/research/schur-6/v/5), and
  [Simplified Chinese](https://beedbyte.tech/zh/research/schur-6/v/5), with
  both reproduction ZIPs and the earlier website versions
- [English manuscript](paper.en.md) and [PDF reading copy](schur-radius33-note.pdf)
- [German summary](abstract.de.md) and [Simplified Chinese summary](abstract.zh.md)
- [LaTeX source](schur-radius33-note.tex) and [PDF build script](build_pdf.py)

The German and Chinese files are summaries. The full proof and its 20-triple
table are in the English manuscript. The `radius33` file names refer to the
exclusion of all extensions at distance **at most 33**.

## Reproduce the finite checks

From the repository root, with Python 3 and no nonstandard packages for the
mathematical checks:

```sh
python repro/verify.py
python repro/exact32.py
python repro/exact33.py
python repro/audit33.py
```

The scripts check the 536-entry certificate, all 71,824 Schur triples with
`1 ≤ x ≤ y` and `x+y ≤ 536`, the complementary-pair counts for 537, and the
20 explicit blocker triples used in the local proof. Expected results and
file hashes are in [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and
[MANIFEST.sha256](MANIFEST.sha256). The independently documented comparison
between the JSON lists and the original printed lists is in
[source-comparison.md](source-comparison.md).

## Source and credit

The 536-color certificate and the bound S(6) ≥ 536 are due to Harold
Fredricksen and Melvin M. Sweet, [“Symmetric Sum-Free Partitions and Lower
Bounds for Schur Numbers,” *The Electronic Journal of Combinatorics* 7
(2000), R32](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/).
Our JSON file is a transcription of their six published lists, expanded by the
scripts using the symmetry and exception stated in that paper. The local
34-change argument, accompanying scripts, and note are attributed to
**Beedbyte · School Scotty**. Correspondence: beedbyte@3g-projects.de.

AI agents transcribed the published partition, wrote and ran the finite
checkers, and performed internal checks of the local argument. A separate
source comparison checked all 269 printed certificate entries against the
publisher's PDF. The explicit witnesses and deterministic checks are supplied
for independent review. This work has not undergone external peer review. No
DOI has been assigned to this repository package.
