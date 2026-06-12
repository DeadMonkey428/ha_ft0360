"""Diagnostics support for FT0360 Weather Station."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import FT0360ConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: FT0360ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    data = coordinator.data or {}
    about = dict(data.get("about", {}))
    if "MAC" in about:
        about["MAC"] = "**REDACTED**"

    return {
        "entry": {
            "title": entry.title,
            "data_keys": sorted(entry.data.keys()),
            "options": dict(entry.options),
        },
        "about": about,
        "record": data.get("record", {}),
    }
