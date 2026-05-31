"""Shared helpers for FT0360 entities."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, MANUFACTURER, MODEL


def device_info_from_coordinator(
    coordinator: DataUpdateCoordinator[dict[str, Any]], entry: ConfigEntry
) -> dict[str, Any]:
    """Return shared device information."""
    data = coordinator.data or {}
    about = data.get("about", {})
    host = data.get("host", entry.data[CONF_HOST])
    mac = about.get("MAC") or entry.unique_id or entry.entry_id
    connections = {("mac", mac)} if about.get("MAC") else set()

    return {
        "identifiers": {(DOMAIN, str(mac).lower())},
        "connections": connections,
        "name": "FT0360 Wetterstation",
        "manufacturer": MANUFACTURER,
        "model": MODEL,
        "sw_version": about.get("Version"),
        "configuration_url": f"http://{host}",
    }
