# Bedder Closest

The `bedder closest` command finds the nearest intervals between two BED files. Unlike `intersect`, which requires overlaps, `closest` can find the nearest intervals even when they don't overlap.

## Basic Usage

### Simple Closest

Find the closest intervals in `target.bed` for each interval in `query.bed`:

**query.bed:**

```
chr1 10 20
chr1 50 60
```

**target.bed:**

```
chr1 30 40
chr1 70 80
```

```bash
$ bedder closest -a query.bed -b target.bed -g genome.fai -n 1 -c distance
chr1 10 20 chr1 30 40 10
chr1 50 60 chr1 30 40 10
```

Each line shows:

- The query interval (first 3 columns)
- The closest target interval (next 3 columns)
- The distance in bases (last column)

---

## Distance

The `distance` column reports the number of bases between intervals:

- **0** = overlapping intervals
- **Positive number** = non-overlapping with that many bases between them
- **-1** = no intervals found within the specified constraints

### Overlapping Intervals

When intervals overlap, the distance is 0:

**single.bed:**

```
chr1 25 35
```

```bash
$ bedder closest -a single.bed -b target.bed -g genome.fai -c distance
chr1 25 35 chr1 30 40 0
```

---

## Finding Multiple Closest Intervals

Use `-n` or `--n-closest` to find multiple nearest intervals:

### n-closest = 1 (default behavior with -n flag)

```bash
$ bedder closest -a multi.bed -b target.bed -g genome.fai -n 1 -c distance
chr1 5 10 chr1 30 40 20
chr1 25 35 chr1 30 40 0
chr1 45 50 chr1 30 40 5
```

### n-closest = 2

Find the two closest intervals for each query:

```bash
$ bedder closest -a query.bed -b target.bed -g genome.fai -n 2 -c distance
chr1 10 20 chr1 30 40 chr1 70 80 10
chr1 50 60 chr1 30 40 chr1 70 80 10
```

Notice that each query interval now has two target intervals (6 columns for targets instead of 3).

---

## Maximum Distance

Use `-d` or `--max-distance` to limit how far to search for closest intervals:

### max-distance = 15

Only report intervals within 15 bases:

```bash
$ bedder closest -a query.bed -b target.bed -g genome.fai -d 15 -c distance
chr1 10 20 chr1 30 40 10
chr1 50 60 chr1 30 40 chr1 70 80 10
```

### max-distance = 5

With a stricter limit, intervals beyond 5 bases are not reported (shown as `-1`):

```bash
$ bedder closest -a query.bed -b target.bed -g genome.fai -d 5 -c distance
chr1 10 20 -1
chr1 50 60 -1
```

The `-1` indicates that no intervals were found within the specified maximum distance.

---

## Default Behavior

Without `-n` or `-d`, `bedder closest` reports **all overlapping intervals** (similar to `bedder intersect`):

**a.bed:**

```
chr1 10 20
chr1 60 75
```

**b.bed:**

```
chr1 15 25
chr1 55 70
```

```bash
$ bedder closest -a a.bed -b b.bed -g genome.fai
chr1 10 20 chr1 15 25
chr1 60 75 chr1 55 70
```

---

## Common Options

All standard `bedder` options work with `closest`:

- `-a <QUERY_PATH>` - query file (required)
- `-b <OTHER_PATHS>` - target file (required)
- `-g, --genome <GENOME_FILE>` - genome file for chromosome ordering (required)
- `-c, --columns <COLUMNS>` - additional columns to output (e.g., `distance`)
- `-o, --output <OUTPUT_PATH>` - output file (default: stdout)
- `-n, --n-closest <N_CLOSEST>` - report the n-closest intervals
- `-d, --max-distance <MAX_DISTANCE>` - maximum distance to search
- `--python <PYTHON_FILE>` - Python file with custom functions
- `-f, --filter <FILTER>` - filter expression

---

## Tips

1. **Use `-c distance`** to see the actual distances between intervals
2. **Use `-n 1`** to find only the single closest interval for each query
3. **Use `-d`** to limit searches and improve performance for large files
4. **Combine `-n` and `-d`** to find the n-closest intervals within a maximum distance
5. When neither `-n` nor `-d` is specified, `closest` behaves like `intersect` and only reports overlapping intervals
