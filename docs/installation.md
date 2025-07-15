# Install bedder 
## Binary options
- bedder-static-linux-x86_64: Static binary for Linux x86_64 (no dependencies required)
- bedder-static-macos-x86_64: Mostly static binary for macOS x86_64 (minimal system dependencies)

## Linux Installation
As of June 2025, the linux binary, when installed on a cluster, requires the use of a python virtual environment (venv). 
```
# Download Linux binary and make it executable
wget https://github.com/quinlan-lab/bedder-rs/releases/download/v0.1.2/bedder-static-linux-x86_64
chmod +x bedder-static-linux-x86_64

# Check whether install was successful
# If successful, will recieve specific error due to lack of arguments
bedder

# Optional: 
# May be necessary if above check fails
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
# If successful, will recieve specific error due to lack of arguments
bedder

# Optional: 
# May be necessary if above check fails
# To determine what $PATH are available: 
echo "$PATH"
# Move to $PATH
sudo mv bedder-static-macos-x86_64 /usr/local/bin/bedder

```

## Binary Information 
- Linux binary: Fully static (~6MB, no dependencies)
- macOS binary: Mostly static (~6MB, minimal system dependencies)
- Python: Works with any Python 3.8+ system
- Architecture: x86_64