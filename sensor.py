"""Sensor platform for FT0360 Weather Station."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    DEGREE,
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN
from .entity import device_info_from_coordinator


@dataclass(frozen=True, kw_only=True)
class FT0360SensorDescription(SensorEntityDescription):
    """Describe an FT0360 sensor."""

    section: int
    item: int


SENSORS: tuple[FT0360SensorDescription, ...] = (
    FT0360SensorDescription(
        key="indoor_temperature",
        translation_key="indoor_temperature",
        section=0,
        item=0,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="indoor_humidity",
        translation_key="indoor_humidity",
        section=0,
        item=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="outdoor_temperature",
        translation_key="outdoor_temperature",
        section=1,
        item=0,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="outdoor_humidity",
        translation_key="outdoor_humidity",
        section=1,
        item=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="pressure_absolute",
        translation_key="pressure_absolute",
        section=2,
        item=0,
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="pressure_relative",
        translation_key="pressure_relative",
        section=2,
        item=1,
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="max_daily_gust",
        translation_key="max_daily_gust",
        section=3,
        item=0,
        native_unit_of_measurement="m/s",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_speed",
        translation_key="wind_speed",
        section=3,
        item=1,
        native_unit_of_measurement="m/s",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_gust",
        translation_key="wind_gust",
        section=3,
        item=2,
        native_unit_of_measurement="m/s",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_direction",
        translation_key="wind_direction",
        section=3,
        item=3,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_average_2_minute",
        translation_key="wind_average_2_minute",
        section=3,
        item=4,
        native_unit_of_measurement="m/s",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_direction_average_2_minute",
        translation_key="wind_direction_average_2_minute",
        section=3,
        item=5,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_average_10_minute",
        translation_key="wind_average_10_minute",
        section=3,
        item=6,
        native_unit_of_measurement="m/s",
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="wind_direction_average_10_minute",
        translation_key="wind_direction_average_10_minute",
        section=3,
        item=7,
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="rain_rate",
        translation_key="rain_rate",
        section=4,
        item=0,
        native_unit_of_measurement="mm/h",
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="rain_hour",
        translation_key="rain_hour",
        section=4,
        item=1,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="rain_day",
        translation_key="rain_day",
        section=4,
        item=2,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="rain_week",
        translation_key="rain_week",
        section=4,
        item=3,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="rain_month",
        translation_key="rain_month",
        section=4,
        item=4,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="rain_year",
        translation_key="rain_year",
        section=4,
        item=5,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="rain_total",
        translation_key="rain_total",
        section=4,
        item=6,
        native_unit_of_measurement="mm",
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.TOTAL,
    ),
    FT0360SensorDescription(
        key="solar_radiation",
        translation_key="solar_radiation",
        section=5,
        item=0,
        native_unit_of_measurement="W/m²",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    FT0360SensorDescription(
        key="uv_index",
        translation_key="uv_index",
        section=5,
        item=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FT0360 sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = [FT0360Sensor(coordinator, entry, description) for description in SENSORS]
    entities.append(FT0360WindDirectionTextSensor(coordinator, entry))
    async_add_entities(entities)



class FT0360Sensor(CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]], SensorEntity):
    """Representation of an FT0360 sensor."""

    _attr_has_entity_name = True
    entity_description: FT0360SensorDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator[dict[str, Any]],
        entry: ConfigEntry,
        description: FT0360SensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_{description.key}"
        self._entry = entry

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return device_info_from_coordinator(self.coordinator, self._entry)

    @property
    def native_value(self) -> float | None:
        """Return the sensor value."""
        try:
            value = self.coordinator.data["record"]["Sensor"][self.entity_description.section]["list"][self.entity_description.item][1]
            return float(value)
        except (KeyError, IndexError, TypeError, ValueError):
            return None


class FT0360WindDirectionTextSensor(CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]], SensorEntity):
    """Textual wind direction sensor."""

    _attr_has_entity_name = True
    _attr_translation_key = "wind_direction_text"

    def __init__(self, coordinator: DataUpdateCoordinator[dict[str, Any]], entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_wind_direction_text"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return device_info_from_coordinator(self.coordinator, self._entry)

    @property
    def native_value(self) -> str | None:
        """Return textual wind direction."""
        try:
            raw_value = self.coordinator.data["record"]["Sensor"][3]["list"][3][1]
            degrees = float(raw_value) % 360
        except (KeyError, IndexError, TypeError, ValueError):
            return None

        directions = ["N", "NO", "O", "SO", "S", "SW", "W", "NW"]
        index = int((degrees + 22.5) // 45) % 8
        return directions[index]
