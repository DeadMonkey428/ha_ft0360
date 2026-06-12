"""Shared helpers for FT0360 entities."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo, format_mac
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, MANUFACTURER, MODEL


def device_info_from_coordinator(
    coordinator: DataUpdateCoordinator[dict[str, Any]], entry: ConfigEntry
) -> DeviceInfo:
    """Return shared device information."""
    data = coordinator.data or {}
    about = data.get("about", {})
    host = data.get("host", entry.data[CONF_HOST])
    raw_mac = about.get("MAC")
    # Keep the historical identifier format for device-registry stability.
    identifier = str(raw_mac or entry.unique_id or entry.entry_id).lower()
    connections = {(CONNECTION_NETWORK_MAC, format_mac(raw_mac))} if raw_mac else set()

    return DeviceInfo(
        identifiers={(DOMAIN, identifier)},
        connections=connections,
        name="FT0360 Wetterstation",
        manufacturer=MANUFACTURER,
        model=MODEL,
        sw_version=about.get("Version"),
        configuration_url=f"http://{host}",
    )
