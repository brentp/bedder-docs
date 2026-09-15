# Highest-identity segmental duplication

Which segmental duplication overlapping an HG002 variant has the highest UCSC
`fracMatch`? Here, **A** contains variants and **B** contains SD alignments.
Python selects the matching record and returns its partner coordinates, with
an option to consider only interchromosomal duplications.

## Python functions

```python title="segdup_best_match.py"
from decimal import Decimal


def best_match(fragment, interchromosomal=False):
    candidates = []
    for overlap in fragment.b:
        b = overlap.bed()
        strand, identity, partner, start, end, uid = b.other_fields()
        identity = identity.split('=', 1)[1]
        score = Decimal(identity)
        if not score.is_finite() or not 0 <= score <= 1:
            raise ValueError('fracMatch must be a finite fraction between 0 and 1')
        if interchromosomal and b.chrom == partner:
            continue
        value = f'{identity}|{b.chrom}:{b.start}-{b.stop}|{partner}:{start}-{end}|{strand}|{b.name}'
        candidates.append((-score, b.name, value))  # Highest identity; ties by row ID.
    return min(candidates)[2] if candidates else '.'


def bedder_sd_best(fragment) -> str:
    """Maximum-fracMatch SD: identity|local interval|partner interval|strand|row ID; BED coordinates."""
    return best_match(fragment)


def bedder_sd_best_interchrom(fragment) -> str:
    """Maximum-fracMatch interchromosomal SD: identity|local interval|partner interval|strand|row ID."""
    return best_match(fragment, interchromosomal=True)
```

The prepared BED6 adds `fracMatch=<value>`, partner chromosome/start/end, and
UCSC UID. The text label preserves identity precision through the current BED
extra-field formatter. `other_fields()` includes the strand and these extras.

## Prepare the SD track

From a `bedder-rs` checkout on the `manuscript` branch, with your existing HG002
VCF and `hg38.fai`, download the table and check its pinned checksum:

```bash
example=manuscript/segdup-identity
curl -fL --retry 3 https://hgdownload.soe.ucsc.edu/goldenPath/hg38/database/genomicSuperDups.txt.gz \
  -o genomicSuperDups.txt.gz
sha256sum -c "$example/genomicSuperDups.sha256"
```

One shell pipeline extracts the required columns, keeps primary chromosomes on
both sides, and sorts the intervals. It uses Bash, gzip, awk, and BEDtools:

```bash
set -euo pipefail
gzip -dc genomicSuperDups.txt.gz |
  awk 'BEGIN {OFS="\t"; primary="^chr([1-9]|1[0-9]|2[0-2]|X|Y)$"}
       $2 ~ primary && $8 ~ primary {
         print $2,$3,$4,"sd_"$12"_"NR,0,$7,"fracMatch="$27,$8,$9,$10,$12
       }' |
  bedtools sort -g hg38.fai > segdups.bed
```

## Annotate the existing VCF

```bash
example=manuscript/segdup-identity
vcf=HG002_GRCh38_MosaicSNVv1.0_GermlineV4.2.1.vcf.gz
bedder intersect -a "$vcf" -b segdups.bed -g hg38.fai \
  --a-piece whole-wide --b-piece whole-wide -r 0 -R 0 \
  --python "$example/segdup_best_match.py" \
  -c py:sd_best -c py:sd_best_interchrom -o segdup-identity.vcf
```

Set `vcf` to any existing compatible VCF; no variant subsetting or reference
sequence is needed. The command annotates every input record.
`whole-wide` supplies all overlaps together, producing one record per query;
both zero overlap requirements retain no-hit queries with `.` annotations.
Ties resolve by row ID.

For **chr19:9722714 G>A**, the best SD has identity **0.911287** and a chr19
partner; restricting to interchromosomal SDs selects a chr5 partner at
**0.910397**. The separately available frozen chr19 example validates 6,205
filtered variants; it can be run offline without any preparation.

Identity describes the entire SD alignment, not just the overlap with the
variant. Returned intervals use zero-based, half-open coordinates. BEDtools can
compute a maximum value; this example also selects the associated record and
filters on its partner chromosome.

[Full code, frozen inputs, optional counts, and independent validation](https://github.com/quinlan-lab/bedder-rs/tree/manuscript/manuscript/segdup-identity)
