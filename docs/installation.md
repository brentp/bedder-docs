# Installation of bedder

Bedder is build with [rust](https://www.rust-lang.org/tools/install) but it embeds a python interpreter. The binary is self-contained, but it does require python packages to be available.

It is recommended to use [uv](https://docs.astral.sh/uv/getting-started/installation/) venv to do so. See below for more details.

## Linux Installation

```
# Download Linux binary and make it executable
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.7/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64

# Check whether install was successful
./bedder-static-linux-x86_64

```

If installation is successful it will show the following output:

```
bedder v0.1.7

Usage: bedder <COMMAND>

Commands:
  full       Full functionality with all options (almost never use this)
  intersect  Intersection mode - hides closest options
  closest    Closest mode - hides overlap requirements
  help       Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
```

### Linux Installation Details

**⚠️ Important:** Bedder requires Python 3.13 specifically. Please ensure you're using this version when creating the virtual environment.

Create a python virtual environment and install bedder

```
uv venv --python 3.13
source venv/bin/activate
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.7/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64
```

If you see:

```
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
Fatal Python error: Failed to import encodings module
Python runtime state: core initialized
ModuleNotFoundError: No module named 'encodings'

Current thread 0x0000000040a43540 (most recent call first):
  <no Python frame>
```

This means it can't find your python libraries. You can activate a uv (or pip) venv or set PYTHONPATH, e.g.

```
PYTHONPATH=~/miniforge3/lib/python3.13/
```

or with uv:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.13
uv venv
source .venv/bin/activate
```
