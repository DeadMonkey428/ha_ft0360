"""Binary sensor platform for FT0360 Weather Station."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from . import FT0360ConfigEntry
from .entity import device_info_from_coordinator

BATTERY_DESCRIPTION = BinarySensorEntityDescription(
    key="battery_low",
    translation_key="battery_low",
    device_class=BinarySensorDeviceClass.BATTERY,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FT0360ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FT0360 binary sensors."""
    coordinator = entry.runtime_data
    async_add_entities([FT0360BatteryLowBinarySensor(coordinator, entry)])


class FT0360BatteryLowBinarySensor(CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]], BinarySensorEntity):
    """Battery status for FT0360 sensors.

    Uses the HA BATTERY device class, where ``is_on`` means a battery
    *problem* (low/empty) — per Home Assistant convention.
    """

    _attr_has_entity_name = True
    entity_description = BATTERY_DESCRIPTION

    def __init__(self, coordinator: DataUpdateCoordinator[dict[str, Any]], entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_battery_low"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return device_info_from_coordinator(self.coordinator, self._entry)

    @property
    def is_on(self) -> bool | None:
        """Return True if any battery reports a problem (low/empty)."""
        try:
            values = self.coordinator.data["record"].get("battery", {}).get("list", [])
            if not values:
                return None
            text = " ".join(str(value).lower() for value in values)
            # BATTERY device class: on = problem. Faithful inverse of the
            # previous "all OK" check.
            return "ok" not in text or "low" in text or "bad" in text
        except (KeyError, TypeError):
            return None
