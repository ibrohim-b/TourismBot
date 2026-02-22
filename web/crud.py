"""
CRUD API routes for managing cities, excursions, and points
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import List, Optional

from db.session import get_async_session
from db.models import City, Excursion, Point
from web.media import save_upload_file, delete_media_file
from utils.logger import setup_logger

logger = setup_logger('web_crud')
router = APIRouter()

# Pydantic models for request/response
class CityCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)

class CityResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class ExcursionCreate(BaseModel):
    city_id: int
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)

class ExcursionUpdate(BaseModel):
    city_id: Optional[int] = None
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)

class ExcursionResponse(BaseModel):
    id: int
    city_id: int
    title: str
    description: str
    
    class Config:
        from_attributes = True

class PointCreate(BaseModel):
    excursion_id: int
    order: int = Field(..., ge=1, le=100)
    title: str = Field(..., min_length=3, max_length=200)
    text: str = Field(..., min_length=10, max_length=2000)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    audio: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None, max_length=255)

class PointUpdate(BaseModel):
    excursion_id: Optional[int] = None
    order: Optional[int] = Field(None, ge=1, le=100)
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    text: Optional[str] = Field(None, min_length=10, max_length=2000)
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    audio: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None, max_length=255)

class PointResponse(BaseModel):
    id: int
    excursion_id: int
    order: int
    title: str
    text: str
    lat: float
    lng: float
    audio: Optional[str] = None
    image: Optional[str] = None
    
    class Config:
        from_attributes = True

# City CRUD endpoints
@router.get("/cities", response_model=List[CityResponse])
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    """Get all cities"""
    result = await session.execute(select(City))
    cities = result.scalars().all()
    return cities

@router.post("/cities", response_model=CityResponse)
async def create_city(city: CityCreate, session: AsyncSession = Depends(get_async_session)):
    """Create a new city"""
    logger.info(f"Creating city: {city.name}")
    db_city = City(name=city.name)
    session.add(db_city)
    await session.commit()
    await session.refresh(db_city)
    logger.info(f"City created with id: {db_city.id}")
    return db_city

@router.get("/cities/{city_id}", response_model=CityResponse)
async def get_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get a specific city by ID"""
    result = await session.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.put("/cities/{city_id}", response_model=CityResponse)
async def update_city(city_id: int, city: CityUpdate, session: AsyncSession = Depends(get_async_session)):
    """Update a city"""
    result = await session.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    if city.name is not None:
        db_city.name = city.name
    
    await session.commit()
    await session.refresh(db_city)
    return db_city

@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete a city"""
    logger.info(f"Deleting city: {city_id}")
    result = await session.execute(select(City).where(City.id == city_id))
    db_city = result.scalar_one_or_none()
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")
    
    await session.delete(db_city)
    await session.commit()
    logger.info(f"City {city_id} deleted")
    return {"message": "City deleted successfully"}

# Excursion CRUD endpoints
@router.get("/excursions", response_model=List[ExcursionResponse])
async def get_excursions(city_id: Optional[int] = None, session: AsyncSession = Depends(get_async_session)):
    """Get all excursions, optionally filtered by city"""
    query = select(Excursion)
    if city_id:
        query = query.where(Excursion.city_id == city_id)
    result = await session.execute(query)
    excursions = result.scalars().all()
    return excursions

@router.post("/excursions", response_model=ExcursionResponse)
async def create_excursion(excursion: ExcursionCreate, session: AsyncSession = Depends(get_async_session)):
    """Create a new excursion"""
    # Verify city exists
    city_result = await session.execute(select(City).where(City.id == excursion.city_id))
    if not city_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="City not found")
    
    db_excursion = Excursion(
        city_id=excursion.city_id,
        title=excursion.title,
        description=excursion.description
    )
    session.add(db_excursion)
    await session.commit()
    await session.refresh(db_excursion)
    return db_excursion

@router.get("/excursions/{excursion_id}", response_model=ExcursionResponse)
async def get_excursion(excursion_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get a specific excursion by ID"""
    result = await session.execute(select(Excursion).where(Excursion.id == excursion_id))
    excursion = result.scalar_one_or_none()
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    return excursion

@router.put("/excursions/{excursion_id}", response_model=ExcursionResponse)
async def update_excursion(excursion_id: int, excursion: ExcursionUpdate, session: AsyncSession = Depends(get_async_session)):
    """Update an excursion"""
    result = await session.execute(select(Excursion).where(Excursion.id == excursion_id))
    db_excursion = result.scalar_one_or_none()
    if not db_excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    
    if excursion.city_id is not None:
        # Verify city exists
        city_result = await session.execute(select(City).where(City.id == excursion.city_id))
        if not city_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="City not found")
        db_excursion.city_id = excursion.city_id
    
    if excursion.title is not None:
        db_excursion.title = excursion.title
    if excursion.description is not None:
        db_excursion.description = excursion.description
    
    await session.commit()
    await session.refresh(db_excursion)
    return db_excursion

@router.delete("/excursions/{excursion_id}")
async def delete_excursion(excursion_id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete an excursion"""
    result = await session.execute(select(Excursion).where(Excursion.id == excursion_id))
    db_excursion = result.scalar_one_or_none()
    if not db_excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    
    await session.delete(db_excursion)
    await session.commit()
    return {"message": "Excursion deleted successfully"}

# Point CRUD endpoints
@router.get("/points", response_model=List[PointResponse])
async def get_points(excursion_id: Optional[int] = None, session: AsyncSession = Depends(get_async_session)):
    """Get all points, optionally filtered by excursion"""
    query = select(Point).order_by(Point.order)
    if excursion_id:
        query = query.where(Point.excursion_id == excursion_id)
    result = await session.execute(query)
    points = result.scalars().all()
    return points

@router.post("/points", response_model=PointResponse)
async def create_point(point: PointCreate, session: AsyncSession = Depends(get_async_session)):
    """Create a new excursion point"""
    # Verify excursion exists
    exc_result = await session.execute(select(Excursion).where(Excursion.id == point.excursion_id))
    if not exc_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Excursion not found")
    
    db_point = Point(
        excursion_id=point.excursion_id,
        order=point.order,
        title=point.title,
        text=point.text,
        lat=point.lat,
        lng=point.lng,
        audio=point.audio,
        image=point.image
    )
    session.add(db_point)
    await session.commit()
    await session.refresh(db_point)
    return db_point

@router.get("/points/{point_id}", response_model=PointResponse)
async def get_point(point_id: int, session: AsyncSession = Depends(get_async_session)):
    """Get a specific point by ID"""
    result = await session.execute(select(Point).where(Point.id == point_id))
    point = result.scalar_one_or_none()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")
    return point

@router.put("/points/{point_id}", response_model=PointResponse)
async def update_point(point_id: int, point: PointUpdate, session: AsyncSession = Depends(get_async_session)):
    """Update a point"""
    result = await session.execute(select(Point).where(Point.id == point_id))
    db_point = result.scalar_one_or_none()
    if not db_point:
        raise HTTPException(status_code=404, detail="Point not found")
    
    if point.excursion_id is not None:
        # Verify excursion exists
        exc_result = await session.execute(select(Excursion).where(Excursion.id == point.excursion_id))
        if not exc_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Excursion not found")
        db_point.excursion_id = point.excursion_id
    
    if point.order is not None:
        db_point.order = point.order
    if point.title is not None:
        db_point.title = point.title
    if point.text is not None:
        db_point.text = point.text
    if point.lat is not None:
        db_point.lat = point.lat
    if point.lng is not None:
        db_point.lng = point.lng
    if point.audio is not None:
        db_point.audio = point.audio
    if point.image is not None:
        db_point.image = point.image
    
    await session.commit()
    await session.refresh(db_point)
    return db_point

@router.delete("/points/{point_id}")
async def delete_point(point_id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete a point"""
    result = await session.execute(select(Point).where(Point.id == point_id))
    db_point = result.scalar_one_or_none()
    if not db_point:
        raise HTTPException(status_code=404, detail="Point not found")
    
    await session.delete(db_point)
    await session.commit()
    return {"message": "Point deleted successfully"}

# Media Upload endpoints
class MediaResponse(BaseModel):
    path: str
    message: str


@router.post("/media/upload")
async def upload_media(
    file: UploadFile = File(...),
    media_type: str = "images"
) -> MediaResponse:
    """
    Upload media file (image, audio, video, etc.)
    
    Supported types:
    - images: jpg, jpeg, png, gif, webp, bmp
    - audio: mp3, wav, ogg, m4a, aac, flac
    - videos: mp4, avi, mov, mkv, webm, flv, wmv
    - documents: pdf, txt, doc, docx, xls, xlsx
    """
    logger.info(f"Uploading {media_type} file: {file.filename}")
    if media_type not in ["images", "audio", "videos", "documents"]:
        raise HTTPException(status_code=400, detail="Invalid media type")
    
    path, error = await save_upload_file(file, media_type)
    
    if error:
        logger.error(f"Upload failed: {error}")
        raise HTTPException(status_code=400, detail=error)
    
    logger.info(f"File uploaded successfully: {path}")
    return MediaResponse(
        path=path,
        message=f"File uploaded successfully to {path}"
    )


@router.post("/media/upload-city")
async def upload_city_media(
    city_id: int,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)
) -> MediaResponse:
    """Upload media for a city"""
    # Verify city exists
    result = await session.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    path, error = await save_upload_file(file, "images", prefix=f"city_{city_id}_")
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Update city with image path
    city.image = path
    await session.commit()
    
    return MediaResponse(
        path=path,
        message=f"City image uploaded successfully"
    )


@router.post("/media/upload-excursion")
async def upload_excursion_media(
    excursion_id: int,
    file: UploadFile = File(...),
    media_type: str = "images",
    session: AsyncSession = Depends(get_async_session)
) -> MediaResponse:
    """Upload media for an excursion (image or video)"""
    if media_type not in ["images", "videos"]:
        raise HTTPException(status_code=400, detail="Only images or videos allowed for excursions")
    
    # Verify excursion exists
    result = await session.execute(select(Excursion).where(Excursion.id == excursion_id))
    excursion = result.scalar_one_or_none()
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")
    
    path, error = await save_upload_file(file, media_type, prefix=f"excursion_{excursion_id}_")
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Update excursion with media path
    if media_type == "images":
        excursion.image = path
    else:
        excursion.video = path
    
    await session.commit()
    
    return MediaResponse(
        path=path,
        message=f"Excursion {media_type} uploaded successfully"
    )


@router.post("/media/upload-point")
async def upload_point_media(
    point_id: int,
    file: UploadFile = File(...),
    media_type: str = "images",
    session: AsyncSession = Depends(get_async_session)
) -> MediaResponse:
    """Upload media for a point (image, audio, or video)"""
    if media_type not in ["images", "audio", "videos"]:
        raise HTTPException(status_code=400, detail="Only images, audio, or videos allowed for points")
    
    # Verify point exists
    result = await session.execute(select(Point).where(Point.id == point_id))
    point = result.scalar_one_or_none()
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")
    
    path, error = await save_upload_file(file, media_type, prefix=f"point_{point_id}_")
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    # Update point with media path
    if media_type == "images":
        point.image = path
    elif media_type == "audio":
        point.audio = path
    else:
        point.video = path
    
    await session.commit()
    
    return MediaResponse(
        path=path,
        message=f"Point {media_type} uploaded successfully"
    )