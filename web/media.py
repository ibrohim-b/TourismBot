"""
Media file upload and management utilities
"""
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from fastapi import UploadFile, HTTPException
from typing import Optional, Tuple
from utils.logger import setup_logger

logger = setup_logger('web_media')

# Get root directory
ROOT_DIR = Path(__file__).parent.parent

# Media directories
MEDIA_DIR = ROOT_DIR / "media"
IMAGES_DIR = MEDIA_DIR / "images"
AUDIO_DIR = MEDIA_DIR / "audio"
VIDEOS_DIR = MEDIA_DIR / "videos"
DOCUMENTS_DIR = MEDIA_DIR / "documents"

# Create directories if they don't exist
for directory in [IMAGES_DIR, AUDIO_DIR, VIDEOS_DIR, DOCUMENTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    "images": {"jpg", "jpeg", "png", "gif", "webp", "bmp"},
    "audio": {"mp3", "wav", "ogg", "m4a", "aac", "flac"},
    "videos": {"mp4", "avi", "mov", "mkv", "webm", "flv", "wmv"},
    "documents": {"pdf", "txt", "doc", "docx", "xls", "xlsx"},
}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB


def get_file_extension(filename: str) -> str:
    """Get file extension without the dot"""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def validate_file(filename: str, file_type: str) -> bool:
    """Validate if file is allowed"""
    if file_type not in ALLOWED_EXTENSIONS:
        return False
    ext = get_file_extension(filename)
    return ext in ALLOWED_EXTENSIONS[file_type]


async def save_upload_file(
    upload_file: UploadFile, file_type: str, prefix: str = ""
) -> Tuple[str, Optional[str]]:
    """
    Save uploaded file and return the relative path
    
    Args:
        upload_file: FastAPI UploadFile object
        file_type: Type of file (images, audio, videos, documents)
        prefix: Optional prefix for filename (e.g., "city_", "excursion_")
    
    Returns:
        Tuple of (relative_path, error_message)
        If successful: ("media/type/filename", None)
        If error: (None, error_message)
    """
    
    logger.info(f"Saving {file_type} file: {upload_file.filename} with prefix: {prefix}")
    
    if file_type not in ALLOWED_EXTENSIONS:
        return None, f"Invalid file type: {file_type}"
    
    if not upload_file.filename:
        return None, "No filename provided"
    
    # Validate file extension
    if not validate_file(upload_file.filename, file_type):
        ext = get_file_extension(upload_file.filename)
        allowed = ", ".join(ALLOWED_EXTENSIONS[file_type])
        return None, f"File extension '{ext}' not allowed. Allowed: {allowed}"
    
    # Validate file size
    file_content = await upload_file.read()
    if len(file_content) > MAX_FILE_SIZE:
        return None, f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.0f} MB"
    
    # Secure filename and add prefix
    original_name = secure_filename(upload_file.filename)
    name_without_ext = Path(original_name).stem
    ext = get_file_extension(original_name)
    
    # Create unique filename with prefix
    final_filename = f"{prefix}{name_without_ext}.{ext}" if prefix else original_name
    
    # Ensure uniqueness
    target_dir = MEDIA_DIR / file_type
    target_path = target_dir / final_filename
    counter = 1
    while target_path.exists():
        name_part = f"{prefix}{name_without_ext}" if prefix else name_without_ext
        final_filename = f"{name_part}_{counter}.{ext}"
        target_path = target_dir / final_filename
        counter += 1
    
    try:
        # Save file
        with open(target_path, "wb") as f:
            f.write(file_content)
        
        # Return relative path for storage in database
        relative_path = f"media/{file_type}/{final_filename}"
        logger.info(f"File saved successfully: {relative_path}")
        return relative_path, None
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return None, f"Error saving file: {str(e)}"


async def delete_media_file(file_path: str) -> Optional[str]:
    """
    Delete a media file
    
    Args:
        file_path: Relative path to file (e.g., "media/images/city_123.jpg")
    
    Returns:
        Error message if failed, None if successful
    """
    try:
        full_path = ROOT_DIR / file_path
        if full_path.exists() and full_path.is_file():
            os.remove(full_path)
            return None
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error deleting file: {str(e)}"


def get_media_url(file_path: Optional[str]) -> Optional[str]:
    """
    Convert file path to URL
    
    Args:
        file_path: Relative path (e.g., "media/images/city_123.jpg")
    
    Returns:
        URL path for accessing the file
    """
    if not file_path:
        return None
    return f"/{file_path}"
