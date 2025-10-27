#!/usr/bin/env python3
"""
Startup wrapper for Google MCP Server
Ensures dependencies are installed before starting the server
"""

import sys
import subprocess
from pathlib import Path

def ensure_setup():
    """Ensure dependencies are installed"""
    setup_script = Path(__file__).parent / "setup.py"
    try:
        result = subprocess.run(
            [sys.executable, str(setup_script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"Setup failed: {result.stderr}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"Error during setup: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point"""
    # Only run setup check on first run or if imports fail
    try:
        import mcp
        import google.oauth2.credentials
    except ImportError:
        if not ensure_setup():
            sys.exit(1)

    # Import and run the server
    server_path = Path(__file__).parent / "server.py"

    # Execute the server script
    with open(server_path) as f:
        code = compile(f.read(), server_path, 'exec')
        exec(code, {'__name__': '__main__', '__file__': str(server_path)})

if __name__ == "__main__":
    main()
