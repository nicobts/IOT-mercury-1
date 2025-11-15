import requests
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timedelta

from src.api.auth_manager import OnceAuthManager
from src.config import config

logger = logging.getLogger(__name__)


class OnceAPIClient:
    """Complete 1NCE API client with automatic authentication"""

    def __init__(self):
        self.auth_manager = OnceAuthManager(
            username=config.ONENCE_USERNAME,
            password=config.ONENCE_PASSWORD,
            base_url=config.ONENCE_API_BASE_URL
        )
        self.base_url = config.ONENCE_API_BASE_URL
        self.session = requests.Session()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make authenticated request with automatic retry on auth failure"""
        url = f"{self.base_url}{endpoint}"
        headers = self.auth_manager.get_auth_headers()

        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        try:
            response = self.session.request(
                method, url, headers=headers, timeout=30, **kwargs
            )

            # Handle 401 Unauthorized
            if response.status_code == 401:
                logger.warning("Received 401, invalidating token and retrying...")
                self.auth_manager.invalidate_token()
                headers = self.auth_manager.get_auth_headers()
                response = self.session.request(
                    method, url, headers=headers, timeout=30, **kwargs
                )

            response.raise_for_status()
            return response.json() if response.text else {}

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    # ===== SIM Management Methods =====

    def get_all_sims(self) -> Dict[str, Any]:
        """Get all SIMs"""
        return self._make_request('GET', '/v1/sims')

    def get_sim(self, iccid: str) -> Dict[str, Any]:
        """Get single SIM details"""
        return self._make_request('GET', f'/v1/sims/{iccid}')

    def get_sim_status(self, iccid: str) -> Dict[str, Any]:
        """Get SIM status"""
        return self._make_request('GET', f'/v1/sims/{iccid}/status')

    def get_sim_usage(
        self,
        iccid: str,
        start_date: str,
        end_date: str
    ) -> Dict[str, Any]:
        """Get SIM usage for date range (YYYY-MM-DD)"""
        params = {'start_dt': start_date, 'end_dt': end_date}
        return self._make_request('GET', f'/v1/sims/{iccid}/usage', params=params)

    def get_sim_connectivity(
        self,
        iccid: str,
        subscriber: bool = True,
        ussd: bool = False
    ) -> Dict[str, Any]:
        """Get SIM connectivity information"""
        params = {'subscriber': subscriber, 'ussd': ussd}
        return self._make_request(
            'GET',
            f'/v1/sims/{iccid}/connectivity_info',
            params=params
        )

    def get_sim_data_quota(self, iccid: str) -> Dict[str, Any]:
        """Get SIM data quota"""
        return self._make_request('GET', f'/v1/sims/{iccid}/quota/data')

    def get_sim_sms_quota(self, iccid: str) -> Dict[str, Any]:
        """Get SIM SMS quota"""
        return self._make_request('GET', f'/v1/sims/{iccid}/quota/sms')

    def get_sim_events(self, iccid: str) -> Dict[str, Any]:
        """Get SIM events"""
        return self._make_request('GET', f'/v1/sims/{iccid}/events')

    # Bulk operations
    def get_usage_for_multiple_sims(
        self,
        iccids: list,
        start_date: str,
        end_date: str
    ) -> Dict[str, Dict[str, Any]]:
        """Get usage for multiple SIMs"""
        results = {}
        for iccid in iccids:
            try:
                results[iccid] = self.get_sim_usage(iccid, start_date, end_date)
            except Exception as e:
                logger.error(f"Failed to get usage for {iccid}: {e}")
                results[iccid] = {"error": str(e)}
        return results

    # SIM Management Operations
    def update_sim_label(self, iccid: str, label: str) -> Dict[str, Any]:
        """Update SIM card label"""
        payload = {"label": label}
        return self._make_request('PATCH', f'/v1/sims/{iccid}', json=payload)

    def enable_sim(self, iccid: str) -> Dict[str, Any]:
        """Enable SIM card"""
        return self._make_request('POST', f'/v1/sims/{iccid}/enable')

    def disable_sim(self, iccid: str) -> Dict[str, Any]:
        """Disable SIM card"""
        return self._make_request('POST', f'/v1/sims/{iccid}/disable')

    def set_imei_lock(self, iccid: str, imei: str) -> Dict[str, Any]:
        """Set IMEI lock for SIM"""
        payload = {"imei": imei}
        return self._make_request('POST', f'/v1/sims/{iccid}/imei_lock', json=payload)

    def remove_imei_lock(self, iccid: str) -> Dict[str, Any]:
        """Remove IMEI lock from SIM"""
        return self._make_request('DELETE', f'/v1/sims/{iccid}/imei_lock')
