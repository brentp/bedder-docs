# Bedder - simple, flexible intersections

## Commands

For now, there is a single command: `bedder` with the following help:

```
Usage: bedder [OPTIONS] -a <QUERY_PATH> -b <OTHER_PATHS> --genome <GENOME_FILE>

Options:
  -a <QUERY_PATH>
          input file
  -b <OTHER_PATHS>
          other file
  -g, --genome <GENOME_FILE>
          genome file for chromosome ordering
  -c, --columns <COLUMNS>
          columns to output (format: name:type:description:number:value_parser)
  -o, --output <OUTPUT_PATH>
          output file (default: stdout) [default: -]
  -m, --a-mode <INTERSECTION_MODE>
          intersection mode for a-file. this determines how the overlap requirements are accumulated. [default: default] [possible values: default, not, piece]
  -M, --b-mode <B_MODE>
          intersection mode for b-file. this determines how the overlap requirements are accumulated. [default: default] [possible values: default, not, piece]
  -p, --a-piece <A_PIECE>
          the piece of the a intervals to report [default: whole] [possible values: none, piece, whole, inverse]
  -P, --b-piece <B_PIECE>
          the piece of the b intervals to report [default: whole] [possible values: none, piece, whole, inverse]
  -r, --a-requirements <A_REQUIREMENTS>
          a-requirements for overlap. A float value < 1 or a number ending with % will be the fraction (or %) of the interval. An integer will be the number of bases. Default is 1 unless n-closest is set.
  -R, --b-requirements <B_REQUIREMENTS>
          b-requirements for overlap. A float value < 1 or a number ending with % will be the fraction (or %) of the interval. An integer will be the number of bases. Default is 1 unless n-closest is set.
      --python <PYTHON_FILE>
          python file with functions to be used in columns
  -n, --n-closest <N_CLOSEST>
          report the n-closest intervals.
          By default, all overlapping intervals are reported.
          If n-closest is set, then the n closest intervals are reported, regardless of overlap.
          When used, the default overlap requirement is set to 0, so that non-overlapping intervals can be reported.
          This is mutually exclusive with --a-requirements and --b-requirements.
  -d, --max-distance <MAX_DISTANCE>
          maximum distance to search for closest intervals.
          By default, there is no distance limit.
          When used, the default overlap requirement is set to 0, so that non-overlapping intervals can be reported.
          This can be overridden by setting a-requirements and b-requirements.
```
