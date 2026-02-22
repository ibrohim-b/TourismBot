# Media Upload Feature - Implementation Summary

## Overview
Added comprehensive media upload functionality to the TourismBot admin panel, allowing users to upload images, audio, video, and documents that can be attached to cities, excursions, and points of interest.

## Changes Made

### 1. Database Models Updated (`db/models.py`)
Added new media fields to support multiple file types:

**City Model**
- `image`: Optional image path for city photos

**Excursion Model**
- `image`: Optional image for excursion preview
- `video`: Optional promotional video

**Point Model**
- `video`: Optional video demonstration (added alongside existing audio/image)

### 2. Media Utility Module (`web/media.py`)
Created a complete media management system with:
- **File validation**: Checks file extensions and types
- **Secure file handling**: Uses werkzeug's secure_filename
- **Automatic organization**: Files sorted into type-specific directories
- **Size limits**: 500 MB maximum per file
- **Supported formats**:
  - Images: JPG, JPEG, PNG, GIF, WebP, BMP
  - Audio: MP3, WAV, OGG, M4A, AAC, FLAC
  - Videos: MP4, AVI, MOV, MKV, WebM, FLV, WMV
  - Documents: PDF, TXT, DOC, DOCX, XLS, XLSX
- **Unique filename handling**: Automatic numbering for duplicate names

### 3. Admin Panel Updates (`web/admin.py`)
Enhanced ModelView configurations with media fields:
- **CityAdmin**: Added image field to form and columns
- **ExcursionAdmin**: Added image and video fields
- **PointAdmin**: Added video field (audio and image already present)
- All fields include helpful descriptions and validation

### 4. API Endpoints (`web/crud.py`)
Added 4 new media upload endpoints:

**General Upload**
- `POST /api/media/upload`: Upload any supported file type

**Entity-Specific Uploads**
- `POST /api/media/upload-city`: Upload city image (auto-updates city record)
- `POST /api/media/upload-excursion`: Upload excursion image or video (auto-updates record)
- `POST /api/media/upload-point`: Upload point image, audio, or video (auto-updates record)

All endpoints return:
```json
{
  "path": "media/type/filename.ext",
  "message": "Success message"
}
```

### 5. Web Server Configuration (`web/main.py`)
- Automatic media directory creation on startup
- Static file serving: Media files accessible via `/media/...` URLs
- Directory structure auto-created for images, audio, videos, documents

### 6. Documentation
Created comprehensive guides:
- **MEDIA_UPLOAD_GUIDE.md**: User guide with API examples, best practices, and configuration
- **test_media_upload.py**: Test script to verify upload functionality

## File Organization

```
/media
├── images/
│   ├── city_1_paris.jpg
│   ├── excursion_2_eiffel_tower.jpg
│   └── point_5_louvre.jpg
├── audio/
│   ├── point_3_guide_en.mp3
│   └── point_4_historical_facts.wav
├── videos/
│   ├── excursion_1_intro.mp4
│   └── point_2_drone_footage.webm
└── documents/
    └── tour_guide_2024.pdf
```

## Usage Workflow

### Via API (Programmatic)
```python
import aiohttp

async def upload_to_point(point_id, audio_file):
    async with aiohttp.ClientSession() as session:
        with open(audio_file, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('file', f)
            
            async with session.post(
                f'http://localhost:8000/api/media/upload-point?point_id={point_id}&media_type=audio',
                data=data
            ) as resp:
                return await resp.json()
```

### Via Admin Panel (Manual)
1. Navigate to Cities/Excursions/Points
2. Click "Edit" on an item
3. Use API endpoints to get file paths
4. Paste path into the image/audio/video field
5. Save changes

### Via cURL
```bash
# Upload to point
curl -X POST "http://localhost:8000/api/media/upload-point?point_id=1&media_type=audio" \
  -F "file=@guide.mp3"

# Response:
# {
#   "path": "media/audio/point_1_guide.mp3",
#   "message": "Point audio uploaded successfully"
# }
```

## Key Features

✅ **Multiple file type support**: Images, audio, video, documents
✅ **Automatic database updates**: Entity-specific endpoints update records
✅ **File validation**: Type, size, and format checking
✅ **Secure file handling**: Prevents directory traversal and malicious uploads
✅ **Auto-organization**: Files sorted by type and prefixed by entity type
✅ **Static file serving**: Media accessible via HTTP
✅ **Error handling**: Clear error messages for upload failures
✅ **Scalability**: Handles large files (up to 500 MB)

## Error Handling

The system provides helpful error messages:
```json
{
  "detail": "File extension 'exe' not allowed. Allowed: mp3, wav, ogg, m4a, aac, flac"
}
```

Common scenarios:
- Invalid file type → 400 error with allowed formats
- File too large → 400 error with size limit
- Entity not found → 404 error
- Server error → 500 with description

## Testing

Run the test script:
```bash
python test_media_upload.py
```

This will:
1. Create a test image
2. Test general upload endpoint
3. Test city media upload endpoint
4. Verify media directory structure
5. Display results

## Database Migration

If upgrading from previous version:
1. New fields are optional (nullable)
2. No existing data will be lost
3. Existing models with NULL media paths work fine
4. Simply add media paths as needed

## Requirements

The following packages are already in requirements.txt:
- `fastapi`: Web framework
- `sqlalchemy`: ORM
- `aiosqlite`: Async SQLite
- `python-multipart`: File upload support
- `werkzeug`: Secure filename handling

## Configuration

Edit `web/media.py` to customize:
```python
MAX_FILE_SIZE = 500 * 1024 * 1024  # Change file size limit

ALLOWED_EXTENSIONS = {
    "images": {"jpg", "jpeg", "png", "gif", "webp", "bmp"},
    # Add/remove formats as needed
}
```

## Next Steps

After deployment:
1. Create media subdirectories (auto-created on startup)
2. Set proper file permissions (www-data or appropriate user)
3. Configure backup strategy for media folder
4. Monitor disk space usage
5. Consider CDN for large-scale deployment

## Support

For detailed information:
- See `MEDIA_UPLOAD_GUIDE.md` for complete API documentation
- Check `web/media.py` for implementation details
- Review test script for usage examples
