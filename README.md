[![documentation build](https://github.com/brentp/bedder-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/brentp/bedder-docs/actions/workflows/ci.yml)

To view or modify docs, do the following:

```
python -m venv venv # or python3
source venv/bin/activate
pip install mkdocs-material

mkdocs serve
# open 127.0.0.1:8000/bedder-docs
```

Then edit/add files in `docs/*.md`

After viewing changes locally, open a PR to github.com/brentp/bedder-docs and the continuous integration via github actions will build and update the docs at <https://brentp.github.io/bedder-docs/>
