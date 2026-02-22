#!/usr/bin/env python3
"""
Test script for media upload functionality
"""
import asyncio
import aiohttp
import json
from pathlib import Path

# Create a test image file
def create_test_image():
    """Create a small test image"""
    import base64
    # Small 1x1 PNG
    png_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )
    test_file = Path("test_image.png")
    test_file.write_bytes(png_data)
    return test_file

async def test_media_upload():
    """Test media upload endpoints"""
    base_url = "http://localhost:8000"
    
    # Create test image
    test_image = create_test_image()
    
    print("🧪 Testing Media Upload API...")
    print("-" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: General media upload
        print("\n1️⃣ Testing general media upload...")
        try:
            with open(test_image, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename='test.png')
                data.add_field('media_type', 'images')
                
                async with session.post(f'{base_url}/api/media/upload', data=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        print(f"   ✅ Success: {result['path']}")
                    else:
                        print(f"   ❌ Error {resp.status}: {await resp.text()}")
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
        
        # Test 2: City media upload (if city exists)
        print("\n2️⃣ Testing city media upload...")
        try:
            with open(test_image, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename='city_test.png')
                
                async with session.post(f'{base_url}/api/media/upload-city?city_id=1', data=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        print(f"   ✅ Success: {result['path']}")
                    elif resp.status == 404:
                        print(f"   ℹ️  No city with ID 1 (expected if database is empty)")
                    else:
                        print(f"   ❌ Error {resp.status}: {await resp.text()}")
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
        
        # Test 3: Check media directory structure
        print("\n3️⃣ Checking media directory structure...")
        media_dir = Path(__file__).parent / "media"
        if media_dir.exists():
            subdirs = [d for d in media_dir.iterdir() if d.is_dir()]
            print(f"   ✅ Media directory exists")
            print(f"   📁 Subdirectories: {[d.name for d in subdirs]}")
        else:
            print(f"   ℹ️  Media directory will be created on first upload")
    
    # Cleanup
    test_image.unlink()
    
    print("\n" + "-" * 50)
    print("✅ Media upload test completed!")

if __name__ == "__main__":
    asyncio.run(test_media_upload())
