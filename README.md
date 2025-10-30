# Git Tools

A few tools I've collected over the years to manage projects that have many git repos. Now in a single script form!

## Features

🔄 **Clone Mode** - Clone all repositories, skip existing ones  
🚀 **Update Mode** - Switch to main branch and pull latest changes  
📊 **Status Mode** - View repository status and health  
🛡️ **Fault Tolerant** - Continues processing even when individual repos fail  

## Quick Start

1. Create `repositories.json`:
```json
{
  "base_url": "git@github.com:steveswinsburg/",
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

## Options

- `-v` - Verbose logging
- `--help` - Show all options

## Notes

- Skips repos with uncommitted changes during updates
- Handles both `main` and `master` branches
