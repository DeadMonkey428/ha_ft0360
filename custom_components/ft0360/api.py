"""API client for FT0360 Weather Station."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from .const import ENDPOINT_ABOUT, ENDPOINT_RECORD

_LOGGER = logging.getLogger(__name__)


class FT0360ApiError(Exception):
    """Raised when the FT0360 API cannot be reached or parsed."""


class FT0360Client:
    """Small async client for the local FT0360 HTTP API."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        self.host = host.strip().replace("http://", "").replace("https://", "").rstrip("/")
        self._session = session

    @property
    def base_url(self) -> str:
        """Return the base URL."""
        return f"http://{self.host}"

    async def _get_json(self, endpoint: str) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)
                if not isinstance(data, dict):
                    raise FT0360ApiError(
                        f"Unexpected response type from {url}: expected dict, got {type(data).__name__}"
                    )
                _LOGGER.debug("Got response from %s: %s", url, data)
                return data
        except FT0360ApiError:
            raise
        except asyncio.TimeoutError as err:
            raise FT0360ApiError(f"Timeout connecting to {url} after 10s") from err
        except aiohttp.ClientConnectorError as err:
            raise FT0360ApiError(f"Cannot connect to {self.host}: {err}") from err
        except aiohttp.ClientResponseError as err:
            raise FT0360ApiError(f"HTTP {err.status} error from {url}") from err
        except aiohttp.ClientError as err:
            raise FT0360ApiError(f"Connection error: {err}") from err
        except ValueError as err:
            raise FT0360ApiError(f"Invalid JSON from {url}: {err}") from err

    async def async_get_record(self) -> dict[str, Any]:
        """Fetch live sensor data."""
        return await self._get_json(ENDPOINT_RECORD)

    async def async_get_about(self) -> dict[str, Any]:
        """Fetch device information."""
        return await self._get_json(ENDPOINT_ABOUT)

    async def async_validate(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Validate the station and return about + record payloads."""
        about = await self.async_get_about()
        record = await self.async_get_record()
        if "Sensor" not in record:
            raise FT0360ApiError(
                f"Missing 'Sensor' key in record response. Got keys: {list(record.keys())}"
            )
        return about, record
