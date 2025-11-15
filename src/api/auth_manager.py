import requests
import base64
from datetime import datetime, timedelta
from typing import Optional
from threading import Lock
import logging

logger = logging.getLogger(__name__)


class OnceAuthManager:
    """Manages authentication for 1NCE API with automatic token refresh"""

    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url

        # Token management
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._lock = Lock()

        # Buffer time before expiry to refresh token (5 minutes)
        self.refresh_buffer = timedelta(minutes=5)

    def _get_basic_auth_header(self) -> str:
        """Create Basic Authentication header"""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _obtain_token(self) -> dict:
        """Obtain a new access token from 1NCE API"""
        url = f"{self.base_url}/oauth/token"

        headers = {
            "Authorization": self._get_basic_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {"grant_type": "client_credentials"}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

            token_data = response.json()
            logger.info("Successfully obtained new access token")
            return token_data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json()
                error_msg = error_data.get('message', 'Unknown error')
                logger.error(f"Authentication failed: {error_msg}")
                raise Exception(f"1NCE Authentication Error: {error_msg}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to obtain token: {e}")
            raise

    def _is_token_valid(self) -> bool:
        """Check if current token is valid and not about to expire"""
        if not self._access_token or not self._token_expires_at:
            return False

        return datetime.now() < (self._token_expires_at - self.refresh_buffer)

    def get_token(self) -> str:
        """Get valid access token, refreshing if necessary"""
        with self._lock:
            if self._is_token_valid():
                return self._access_token

            logger.info("Token expired or missing, obtaining new token...")
            token_data = self._obtain_token()

            self._access_token = token_data['access_token']
            expires_in = token_data.get('expires_in', 3600)
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            logger.info(f"New token obtained, expires at {self._token_expires_at}")
            return self._access_token

    def get_auth_headers(self) -> dict:
        """Get headers with valid Bearer token"""
        token = self.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def invalidate_token(self):
        """Force token refresh on next request"""
        with self._lock:
            self._access_token = None
            self._token_expires_at = None
            logger.info("Token invalidated")
