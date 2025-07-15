# Installation of bedder 
## Binary options
- bedder-static-linux-x86_64: Static binary for Linux x86_64 
- bedder-static-macos-x86_64: Mostly static binary for macOS x86_64 

## Linux Installation
As of June 2025, the linux binary, when installed on a cluster, requires the use of a python virtual environment (venv). 
```
# Download Linux binary and make it executable
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.2/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64

# Check whether install was successful
bedder

```
If installation is successful, running the command "bedder" should produce an error regarding lack of input arguments:
```
[<DATE> INFO  bedder] starting up
error: the following required arguments were not provided:
  -a <QUERY_PATH>
  -b <OTHER_PATHS>
  --genome <GENOME_FILE>
```

If installation is unsuccessful, consider reinstalling in a python virtual environment or relocating the binary:

### Optional relocation of the linux binary
This may be necessary if above check fails or if you are hoping to install the linux binary in a particular location distinct from the default. 

```

# To determine what $PATH are available: 
echo "$PATH"
# Move to $PATH
sudo mv bedder-static-linux-x86_64 /usr/local/bin/bedder

```

## macOS Installation 
```
# Download Mac binary and make executable
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.2/bedder-static-macos-x86_64
chmod +x bedder-static-macos-x86_64

# Check whether install was successful
bedder

```
Once again, if installation is successful, running the command "bedder" should produce the following error regarding lack of input arguments:
```
[<DATE> INFO  bedder] starting up
error: the following required arguments were not provided:
  -a <QUERY_PATH>
  -b <OTHER_PATHS>
  --genome <GENOME_FILE>
```
If installation is unsuccessful, consider reinstalling in a python virtual environment or relocating the binary:

### Optional relocation of the macOS binary 
This may be necessary if above check fails or if you are hoping to install the macOS binary in a particular location distinct from the default. 
```
# To determine what $PATH are available: 
echo "$PATH"
# Move to $PATH
sudo mv bedder-static-macos-x86_64 /usr/local/bin/bedder

```

## Binary Information 
- Linux binary: Fully static (~6MB, no dependencies)
    - fully static when installing on a local machine
    - testing has identified that as of June 2025, installation on a remote cluster may require the use of a python venv
- macOS binary: Mostly static (~6MB, minimal system dependencies)
- Python: Works with any Python 3.8+ system
- Architecture: x86_64