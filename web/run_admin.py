#!/usr/bin/env python3
"""
Startup script for the Tourism Bot Admin Panel
"""

import uvicorn
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Start the admin panel server"""
    print("🚀 Starting Tourism Bot Admin Panel...")
    print("📍 Admin panel will be available at: http://localhost:8000/admin")
    print("🔐 Default credentials: admin / admin123")
    print("💡 You can change credentials by setting ADMIN_USERNAME and ADMIN_PASSWORD environment variables")
    print("-" * 60)
    
    uvicorn.run(
        "web.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()