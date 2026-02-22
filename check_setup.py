#!/usr/bin/env python
"""
Quick setup and validation script for the Tourism Bot Admin Panel
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Check if all required environment variables and files exist"""
    print("🔍 Checking environment setup...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating with defaults...")
        with open(".env", "w") as f:
            f.write("DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3\n")
            f.write("ADMIN_USERNAME=admin\n")
            f.write("ADMIN_PASSWORD=admin123\n")
        print("✅ .env file created with default credentials")
        print("   Change these in production!")
    else:
        print("✅ .env file exists")
    
    # Check imports
    print("\n🔍 Checking required packages...")
    required_packages = [
        "fastapi",
        "sqlalchemy",
        "sqladmin",
        "pydantic",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages found")
    return True

def check_database():
    """Check if database can be initialized"""
    print("\n🔍 Checking database...")
    db_file = Path("db.sqlite3")
    if db_file.exists():
        print(f"✅ Database exists at {db_file}")
    else:
        print(f"⚠️  Database will be created on first run")
    return True

def main():
    """Run all checks"""
    print("=" * 50)
    print("Tourism Bot Admin Panel - Setup Check")
    print("=" * 50)
    
    os.chdir(Path(__file__).parent)
    
    all_ok = True
    all_ok = check_environment() and all_ok
    all_ok = check_database() and all_ok
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ Environment is ready!")
        print("\nTo start the admin panel:")
        print("  cd web")
        print("  python run_admin.py")
        print("\nThen visit: http://localhost:8000/admin")
        print("Default credentials: admin / admin123")
    else:
        print("⚠️  Please fix the issues above")
        sys.exit(1)
    
    print("=" * 50)

if __name__ == "__main__":
    main()
