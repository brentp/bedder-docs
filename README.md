[![documentation build](https://github.com/brentp/bedder-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/brentp/bedder-docs/actions/workflows/ci.yml)

To view or modify docs, do the following:

```
python -m venv venv # or python3
source venv/bin/activate
pip install mkdocs-material

mkdocs serve
# open 127.0.0.1:8000/bedder-docs
```

Then edit/add files in `docs/*.md`.

## Agent skill

`docs/agent-skill.md` is the human-editable source for the Bedder agent guide.
`bedder-skill/SKILL.md` is the installable skill generated from that source with
the required YAML frontmatter. Do not edit `bedder-skill/SKILL.md` directly.

The documentation build regenerates `SKILL.md` and fails if the committed artifact
is stale. After editing `docs/agent-skill.md`, regenerate and verify it locally:

```bash
python scripts/generate_skill.py
python scripts/generate_skill.py --check
```

The MkDocs post-build hook then copies the complete `bedder-skill/` directory into
the published site without rendering `SKILL.md` as HTML. Development and release
builds expose the raw skill at:

- `https://brentp.github.io/bedder-docs/dev/bedder-skill/SKILL.md`
- `https://brentp.github.io/bedder-docs/latest/bedder-skill/SKILL.md`

After viewing changes locally, open a PR to github.com/brentp/bedder-docs and the continuous integration via github actions will build and update the docs at <https://brentp.github.io/bedder-docs/>

## Testing Documentation Examples

The examples in `docs/subcommands/intersection.md` can be tested to ensure they produce the expected output:

```bash
# Place the latest bedder binary in the repo root
cp /path/to/bedder ./bedder

# Run the test script
python scripts/test_intersection_examples.py
```

The script extracts all command examples from the markdown file, runs them against `./bedder`, and verifies the output matches the documented expected output. Make sure `./bedder` is the latest bedder binary before running the tests.
