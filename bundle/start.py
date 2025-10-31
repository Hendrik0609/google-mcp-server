#!/usr/bin/env python3
"""
Startup wrapper for Google MCP Server
Loads vendored dependencies and starts the server
"""

import sys
from pathlib import Path

def main():
    """Main entry point"""
    # Add vendored dependencies to path
    vendor_path = Path(__file__).parent / "vendor"
    if vendor_path.exists():
        sys.path.insert(0, str(vendor_path))

    # Import and run the server
    server_path = Path(__file__).parent / "server.py"

    # Execute the server script
    with open(server_path) as f:
        code = compile(f.read(), server_path, 'exec')
        exec(code, {'__name__': '__main__', '__file__': str(server_path)})

if __name__ == "__main__":
    main()
