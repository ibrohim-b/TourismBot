# Quick Start: Media Upload Feature

## What's New? 🎉

You can now upload images, audio, video, and documents directly from the admin panel!

## How to Use

### 1. Start the Web Server
```bash
cd /Users/ibrohim/PycharmProjects/TourismBot
uvicorn web.main:app --reload
```

### 2. Three Ways to Upload Media

#### Option A: Web Form (Easiest! 🌐)
1. Open [media_upload.html](media_upload.html) in your browser
2. Select upload type (General or Entity-specific)
3. Choose your file
4. Click "Upload"
5. Get the file path

#### Option B: Admin Panel (Manual ⚙️)
1. Go to http://localhost:8000/admin
2. Edit a City/Excursion/Point
3. Get file path from web form (Option A)
4. Paste into the image/audio/video field
5. Save

#### Option C: API (Programmatic 💻)

**Upload to a Point:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-point?point_id=1&media_type=audio" \
  -F "file=@/path/to/guide.mp3"
```

**Response:**
```json
{
  "path": "media/audio/point_1_guide.mp3",
  "message": "Point audio uploaded successfully"
}
```

## Supported Files

| Type | Formats | Max Size |
|------|---------|----------|
| Images | JPG, PNG, GIF, WebP, BMP | 500 MB |
| Audio | MP3, WAV, OGG, M4A, AAC, FLAC | 500 MB |
| Video | MP4, AVI, MOV, MKV, WebM, FLV, WMV | 500 MB |
| Documents | PDF, TXT, DOC, DOCX, XLS, XLSX | 500 MB |

## Examples

### Upload City Image
1. Open media_upload.html
2. Switch to "Entity Upload" tab
3. Select "🏙️ City"
4. Enter City ID: `1`
5. Select image file
6. Click Upload
7. Copy returned path to City admin form

### Upload Point Audio Guide
1. Open media_upload.html
2. Switch to "Entity Upload" tab
3. Select "📍 Point"
4. Enter Point ID: `1`
5. Select "🎵 Audio"
6. Select MP3 file
7. Click Upload
8. Copy returned path to Point admin form

### Upload Excursion Video
1. Open media_upload.html
2. Switch to "Entity Upload" tab
3. Select "🗺️ Excursion"
4. Enter Excursion ID: `1`
5. Select "🎥 Video"
6. Select MP4 file
7. Click Upload
8. Copy returned path to Excursion admin form

## File Organization

Files are automatically organized:
```
/media
├── images/      # City, Excursion, Point images
├── audio/       # Point audio guides
├── videos/      # Excursion and Point videos
└── documents/   # PDFs and documents
```

## Accessing Media

Once uploaded, access files at:
```
http://localhost:8000/media/images/city_1_paris.jpg
http://localhost:8000/media/audio/point_1_guide.mp3
http://localhost:8000/media/videos/excursion_2_tour.mp4
```

## Database Fields

**Cities**
- `image`: City photo

**Excursions**
- `image`: Preview image
- `video`: Promotional video

**Points**
- `image`: Landmark photo
- `audio`: Audio guide
- `video`: Demonstration video

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /api/media/upload` | Upload any file |
| `POST /api/media/upload-city` | Upload city image |
| `POST /api/media/upload-excursion` | Upload excursion media |
| `POST /api/media/upload-point` | Upload point media |

## Python Example

```python
import aiohttp
import asyncio

async def upload_city_image(city_id, image_path):
    async with aiohttp.ClientSession() as session:
        with open(image_path, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('file', f)
            
            async with session.post(
                f'http://localhost:8000/api/media/upload-city?city_id={city_id}',
                data=data
            ) as resp:
                return await resp.json()

# Usage
result = asyncio.run(upload_city_image(1, 'paris.jpg'))
print(result['path'])  # media/images/city_1_paris.jpg
```

## Testing

Run the test script:
```bash
python test_media_upload.py
```

## Troubleshooting

**"File type not allowed"**
- Check file extension (must match allowed list)
- Remove special characters from filename

**"File too large"**
- Maximum size is 500 MB
- For videos, compress first

**"City/Point not found"**
- Verify the ID exists in database
- Check admin panel for correct ID

**Files not accessible**
- Verify media directory exists
- Check file permissions
- Restart web server

## More Information

- 📖 Full guide: [MEDIA_UPLOAD_GUIDE.md](MEDIA_UPLOAD_GUIDE.md)
- 🔧 Implementation details: [MEDIA_IMPLEMENTATION_SUMMARY.md](MEDIA_IMPLEMENTATION_SUMMARY.md)
- 🧪 Test script: [test_media_upload.py](test_media_upload.py)

## Need Help?

1. Check the error message
2. Review [MEDIA_UPLOAD_GUIDE.md](MEDIA_UPLOAD_GUIDE.md)
3. Run [test_media_upload.py](test_media_upload.py) to test endpoints
4. Use [media_upload.html](media_upload.html) for a visual guide

Enjoy uploading! 🎬
