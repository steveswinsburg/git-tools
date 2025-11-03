# Git Tools

A Python script to manage multiple Git repositories from a JSON configuration file. Perfect for handling hundreds of repositories with fault tolerance.

## Features

🔄 **Clone Mode** - Clone all repositories, skip existing ones  
🚀 **Update Mode** - Switch to main branch and pull latest changes  
📊 **Status Mode** - View repository status and health  
🛡️ **Fault Tolerant** - Continues processing even when individual repos fail  
📝 **Smart Logging** - Detailed console and file logging  

## Quick Start

1. Create `repositories.json`:
```json
{
  "base_url": "https://github.com/steveswinsburg",
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

## Options

- `-v` - Verbose logging
- `--help` - Show all options

## Notes

- Skips repos with uncommitted changes during updates
- Handles both `main` and `master` branches
- Logs all activity to console with timestamps
- Requires Python 3.6+ and Git CLI