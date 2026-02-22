# Media Upload Feature

## Overview
The media upload feature allows users to upload images, audio, video, and document files through the admin panel. Files are automatically organized in the `/media` folder by type and can be attached to cities, excursions, and points.

## Supported File Types

### Images
- Formats: `jpg`, `jpeg`, `png`, `gif`, `webp`, `bmp`
- Max size: 500 MB
- Used for: Cities, Excursions, Points

### Audio
- Formats: `mp3`, `wav`, `ogg`, `m4a`, `aac`, `flac`
- Max size: 500 MB
- Used for: Points (e.g., audio guides)

### Videos
- Formats: `mp4`, `avi`, `mov`, `mkv`, `webm`, `flv`, `wmv`
- Max size: 500 MB
- Used for: Excursions, Points

### Documents
- Formats: `pdf`, `txt`, `doc`, `docx`, `xls`, `xlsx`
- Max size: 500 MB
- Used for: General storage

## API Endpoints

### General Media Upload
```
POST /api/media/upload
```

**Parameters:**
- `file` (UploadFile, required): The file to upload
- `media_type` (string): Type of media - `images`, `audio`, `videos`, or `documents`

**Example:**
```bash
curl -X POST "http://localhost:8000/api/media/upload" \
  -F "file=@image.jpg" \
  -F "media_type=images"
```

**Response:**
```json
{
  "path": "media/images/image.jpg",
  "message": "File uploaded successfully to media/images/image.jpg"
}
```

### Upload City Media
```
POST /api/media/upload-city
```

**Parameters:**
- `city_id` (integer, required): ID of the city
- `file` (UploadFile, required): Image file

**Example:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-city?city_id=1" \
  -F "file=@paris.jpg"
```

**Response:**
```json
{
  "path": "media/images/city_1_paris.jpg",
  "message": "City image uploaded successfully"
}
```

### Upload Excursion Media
```
POST /api/media/upload-excursion
```

**Parameters:**
- `excursion_id` (integer, required): ID of the excursion
- `file` (UploadFile, required): Image or video file
- `media_type` (string): `images` or `videos`

**Example - Image:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-excursion?excursion_id=1&media_type=images" \
  -F "file=@tour.jpg"
```

**Example - Video:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-excursion?excursion_id=1&media_type=videos" \
  -F "file=@tour.mp4"
```

### Upload Point Media
```
POST /api/media/upload-point
```

**Parameters:**
- `point_id` (integer, required): ID of the point
- `file` (UploadFile, required): Image, audio, or video file
- `media_type` (string): `images`, `audio`, or `videos`

**Example - Audio:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-point?point_id=1&media_type=audio" \
  -F "file=@guide.mp3"
```

**Example - Image:**
```bash
curl -X POST "http://localhost:8000/api/media/upload-point?point_id=1&media_type=images" \
  -F "file=@landmark.jpg"
```

## Using the Admin Panel

### Adding Media to Cities

1. Go to Admin Panel → Cities
2. Click "Edit" on a city
3. Fill in the city name and image path:
   - You can manually enter: `media/images/city_name.jpg`
   - Or use the API to upload and get the path

### Adding Media to Excursions

1. Go to Admin Panel → Excursions
2. Click "Edit" on an excursion
3. Fill in:
   - Title and description
   - Image path: `media/images/excursion_name.jpg`
   - Video path (optional): `media/videos/excursion_name.mp4`

### Adding Media to Points

1. Go to Admin Panel → Excursion Points
2. Click "Edit" on a point
3. Fill in:
   - Title, description, coordinates
   - Image path: `media/images/point_name.jpg`
   - Audio path: `media/audio/point_guide.mp3`
   - Video path (optional): `media/videos/point_name.mp4`

## File Organization

Files are automatically organized in the following structure:
```
/media
├── images/
│   ├── city_1_paris.jpg
│   ├── excursion_1_tour.jpg
│   └── point_1_landmark.jpg
├── audio/
│   ├── point_1_guide.mp3
│   └── point_2_description.mp3
├── videos/
│   ├── excursion_1_intro.mp4
│   └── point_1_demo.mp4
└── documents/
    └── tour_guide.pdf
```

## Accessing Media

Once uploaded, media files can be accessed at:
```
http://localhost:8000/media/images/city_1_paris.jpg
http://localhost:8000/media/audio/point_1_guide.mp3
http://localhost:8000/media/videos/excursion_1_intro.mp4
```

## Best Practices

1. **File Naming**: Use descriptive names without special characters
2. **File Size**: Keep files under 500 MB (images < 5 MB recommended)
3. **Formats**:
   - Images: Use PNG/WebP for quality, JPEG for smaller files
   - Audio: MP3 is most compatible
   - Video: MP4 is most compatible
4. **Organization**: Use the entity-specific upload endpoints to auto-organize files

## Database Models Updated

### City
- `id`: Integer (Primary Key)
- `name`: String
- `image`: String (path to image file)

### Excursion
- `id`: Integer (Primary Key)
- `city_id`: Integer (Foreign Key)
- `title`: String
- `description`: Text
- `image`: String (path to image file)
- `video`: String (path to video file)

### Point
- `id`: Integer (Primary Key)
- `excursion_id`: Integer (Foreign Key)
- `order`: Integer
- `title`: String
- `text`: Text
- `lat`: Float
- `lng`: Float
- `audio`: String (path to audio file)
- `image`: String (path to image file)
- `video`: String (path to video file)

## Error Handling

The API returns descriptive error messages:

```json
{
  "detail": "File extension 'exe' not allowed. Allowed: jpg, jpeg, png, gif, webp, bmp"
}
```

Common errors:
- **400**: Invalid file type, file too large, or unsupported format
- **404**: City, excursion, or point not found
- **500**: Server error during file save

## Python Usage Example

```python
import aiohttp
import asyncio

async def upload_city_image(city_id: int, file_path: str):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('file', f)
            
            async with session.post(
                f'http://localhost:8000/api/media/upload-city?city_id={city_id}',
                data=data
            ) as resp:
                return await resp.json()

# Usage
result = asyncio.run(upload_city_image(1, 'paris.jpg'))
print(result['path'])  # Output: media/images/city_1_paris.jpg
```

## Configuration

Media settings are in `web/media.py`:

```python
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB

ALLOWED_EXTENSIONS = {
    "images": {"jpg", "jpeg", "png", "gif", "webp", "bmp"},
    "audio": {"mp3", "wav", "ogg", "m4a", "aac", "flac"},
    "videos": {"mp4", "avi", "mov", "mkv", "webm", "flv", "wmv"},
    "documents": {"pdf", "txt", "doc", "docx", "xls", "xlsx"},
}
```

Modify these as needed for your use case.
