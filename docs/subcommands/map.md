# Bedder Map

`bedder map` aggregates values from overlapping `-b` intervals for each `-a` interval.

## Quick Mental Model

For each `A` interval:

1. Find overlapping `B` intervals.
2. Extract one numeric value per overlap using `-c/--column` (default: BED column 5).
3. Aggregate those values with `-O/--operation` (default: `sum`).
4. Append aggregate result columns to the output row.

`-a` currently must be BED. `-b` can be BED/VCF/BCF.

## Example Files

These examples use files in `tests/examples/`.

### `map_a.bed`

```text
chr1    100     200     geneA   10
chr1    300     400     geneB   20
```

### `map_a_nohit.bed`

```text
chr1    100     200     geneA   10
chr1    500     600     geneC   30
```

### `map_b.bed`

```text
chr1    120     180     geneA   5
chr1    130     170     geneB   7
chr1    150     190     geneA   3
chr1    350     380     geneB   4
```

### `map_b.vcf`

```text
#CHROM  POS  ID  REF  ALT  QUAL  FILTER  INFO
chr1    121  .   A    T    .     PASS    DP=5;AF=0.1
chr1    131  .   A    G,C  .     PASS    DP=7;AF=0.2,0.8
chr1    151  .   C    T    .     PASS    DP=3;AF=0.3
chr1    351  .   G    A    .     PASS    DP=4;AF=0.4
```

### `map_b_missing_dp.vcf`

```text
#CHROM  POS  ID  REF  ALT  QUAL  FILTER  INFO
chr1    121  .   A    T    .     PASS    DP=5;AF=0.1
chr1    131  .   A    G,C  .     PASS    DP=7;AF=0.2,0.8
chr1    151  .   C    T    .     PASS    DP=3;AF=0.3
chr1    161  .   T    C    .     PASS    AF=0.5
chr1    351  .   G    A    .     PASS    DP=4;AF=0.4
```

## How `-c` And `-O` Pair

`bedder map` pairs selectors (`-c`) and operations (`-O`) like `bedtools map`:

- Same lengths: pair positionally.
- One selector and many operations: reuse the selector for every operation.
- Many selectors and one operation: reuse the operation for every selector.
- Otherwise: error.

## Core Examples

Default behavior maps BED score (`-c 5`) with `sum`:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai
chr1    100     200     geneA   10      15
chr1    300     400     geneB   20      4
```

`geneA` sums `5+7+3=15`; `geneB` sums `4`.

Use multiple operations:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai -c 5 -O sum,mean,count
chr1    100     200     geneA   10      15      5       3
chr1    300     400     geneB   20      4       4       1
```

No overlap behavior (`sum` becomes `.`, `count` becomes `0`):

```bash
$ bedder map -a tests/examples/map_a_nohit.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai -O sum,count
chr1    100     200     geneA   10      15      3
chr1    500     600     geneC   30      .       0
```

## Name-Aware Mapping (`-n`, `-G`)

Restrict to overlaps where B name matches A name:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai -n
chr1    100     200     geneA   10      8
chr1    300     400     geneB   20      4
```

Group by B name (`-G`) to emit one output row per B-name group:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai -G -O sum,count
chr1    100     200     geneA   10      geneA   8       2
chr1    100     200     geneA   10      geneB   7       1
chr1    300     400     geneB   20      geneB   4       1
```

Without `-G`, output is one row per `A`.  
With `-G`, output is one row per `(A, B-name-group)` and includes an extra B-name column before aggregates.

## Python Customization

Python functions must be named `bedder_<name>`, then referenced as `py:<name>`.

### Python Operation (`-O py:<name>`)

Use this when you want custom aggregation over the extracted numeric list.
The function receives `values` (`list[float]`).

```python
def bedder_sum_plus_one(values) -> float:
    return float(sum(values) + 1.0)
```

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai --python tests/examples/map_ops.py -O py:sum_plus_one
chr1    100     200     geneA   10      16
chr1    300     400     geneB   20      5
```

### Python As A Column (`-c py:<name>`)

You can compute mapped values with Python column extractors.

- Extractor functions receive one overlapping interval (`iv`) at a time.
- Extractors must be annotated `-> int` or `-> float`.
- Returning `None` skips that overlap for value-based operations.

Example functions from `tests/examples/map_ops.py`:

```python
def bedder_bed_score(iv) -> float:
    b = iv.bed()
    if b is None or b.score is None:
        return None
    return float(b.score)

def bedder_vcf_dp(iv) -> float:
    v = iv.vcf()
    if v is None:
        return None
    dp = v.info("DP")
    return float(dp) if dp is not None else None
```

Extractor on BED `-b`:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.bed -g tests/examples/fake.fai --python tests/examples/map_ops.py -c py:bed_score -O sum,mean,count
chr1    100     200     geneA   10      15      5       3
chr1    300     400     geneB   20      4       4       1
```

Extractor on VCF `-b`:

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b.vcf -g tests/examples/fake.fai --python tests/examples/map_ops.py -c py:vcf_dp -O sum,mean,count
chr1    100     200     geneA   10      15      5       3
chr1    300     400     geneB   20      4       4       1
```

Missing extracted values example (`DP` missing for one overlap):

```bash
$ bedder map -a tests/examples/map_a.bed -b tests/examples/map_b_missing_dp.vcf -g tests/examples/fake.fai --python tests/examples/map_ops.py -c py:vcf_dp -O sum,mean,count
chr1    100     200     geneA   10      15      5       4
chr1    300     400     geneB   20      4       4       1
```

For `geneA`, one overlap has no `DP`, so `sum/mean` use three numeric values, while `count` still reports four overlaps.

## Common Gotchas

- VCF/BCF with value-based operations cannot use numeric BED selector syntax like `-c 5`; use `-c py:<name>`.
- With plain (unindexed) VCF, HTSlib may print missing-index warnings to stderr; stdout results are still valid.
- Any `py:` selector/operation requires `--python <file>`.
