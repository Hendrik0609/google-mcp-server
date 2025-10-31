#!/usr/bin/env python3
"""
Setup script for Google MCP Server
Installs dependencies if not already present
"""

import subprocess
import sys
import os
from pathlib import Path

def check_and_install_dependencies():
    """Check if dependencies are installed, install if missing"""
    try:
        # Try importing a key dependency
        import mcp
        import google.oauth2.credentials
        return True
    except ImportError:
        print("Installing dependencies...")
        requirements_file = Path(__file__).parent / "requirements.txt"

        # Try with --user first (works on externally-managed systems)
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "-r", str(requirements_file),
                "--user",
                "--quiet"
            ])
            print("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            # If --user fails, try with venv
            print("Creating virtual environment...")
            venv_path = Path(__file__).parent / "venv"
            try:
                subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
                venv_python = venv_path / "bin" / "python"
                subprocess.check_call([
                    str(venv_python), "-m", "pip", "install",
                    "-r", str(requirements_file),
                    "--quiet"
                ])
                print("Dependencies installed in venv!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error installing dependencies: {e}", file=sys.stderr)
                return False

if __name__ == "__main__":
    if not check_and_install_dependencies():
        sys.exit(1)
    print("Setup complete!")
