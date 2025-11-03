# Git Tools

A few tools I've collected over the years to manage projects that have many git repos. Now in a single script form!

## Features

**Clone Mode** - Clone all repositories, skip existing ones  
**Update Mode** - Switch to main branch and pull latest changes  
**Status Mode** - View repository status and health  
**Custom Checkout Directory** - Configure where repositories are cloned  
**Multiple Config Files** - Support different repository configurations  
**Fault Tolerance** - Continues processing even when individual repos fail  

## Quick Start

1. Create `repositories.json`:
```json
{
  "base_url": "https://github.com/steveswinsburg/",
  "checkout_directory": "../my-projects",
  "repositories": [
    "repo1",
    "repo2", 
    "repo3",
    "another-repo",
    "yet-another-repo"
  ]
}
```

2. Run commands:
```bash
python3 git-tools.py clone   # Clone all repos
python3 git-tools.py update  # Update all repos  
python3 git-tools.py status  # Check repo status
```

## Configuration

### Config File Format

- `base_url` - Base URL for repositories (with or without trailing slash)
- `checkout_directory` - Directory where repositories will be cloned (default: current directory)
- `repositories` - Array of repository names to manage

### Multiple Config Files

You can use different configuration files for different projects or environments:

```bash
# Work repos
python3 git-tools.py -c work-repos.json clone

# Personal repos  
python3 git-tools.py --config personal-repos.json update
```

## Options

- `-c, --config` - Specify custom config file (default: repositories.json)
- `-v, --verbose` - Verbose logging
- `-h, --help` - Show all options

## Examples

```bash
# Basic usage with default config
python3 git-tools.py clone
python3 git-tools.py update
python3 git-tools.py status

# Using custom config files
python3 git-tools.py -c work-repositories.json clone
python3 git-tools.py --config personal-repositories.json update

# Verbose output with custom config
python3 git-tools.py -v --config repositories.json status
```
