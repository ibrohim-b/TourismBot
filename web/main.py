import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
from markupsafe import Markup

from db.base import Base
from db.session import async_engine, sync_engine, SyncSessionLocal
from web.admin import CityAdmin, ExcursionAdmin, PointAdmin
from web.auth import AdminAuth
from web.crud import router as crud_router
from web.media_admin import MEDIA_CSS, MEDIA_JS
from utils.logger import setup_logger

logger = setup_logger('web_main')

# Get root directory
ROOT_DIR = Path(__file__).parent.parent
MEDIA_DIR = ROOT_DIR / "media"

# Create media directories if they don't exist
MEDIA_DIR.mkdir(exist_ok=True)
(MEDIA_DIR / "images").mkdir(exist_ok=True)
(MEDIA_DIR / "audio").mkdir(exist_ok=True)
(MEDIA_DIR / "videos").mkdir(exist_ok=True)
(MEDIA_DIR / "documents").mkdir(exist_ok=True)

# Create app
app = FastAPI(
    title="Tourism Guide Admin Panel",
    description="Admin interface for managing cities, excursions, and points of interest",
    version="1.0.0",
    root_path="",
)

# Serve media files statically
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Add session middleware FIRST - this is critical for authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "SESSION_SECRET_KEY", "your-secret-key-here-change-in-production"
    ),
    max_age=3600,
)

# Create authentication backend
authentication_backend = AdminAuth(
    secret_key=os.getenv(
        "SESSION_SECRET_KEY", "your-secret-key-here-change-in-production"
    ),
)

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class InjectMediaAssetsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith('/admin/') and response.headers.get('content-type', '').startswith('text/html'):
            body = b''
            async for chunk in response.body_iterator:
                body += chunk
            body_str = body.decode('utf-8')
            if '</head>' in body_str:
                body_str = body_str.replace('</head>', MEDIA_CSS + '</head>')
            if '</body>' in body_str:
                body_str = body_str.replace('</body>', MEDIA_JS + '</body>')
            headers = dict(response.headers)
            headers['content-length'] = str(len(body_str.encode('utf-8')))
            return Response(content=body_str, status_code=response.status_code, headers=headers, media_type=response.media_type)
        return response

app.add_middleware(InjectMediaAssetsMiddleware)

# Create Admin with authentication using sync engine and sync sessionmaker
admin = Admin(
    app,
    engine=sync_engine,
    session_maker=SyncSessionLocal,
    authentication_backend=authentication_backend,
    title="Tourism Guide Admin",
    base_url="/admin",
)

admin.add_view(CityAdmin)
admin.add_view(ExcursionAdmin)
admin.add_view(PointAdmin)

# Include CRUD API routes
app.include_router(crud_router, prefix="/api", tags=["CRUD Operations"])


@app.get("/")
async def root():
    return RedirectResponse(url="/admin")


@app.on_event("startup")
async def startup():
    logger.info("Starting web application...")
    # Create all tables in the database using async engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")
