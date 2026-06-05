"""Config flow for FT0360 Weather Station."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import NumberSelector, NumberSelectorConfig, NumberSelectorMode

from .api import FT0360ApiError, FT0360Client
from .const import (
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

CONF_UPDATE_INTERVAL_FIELD = "update_interval"


def _host_schema(default_host: str | None = None, default_interval: int = DEFAULT_SCAN_INTERVAL) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=default_host or ""): str,
            vol.Required(CONF_UPDATE_INTERVAL_FIELD, default=default_interval): NumberSelector(
                NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=1,
                    mode=NumberSelectorMode.BOX,
                    unit_of_measurement="s",
                )
            ),
        }
    )


def _options_schema(default_interval: int = DEFAULT_SCAN_INTERVAL) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_UPDATE_INTERVAL_FIELD, default=default_interval): NumberSelector(
                NumberSelectorConfig(
                    min=MIN_SCAN_INTERVAL,
                    max=MAX_SCAN_INTERVAL,
                    step=1,
                    mode=NumberSelectorMode.BOX,
                    unit_of_measurement="s",
                )
            ),
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FT0360."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return FT0360OptionsFlowHandler(config_entry)

    async def _async_validate_and_connect(
        self, host: str
    ) -> tuple[dict[str, Any], dict[str, str]]:
        """Validate connection and return (about, errors)."""
        errors: dict[str, str] = {}
        session = async_get_clientsession(self.hass)
        client = FT0360Client(host, session)
        try:
            about, _record = await client.async_validate()
        except (FT0360ApiError, aiohttp.ClientError) as err:
            _LOGGER.debug("Unable to connect to FT0360 at %s: %s", host, err)
            errors["base"] = "cannot_connect"
            about = {}
        except Exception:  # noqa: BLE001
            _LOGGER.exception("Unexpected error while connecting to FT0360 at %s", host)
            errors["base"] = "unknown"
            about = {}
        return about, errors

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = str(user_input[CONF_HOST]).strip().replace("http://", "").replace("https://", "").rstrip("/")
            scan_interval = int(user_input[CONF_UPDATE_INTERVAL_FIELD])
            about, errors = await self._async_validate_and_connect(host)
            if not errors:
                mac = about.get("MAC") or host
                await self.async_set_unique_id(str(mac).lower())
                self._abort_if_unique_id_configured(updates={CONF_HOST: host})
                return self.async_create_entry(
                    title=f"FT0360 {host}",
                    data={CONF_HOST: host, CONF_SCAN_INTERVAL: scan_interval},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_host_schema(),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Handle reconfiguration (change host/IP)."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        errors: dict[str, str] = {}

        if user_input is not None:
            host = str(user_input[CONF_HOST]).strip().replace("http://", "").replace("https://", "").rstrip("/")
            scan_interval = int(user_input[CONF_UPDATE_INTERVAL_FIELD])
            about, errors = await self._async_validate_and_connect(host)
            if not errors:
                return self.async_update_reload_and_abort(
                    entry,
                    title=f"FT0360 {host}",
                    data={CONF_HOST: host, CONF_SCAN_INTERVAL: scan_interval},
                    reason="reconfigure_successful",
                )

        current_host = entry.data.get(CONF_HOST, "")
        current_interval = entry.options.get(
            CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_host_schema(current_host, int(current_interval)),
            errors=errors,
        )


class FT0360OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle FT0360 options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={CONF_SCAN_INTERVAL: int(user_input[CONF_UPDATE_INTERVAL_FIELD])},
            )

        current_interval = self._config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self._config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(int(current_interval)),
        )
