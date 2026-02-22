# Admin Panel Media Upload Guide

## Quick Start 🚀

The admin panel now has built-in drag-and-drop media upload! No more copying paths manually.

### How to Upload

#### 1. Navigate to Admin Panel
```
http://localhost:8000/admin
```

#### 2. Edit a City, Excursion, or Point

Click "Edit" on any item in the list.

#### 3. Find the Media Field
You'll see a styled upload area with:
- 📁 File input button
- Drag & drop zone
- Real-time preview
- Current file path

#### 4. Upload Your File

**Option A: Click Upload Button**
- Click "📁 Choose File or Drag & Drop"
- Select file from your computer
- Wait for upload to complete

**Option B: Drag & Drop**
- Drag file from your computer
- Drop onto the dashed border area
- Upload starts automatically

#### 5. View Preview
- ✅ Image preview displays immediately
- 🎵 Audio player appears for audio files
- 🎥 Video player appears for video files
- 📄 Download link appears for documents

#### 6. File Path Auto-Filled
- Path automatically filled in the form
- No manual copying needed!

#### 7. Save Changes
- Click "Save" to update the item
- Media file persists in database

---

## Features

### ✨ Visual Feedback
- **Drag highlight**: Border changes color when dragging
- **Upload progress**: Shows uploading indicator
- **Success message**: ✅ notification appears
- **Error handling**: ❌ Shows what went wrong

### 📺 Media Previews
- **Images**: Full-size preview
- **Audio**: Playable audio player
- **Video**: Playable video player
- **Documents**: Download link

### 🔄 Smart Path Handling
- Paths auto-generated with entity type
- Example: `media/images/city_1_paris.jpg`
- No manual file path entry needed

### 📁 Automatic Organization
Files stored in type-specific folders:
```
/media
├── images/      (Cities, Excursions, Points)
├── audio/       (Point audio guides)
├── videos/      (Excursion and Point videos)
└── documents/   (PDFs, docs, etc.)
```

---

## Upload by Entity Type

### 🏙️ Cities

**Field:** Image

**Supported Formats:** JPG, PNG, GIF, WebP, BMP

**Example:**
1. Go to Admin → Cities
2. Click Edit on a city
3. Drag image onto "Image" field
4. Image auto-uploaded and previewed
5. Click Save

### 🗺️ Excursions

**Fields:** 
- Image (preview picture)
- Video (promotional video)

**Image Formats:** JPG, PNG, GIF, WebP, BMP

**Video Formats:** MP4, AVI, MOV, MKV, WebM, FLV, WMV

**Example:**
1. Go to Admin → Excursions
2. Click Edit on an excursion
3. Upload image to "Image" field
4. Upload video to "Video" field
5. Both previewed immediately
6. Click Save

### 📍 Points

**Fields:**
- Image (landmark photo)
- Audio (audio guide)
- Video (demonstration)

**Image Formats:** JPG, PNG, GIF, WebP, BMP

**Audio Formats:** MP3, WAV, OGG, M4A, AAC, FLAC

**Video Formats:** MP4, AVI, MOV, MKV, WebM, FLV, WMV

**Example:**
1. Go to Admin → Excursion Points
2. Click Edit on a point
3. Upload image, audio, and/or video
4. All previewed immediately
5. Click Save

---

## Advanced Features

### Manual Path Entry
If you already know the file path:
1. Click in the path field
2. Manually type path
3. Click Save

### Update Existing File
1. Click Edit on item
2. Upload new file
3. Old file replaced automatically
4. Click Save

### Remove File
1. Clear the path field
2. Click Save
3. Media field becomes empty

### File Limits
- Maximum file size: 500 MB
- Recommended sizes:
  - Images: < 5 MB
  - Audio: < 50 MB
  - Video: < 200 MB

---

## Troubleshooting

### Upload fails - "File type not allowed"
**Solution:** Check that file extension is in allowed list
- Images: .jpg, .png, .gif, .webp, .bmp
- Audio: .mp3, .wav, .ogg, .m4a, .aac, .flac
- Video: .mp4, .avi, .mov, .mkv, .webm, .flv, .wmv

### File size error
**Solution:** File is too large
- Compress before uploading
- Max size is 500 MB
- For images: compress to < 5 MB

### Preview doesn't show
**Solution:** File uploaded but preview not loading
- Refresh page
- Check that file path is correct
- Verify media directory exists

### Changes not saved
**Solution:** Upload completes but changes not saved
- Always click "Save" button after upload
- Don't navigate away before saving

### Upload very slow
**Solution:** Large file taking time
- Use smaller files (< 100 MB recommended)
- Check internet connection
- Wait for progress indicator to finish

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Focus upload field | Tab to field |
| Select file | Click or Space when focused |
| Submit form | Ctrl+Enter |

---

## Tips & Best Practices

### 🎨 For Images
1. Use web-friendly formats (PNG for quality, JPEG for size)
2. Optimize for web (resize to max 2000x2000 px)
3. Compress before uploading (< 5 MB recommended)

### 🎵 For Audio
1. Use MP3 format for best compatibility
2. Keep audio quality reasonable (128 kbps - 320 kbps)
3. Test audio playback after upload

### 🎥 For Videos
1. Use MP4 format for best compatibility
2. Use H.264 codec
3. Keep duration reasonable (< 10 min recommended)
4. Compress to 5-100 MB range

### 📝 File Naming
1. Use descriptive names (e.g., "eiffel_tower.jpg")
2. Avoid special characters
3. Use lowercase with underscores
4. Keep names concise (< 50 characters)

---

## Browser Support

Works on all modern browsers:
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

---

## What Happens During Upload

1. **Select File** → File chosen locally
2. **Validate** → Check size, type, format
3. **Upload** → File sent to server
4. **Save** → File stored on disk
5. **Database Update** → Path saved to database
6. **Preview** → File displayed in form
7. **Confirm** → Click Save to finalize

---

## Storage Location

All files stored in `/media` folder at project root:
```
/Users/ibrohim/PycharmProjects/TourismBot/
├── media/
│   ├── images/
│   │   ├── city_1_paris.jpg
│   │   └── excursion_2_eiffel.jpg
│   ├── audio/
│   │   └── point_3_guide.mp3
│   ├── videos/
│   │   └── excursion_1_intro.mp4
│   └── documents/
│       └── tour_guide.pdf
```

---

## API Alternative

If you prefer to use the API directly:

```bash
# Upload to point with audio
curl -X POST "http://localhost:8000/api/media/upload-point?point_id=1&media_type=audio" \
  -F "file=@guide.mp3"

# Response:
# {
#   "path": "media/audio/point_1_guide.mp3",
#   "message": "Point audio uploaded successfully"
# }
```

See [MEDIA_UPLOAD_GUIDE.md](MEDIA_UPLOAD_GUIDE.md) for full API documentation.

---

## Need Help?

1. **Check error message** - Usually indicates what went wrong
2. **Review format** - Ensure file format is supported
3. **Check file size** - Keep under 500 MB
4. **Clear cache** - Refresh browser (Ctrl+Shift+R)
5. **Test with HTML form** - Use [media_upload.html](media_upload.html) to test

Enjoy the enhanced admin panel! 🎉
