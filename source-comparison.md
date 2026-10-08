# Printed-source comparison

On 8 October 2026, the six `listed_sets` arrays in `repro/fredricksen_sweet_536.json` were compared entry by entry, in their printed order, against the construction on PDF page 6 of Harold Fredricksen and Melvin M. Sweet, “Symmetric Sum-Free Partitions and Lower Bounds for Schur Numbers,” *The Electronic Journal of Combinatorics* 7 (2000), R32:

https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/

The source was read from the publisher's PDF text extraction. For each printed `Set 1` through `Set 6`, all integers between that label and the next set label were parsed and compared in order with the corresponding JSON array. This comparison is separate from `verify.py`, which tests the coloring encoded in the JSON.

| Set | Printed count | JSON count | Ordered entries |
| --- | ---: | ---: | --- |
| 1 | 65 | 65 | Exact match |
| 2 | 43 | 43 | Exact match |
| 3 | 55 | 55 | Exact match |
| 4 | 39 | 39 | Exact match |
| 5 | 32 | 32 | Exact match |
| 6 | 35 | 35 | Exact match |

There are 269 printed entries: every integer from 1 through 268 and the exceptional 358. The paper's definition of symmetry permits the pair 179 and 358 to be assigned different colors. This source comparison supports the transcription claim; it does not replace an independent mathematical review of the local 34-change argument.
