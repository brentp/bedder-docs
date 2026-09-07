# Python callbacks

Bedder embeds Python to compute custom columns and filters while the CLI processes
intervals. Pass a callback file with `--python` and select a function with
`-c 'py:name'`:

[https://quinlan-lab.github.io/bedder-rs/](https://quinlan-lab.github.io/bedder-rs/)

To use `bedder` as a Rust library, run Python inside a Rust application, or expose
your project as a Python module, see [Embedding](embedding.md).

```python
def bedder_n_overlapping(fragment) -> int:
    """Number of reported B intervals."""
    return len(fragment.b)
```

```bash
bedder intersect \
  -a a.bed -b b.bed -g reference.fa.fai \
  --python callbacks.py -c 'py:n_overlapping'
```

Callback names must start with `bedder_`, but the command-line selector omits that
prefix. Every discovered callback must have a concrete return annotation of
`int`, `float`, `str`, or `bool` and must return exactly that type. Do not use
postponed annotations (`from __future__ import annotations`) or prefix helper
functions with `bedder_`.

Intersection callbacks receive a report fragment. `fragment.a` is the query
position, `fragment.b` is the list of reported matching positions, and
`fragment.id` is the fragment identifier. Positions expose `chrom`, `start`, and
`stop`; use `.bed()` for BED-specific fields or `.vcf()` for VCF/BCF-specific
fields.

The callback file is loaded by Bedder's embedded interpreter. It is not a normal
standalone program, and it should not import `bedder` at module load time.

See [Use Bedder from an agent](agent-skill.md#write-an-intersection-python-callback)
for the complete callback object model, VCF examples, map callback contracts,
validation workflow, and common failure modes.

The generated Rust/Python API documentation is also available at
[quinlan-lab.github.io/bedder-rs](https://quinlan-lab.github.io/bedder-rs/).
