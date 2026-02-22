import os
from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from utils.logger import setup_logger

logger = setup_logger('web_auth')

class AdminAuth(AuthenticationBackend):
    """Admin authentication backend"""
    
    async def login(self, request: Request) -> bool:
        try:
            form = await request.form()
            username = form.get("username", "").strip()
            password = form.get("password", "")
            
            admin_username = os.getenv("ADMIN_USERNAME", "admin")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
            
            logger.info(f"Login attempt: username={username}")
            
            if username == admin_username and password == admin_password:
                request.session["token"] = "authenticated"
                logger.info(f"Login successful for user: {username}")
                return True
            else:
                logger.warning(f"Login failed for user: {username}")
                return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated"""
        token = request.session.get("token")
        authenticated = token == "authenticated"
        logger.debug(f"Authentication check: authenticated={authenticated}")
        return authenticated

