#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional


class GitTools:
    def __init__(self):
        """Initialize the repository manager with configuration."""
        self.config_file = "repositories.json"
        self.config = self._load_config()
        self.base_url = self.config.get("base_url", "")
        self.checkout_directory = Path(self.config.get("checkout_directory", "."))
        self.repositories = self.config.get("repositories", [])
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file {self.config_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {self.config_file}: {e}")
            sys.exit(1)
    
    def _run_command(self, command: List[str], cwd: Optional[str] = None) -> tuple:
        """Run a shell command and return (success, output, error)."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timeout"
        except Exception as e:
            return False, "", str(e)
    
    def _get_repo_url(self, repo_name: str) -> str:
        """Construct the full repository URL."""
        # Remove trailing slash from base_url if present
        base = self.base_url.rstrip('/')
        return f"{base}/{repo_name}"
    
    def _repo_exists(self, repo_name: str) -> bool:
        """Check if repository directory exists and is a git repo."""
        repo_path = self.checkout_directory / repo_name
        return repo_path.exists() and (repo_path / '.git').exists()
    
    def _get_repo_path(self, repo_name: str) -> Path:
        """Get the full path to a repository."""
        return self.checkout_directory / repo_name
    
    def clone_repositories(self) -> None:
        """Clone all repositories. Skip if already exists."""
        self.logger.info(f"Starting clone operation for {len(self.repositories)} repositories")
        self.logger.info(f"Checkout directory: {self.checkout_directory}")
        
        # Ensure checkout directory exists
        self.checkout_directory.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for repo in self.repositories:
            self.logger.info(f"Processing repository: {repo}")
            
            if self._repo_exists(repo):
                self.logger.info(f"Repository {repo} already exists, skipping")
                skip_count += 1
                continue
            
            repo_url = self._get_repo_url(repo)
            repo_path = self._get_repo_path(repo)
            self.logger.info(f"Cloning {repo_url} to {repo_path}")
            
            success, output, error = self._run_command(['git', 'clone', repo_url, str(repo_path)])
            
            if success:
                self.logger.info(f"Successfully cloned {repo}")
                success_count += 1
            else:
                self.logger.error(f"Failed to clone {repo}: {error}")
                error_count += 1
        
        self.logger.info(f"Clone operation completed: {success_count} cloned, {skip_count} skipped, {error_count} errors")
    
    def update_repositories(self) -> None:
        """Update all repositories by switching to main/master and pulling."""
        self.logger.info(f"Starting update operation for {len(self.repositories)} repositories")
        self.logger.info(f"Checkout directory: {self.checkout_directory}")
        
        success_count = 0
        error_count = 0
        
        for repo in self.repositories:
            self.logger.info(f"Updating repository: {repo}")
            
            if not self._repo_exists(repo):
                self.logger.warning(f"Repository {repo} does not exist, skipping")
                continue
            
            repo_path = self._get_repo_path(repo)
            
            # Check if repo has uncommitted changes
            success, output, error = self._run_command(['git', 'status', '--porcelain'], cwd=str(repo_path))
            if success and output.strip():
                self.logger.warning(f"Repository {repo} has uncommitted changes, skipping update")
                error_count += 1
                continue
            
            # Switch to main branch
            success, output, error = self._run_command(['git', 'checkout', 'main'], cwd=str(repo_path))
            if not success:
                # Try 'master' if 'main' doesn't exist
                success, output, error = self._run_command(['git', 'checkout', 'master'], cwd=str(repo_path))
                if not success:
                    self.logger.error(f"Failed to checkout main/master branch for {repo}: {error}")
                    error_count += 1
                    continue
            
            # Pull latest changes
            success, output, error = self._run_command(['git', 'pull'], cwd=str(repo_path))
            if success:
                self.logger.info(f"Successfully updated {repo}")
                success_count += 1
            else:
                self.logger.error(f"Failed to pull latest changes for {repo}: {error}")
                error_count += 1
        
        self.logger.info(f"Update operation completed: {success_count} updated, {error_count} errors")
    
    def list_repositories(self) -> None:
        """List all repositories and their status."""
        self.logger.info("Repository Status:")
        self.logger.info(f"Base URL: {self.base_url}")
        self.logger.info(f"Checkout Directory: {self.checkout_directory}")
        self.logger.info("-" * 50)
        
        for repo in self.repositories:
            if self._repo_exists(repo):
                repo_path = self._get_repo_path(repo)
                
                # Get current branch
                success, branch, error = self._run_command(['git', 'branch', '--show-current'], cwd=str(repo_path))
                branch_info = branch if success else "unknown"
                
                # Check for uncommitted changes
                success, status, error = self._run_command(['git', 'status', '--porcelain'], cwd=str(repo_path))
                has_changes = success and status.strip()
                status_info = "dirty" if has_changes else "clean"
                
                self.logger.info(f"{repo:<30} EXISTS (branch: {branch_info}, status: {status_info})")
            else:
                self.logger.info(f"{repo:<30} NOT FOUND")


def show_help():
    """Display simple help information."""
    print("Git Tools")
    print("Manage multiple git repos for a project\n")
    
    print("Commands:")
    print("  clone     Clone all repositories from config")
    print("  update    Update all repositories (switch to main and pull)")
    print("  status    Show status of all repositories")

    print("\nExamples:")
    print("  python3 git-tools.py clone")
    print("  python3 git-tools.py update")
    print("  python3 git-tools.py status")
    
    print("\nOptions:")
    print("  -v, --verbose    Enable verbose logging")
    print("  -h, --help       Show this help")


def main():
    # Simple argument parsing
    args = sys.argv[1:]
    
    # Handle help
    if not args or args[0] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    # Handle verbose flag
    verbose = False
    if "-v" in args or "--verbose" in args:
        verbose = True
        args = [arg for arg in args if arg not in ["-v", "--verbose"]]
    
    # Check for valid command
    if not args or args[0] not in ["clone", "update", "status"]:
        print("Error: Please specify a valid command (clone, update, or status)")
        print("Use --help for more information")
        sys.exit(1)
    
    mode = args[0]
    
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize manager
    gittools = GitTools()
    
    # Execute requested operation
    if mode == "clone":
        gittools.clone_repositories()
    elif mode == "update":
        gittools.update_repositories()
    elif mode == "status":
        gittools.list_repositories()


if __name__ == "__main__":
    main()