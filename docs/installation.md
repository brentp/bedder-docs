# Installation of bedder

Bedder is build with [rust](https://www.rust-lang.org/tools/install) but it embeds a python interpreter. The binary is self-contained, but it does require python packages to be available.

It is recommended to use [uv](https://docs.astral.sh/uv/getting-started/installation/) venv to do so. See below for more details.

## Linux Installation

```
# Download Linux binary and make it executable
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.6/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64

# Check whether install was successful
./bedder-static-linux-x86_64

```

If installation is successful it will show the following output:

```
bedder v0.1.6

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

Create a python virtual environment and install bedder

```
python -m venv venv
source venv/bin/activate
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.6/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64
```
