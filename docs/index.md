# Bedder - simple, flexible intersections

`bedder` is organized into subcommands for easier usage:

```
bedder v0.1.8

Usage: bedder <COMMAND>

Commands:
  full       Full functionality with all options (almost never use this)
  intersect  Intersection mode - hides closest options
  closest    Closest mode - hides overlap requirements
  help       Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
```

### Subcommands

- **`bedder intersect`** - For finding overlaps between intervals. This is the most commonly used mode and hides closest-related options for simplicity.
- **`bedder closest`** - For finding the nearest intervals. This mode hides overlap requirement options.
- **`bedder full`** - Contains all options from both intersect and closest modes. Use this only when you need access to all features simultaneously.

### Common Options (for all subcommands)

All subcommands share common options:

- `-a <QUERY_PATH>` - input file
- `-b <OTHER_PATHS>` - other file
- `-g, --genome <GENOME_FILE>` - genome file for chromosome ordering
- `-c, --columns <COLUMNS>` - columns to output (format: name:type:description:number:value_parser)
- `-o, --output <OUTPUT_PATH>` - output file (default: stdout)
- `-p, --a-piece <A_PIECE>` - the piece of the a intervals to report [default: whole] [possible values: none, piece, whole, inverse, whole-wide]
- `-P, --b-piece <B_PIECE>` - the piece of the b intervals to report [default: whole] [possible values: none, piece, whole, inverse, whole-wide]
- `--python <PYTHON_FILE>` - python file with functions to be used in columns
- `-f, --filter <FILTER>` - optional filter expression (Python boolean expression; 'r' and 'fragment' are the current report fragment) indicates if the fragment should be included in the output

### Intersect-specific Options

- `-m, --a-mode <INTERSECTION_MODE>` - intersection mode for a-file [default: default] [possible values: default, not, piece]
- `-M, --b-mode <B_MODE>` - intersection mode for b-file [default: default] [possible values: default, not, piece]
- `-r, --a-requirements <A_REQUIREMENTS>` - a-requirements for overlap (float < 1, percentage, or integer for bases)
- `-R, --b-requirements <B_REQUIREMENTS>` - b-requirements for overlap (float < 1, percentage, or integer for bases)

### Closest-specific Options

- `-n, --n-closest <N_CLOSEST>` - report the n-closest intervals
- `-d, --max-distance <MAX_DISTANCE>` - maximum distance to search for closest intervals

## Logging

`bedder` has logging for debugging and tracing. The default is to only show warnings. If interested in more granular (verbose) output, set an environment variable:

```
export RUST_LOG=info
```

sometimes this can be helpful if `bedder` isn't behaving how you expect.
