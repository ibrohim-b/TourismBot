#!/usr/bin/env python3
"""
Startup script for the Web Admin Panel
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import and run web admin
from web.run_admin import main

if __name__ == "__main__":
    main()
