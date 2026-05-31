"""API client for FT0360 Weather Station."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from .const import ENDPOINT_ABOUT, ENDPOINT_RECORD


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
                    raise FT0360ApiError(f"Unexpected response from {url}")
                return data
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as err:
            raise FT0360ApiError(f"{type(err).__name__}: {err}") from err

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
            raise FT0360ApiError("Missing Sensor data")
        return about, record
