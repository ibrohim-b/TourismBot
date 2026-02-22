#!/usr/bin/env python3
"""
Startup script for the Telegram Bot Worker
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import and run bot
from bot.main import main
import asyncio

if __name__ == "__main__":
    print("🤖 Starting Telegram Bot Worker...")
    asyncio.run(main())
