# Embedding Bedder

Use `bedder` as a Rust library to intersect genomic records directly. You can also
pass the results to an embedded Python interpreter or expose them from your own
Python extension.

## Rust API

Add bedder to your project's `Cargo.toml`:

```toml
[dependencies]
bedder = { git = "https://github.com/quinlan-lab/bedder-rs.git" }
```

For local development, use `bedder = { path = "../bedder-rs" }` instead. Pin a
tested Git revision with `rev` for reproducible builds.

This example uses BED records in memory. Put it in `src/main.rs`:

```rust
use bedder::{
    bedder_bed::BedderBed,
    chrom_ordering::parse_genome,
    intersection::{IntersectionIterator, Intersections},
};
use std::io::{self, Cursor};

fn example_intersection() -> io::Result<Intersections> {
    let genome = parse_genome(b"chr1\t1000\n".as_slice())?;
    let a = BedderBed::new(Cursor::new(b"chr1\t100\t200\n".as_slice()), None::<&str>);
    let b = BedderBed::new(Cursor::new(b"chr1\t150\t250\n".as_slice()), None::<&str>);

    let mut intersections = IntersectionIterator::new(
        Box::new(a),
        vec![Box::new(b)],
        &genome,
        0,     // max_distance: overlaps only
        0,     // n_closest: disable nearest-neighbor search
        false, // retain query intervals even when they have no overlaps
    )?;

    intersections.next().expect("one query record")
}

fn main() -> io::Result<()> {
    let hits = example_intersection()?;
    let a = hits.base_interval.lock();
    println!(
        "{}:{}-{}: {} overlap(s)",
        a.chrom(),
        a.start(),
        a.stop(),
        hits.overlapping.len()
    );
    Ok(())
}
```

Run the example:

```bash
$ cargo run
chr1:100-200: 1 overlap(s)
```

### Input Records

Coordinates are zero-based and half-open. Each input must be sorted by chromosome
in the order supplied to `parse_genome`, then by start position. For larger
inputs, iterate over `IntersectionIterator`: each item is an
`io::Result<Intersections>` for one query record. Each hit's `id` identifies its
source by index in the vector of other inputs.

For files, use `BedderBed::new(BufReader::new(File::open(path)?), Some(path))`, or
`bedder::sniff::open(reader, path)?.0.into_positioned_iterator()` for format
detection. Custom record streams can implement `bedder::position::PositionedIterator`.

### VCF INFO and FILTER Fields

VCF positions retain their underlying `rust_htslib::bcf::Record`. Match on
`Position::Vcf` to access typed INFO values and FILTER tags.

For example, save this tab-separated file as `variants.vcf`:

```vcf
##fileformat=VCFv4.2
##contig=<ID=chr1,length=1000>
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total depth">
##FILTER=<ID=LowQual,Description="Low quality">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	151	.	A	G	50	PASS	DP=35
chr1	161	.	C	T	10	LowQual	DP=40
chr1	171	.	G	A	50	PASS	DP=8
```

In `example_intersection()`, replace the construction of `b` with:

```rust
let b = bedder::bedder_vcf::BedderVCF::from_path("variants.vcf")?;
```

Keep the BED query and iterator setup, then replace `main()` with this function
and its helper. It counts overlapping variants with INFO/DP at least 20 and no
failing FILTER tags:

```rust
fn count_depth_pass(hits: &Intersections) -> Result<usize, Box<dyn std::error::Error>> {
    let mut count = 0;
    for hit in &hits.overlapping {
        let position = hit.interval.lock();
        let bedder::position::Position::Vcf(vcf) = &*position else {
            continue;
        };
        if !vcf.record.has_filter(b"PASS".as_slice()) {
            continue;
        }
        let depth = vcf
            .record
            .info(b"DP")
            .integer()?
            .and_then(|values| values.first().copied());
        if depth.is_some_and(|dp| dp >= 20) {
            count += 1;
        }
    }
    Ok(count)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let hits = example_intersection()?;
    println!(
        "{} variant(s) meet the depth and FILTER criteria",
        count_depth_pass(&hits)?
    );
    Ok(())
}
```

```bash
$ cargo run
1 variant(s) meet the depth and FILTER criteria
```

The VCF's one-based POS 151 is exposed as start 150 in `bedder`.

Here `DP` must be declared as an integer INFO field in the VCF header. A tag absent
from a record returns `None`; an undefined tag or a type mismatch returns an
error, propagated by `?`. Explicit missing integer values use HTSlib's negative
sentinel and also fail this positive-depth threshold. Use `.float()`, `.string()`,
or `.flag()` for other INFO types; retain all values for fields with multiple
entries instead of taking the first.

`has_filter(b"PASS".as_slice())` also accepts an empty FILTER list (VCF `.`), so
this example means **no failing filters**, not necessarily that filtering was
performed. To require explicit PASS, use this condition instead of `has_filter`:
`vcf.record.filters().any(|id| vcf.record.header().id_to_name(id) == b"PASS")`.
To check a particular failure, use `vcf.record.has_filter(b"LowQual".as_slice())`.

## Embedded Python

To run Python inside your Rust application, use bedder's Python wrappers.

Add a direct PyO3 dependency matching bedder's version:

```toml
pyo3 = "0.26.0"
```

Keep `example_intersection()` above and replace `main()` with:

```rust
use bedder::{py::PyIntersections, report_options::ReportOptions};
use pyo3::{prelude::*, types::PyDict};
use std::sync::Arc;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let hits = example_intersection()?;
    Python::initialize();

    Python::attach(|py| -> PyResult<()> {
        bedder::py::initialize_python(py)?;
        let locals = PyDict::new(py);
        locals.set_item("hits", PyIntersections::new(
            hits, Arc::new(ReportOptions::builder().build()),
        ))?;
        py.run(
            c"print(hits.base_interval.chrom, len(hits.overlapping), flush=True)",
            None,
            Some(&locals),
        )
    })?;
    Ok(())
}
```

```bash
$ cargo run
chr1 1
```

Python receives bedder's existing wrappers: it can inspect
`hits.base_interval`, iterate over `hits.overlapping`, or call `hits.report()` to
obtain report fragments. `initialize_python` registers `bedder` and `bedder_py`
in that interpreter and also adds wrapper classes to Python's builtins. Initialize
this environment once, then reuse it for subsequent records.

For the CLI-style callback convention, functions use names such as
`bedder_count(fragment) -> int`. The public `introspect_python_functions` and
`CompiledPython` helpers handle discovery and evaluation; the example above
executes Python directly and does not require that convention.

### VCF Fields from Python

With VCF records as the `b` input above, Python can call `position.vcf()` to get
the VCF wrapper (`None` for other record types). This callback applies the same
depth and FILTER criteria to a report fragment:

```python
def bedder_depth_pass(fragment) -> int:
    count = 0
    for position in fragment.b:
        vcf = position.vcf()
        if vcf is None:
            continue
        if any(tag != "PASS" for tag in vcf.filters):
            continue
        depth = vcf.info("DP")
        if depth is not None and depth >= 20:
            count += 1
    return count

for fragment in hits.report():
    print(bedder_depth_pass(fragment), flush=True)  # 1 for the sample VCF
```

Run this code in the interpreter where the Rust example supplies `hits` (or use
the callback with the CLI). For `Number=1,Type=Integer`, `info("DP")` returns a
scalar integer; an absent tag returns `None`, and an undefined header tag raises
`KeyError`. Multiple-value numeric INFO fields return lists. As in Rust, an
explicit missing integer sentinel fails the `>= 20` check.

`vcf.filters` is a list of names such as `["PASS"]` or `["LowQual"]`; this example
also accepts an empty list. Use `vcf.filters == ["PASS"]` to require explicit
PASS. You can update shared records with `vcf.set_info("DP", 50)` or
`vcf.filters = ["LowQual"]`; the corresponding tags must already be declared in
the VCF header. These changes affect the in-memory record; writing an output VCF
is a separate step.

## Python Extension Module

To support `import my_intervals` from a separate Python process, create a library
crate named `my_intervals`. Keep the bedder dependency and add these settings:

```toml
[lib]
crate-type = ["cdylib"]

[dependencies.pyo3]
version = "0.26.0"
features = ["extension-module"]
```

Put `example_intersection()` and its imports in `src/lib.rs`, then add:

```rust
use bedder::{py::PyIntersections, report_options::ReportOptions};
use pyo3::{exceptions::PyOSError, prelude::*};
use std::sync::Arc;

#[pyfunction]
fn intersect_example() -> PyResult<PyIntersections> {
    let hits = example_intersection()
        .map_err(|err| PyOSError::new_err(err.to_string()))?;
    Ok(PyIntersections::new(
        hits, Arc::new(ReportOptions::builder().build()),
    ))
}

#[pymodule]
fn my_intervals(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyIntersections>()?;
    m.add_function(wrap_pyfunction!(intersect_example, m)?)?;
    Ok(())
}
```

In an activated Python virtual environment, run these commands in the extension
project:

```bash
pip install maturin
maturin develop
```

From Python:

```python
import my_intervals

hits = my_intervals.intersect_example()
print(hits.base_interval.chrom, len(hits.overlapping))  # chr1 1
```

Python owns the interpreter in this case, so the extension does not call
`Python::initialize()`. Keep `extension-module` enabled only for extension builds;
it changes Python linking and can break binaries that embed Python. See the
[PyO3 0.26 build guide](https://pyo3.rs/v0.26.0/building-and-distribution.html).

## Build Requirements

As of bedder 0.1.14, PyO3 is an unconditional dependency. The `python_embedded`
feature is empty; disabling default features does not remove Python support.
Building the Rust example still requires a usable Python development installation
and the native toolchain required by bedder's HTSlib dependencies. Embedded Python
also needs its runtime and standard library available when the application runs.
Use `PYO3_PYTHON` to select the build interpreter if necessary.
