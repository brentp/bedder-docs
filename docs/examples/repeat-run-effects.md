# SNV effects on uninterrupted repeats

Does an HG002 SNV lengthen or shorten the longest pure repeat run? Here, **A**
contains variants and **B** contains repeat intervals, motifs, and reference
sequences. The Python callback substitutes each ALT and reports the change.

## Python callback

This excerpt uses `effect()` from the
[full script](https://github.com/quinlan-lab/bedder-rs/blob/manuscript/manuscript/repeat-interruptions/repeat_run_effect.py).
That helper compares the longest consecutive run of complete motif copies,
allowing all motif rotations and overlapping start positions.

```python title="repeat_run_effect.py"
def bedder_repeat_run(fragment) -> str:
    """Repeat ID|motif|reference pure copies|alternate pure copies|delta; single-SNV effect."""
    variant = fragment.a.vcf()
    if variant is None:
        raise ValueError('requires VCF query records')
    if len(variant.ALT) != 1:
        raise ValueError('requires biallelic input')
    if len(fragment.b) != 1:
        raise ValueError('requires one repeat per record: use --a-piece whole --b-piece whole')
    repeat = fragment.b[0].bed()
    if repeat is None:
        raise ValueError('requires BED repeat records')
    motif, sequence = repeat.other_fields()
    if len(sequence) != repeat.stop - repeat.start:
        raise ValueError('repeat sequence length does not match BED interval')
    before, after, delta = effect(sequence, motif, variant.pos - repeat.start,
                                  variant.REF, variant.ALT[0])
    return f'{repeat.name}|{motif}|{before}|{after}|{delta}'
```

## Run it

From a `bedder-rs` checkout on the `manuscript` branch, using the full script and
bundled inputs:

```bash
example=manuscript/repeat-interruptions
bedder intersect -a "$example/data/variants.vcf" \
  -b "$example/data/repeats.bed" -g "$example/data/genome.tsv" \
  --a-piece whole --b-piece whole \
  --python "$example/repeat_run_effect.py" -c py:repeat_run \
  -o repeat-effects.vcf
```

Each output record describes one variant–repeat pair. For example,
**chr19:16259432 T>C** changes the longest uninterrupted AC run from **13 to 26
copies**, without inserting bases. The frozen example validates 561 pairs from
551 HG002 SNVs.

This is one SNV applied to the reference sequence, bounded by the repeat
interval—not a reconstructed HG002 haplotype or a pathogenicity prediction.

[Full code, frozen inputs, and independent validation](https://github.com/quinlan-lab/bedder-rs/tree/manuscript/manuscript/repeat-interruptions)
