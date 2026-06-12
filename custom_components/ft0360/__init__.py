"""FT0360 Weather Station integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import FT0360ApiError, FT0360Client
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

type FT0360ConfigEntry = ConfigEntry[DataUpdateCoordinator[dict[str, Any]]]


async def async_setup_entry(hass: HomeAssistant, entry: FT0360ConfigEntry) -> bool:
    """Set up FT0360 from a config entry."""
    host = entry.data[CONF_HOST]
    session = async_get_clientsession(hass)
    client = FT0360Client(host, session)

    async def async_update_data() -> dict[str, Any]:
        try:
            record, about = await asyncio.gather(
                client.async_get_record(),
                client.async_get_about(),
            )
        except FT0360ApiError as err:
            raise UpdateFailed(str(err)) from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching FT0360 data from %s", host)
            raise UpdateFailed(f"{type(err).__name__}: {err}") from err
        return {"record": record, "about": about, "host": host}

    interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    coordinator: DataUpdateCoordinator[dict[str, Any]] = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=int(interval)),
        config_entry=entry,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: FT0360ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: FT0360ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
