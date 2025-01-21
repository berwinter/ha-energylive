"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
    RestoreSensor,
)
from homeassistant.util import slugify
from homeassistant.const import (
    EntityCategory,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import const
from homeassistant.helpers import device_registry as dr


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    device_registry = dr.async_get(hass)

    energylive = config_entry.runtime_data
    new_devices = []
    devices = await energylive.getDevices()
    for device in devices:
        await device.getDetails()
        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={(const.DOMAIN, device._id)},
            manufacturer="smartENERGY",
            name=device._id,
            model=const.DEVICE_TYPE_MAP[device._type],
            model_id=device._serial,
        )
        for measurement in device._measurements:
            match measurement:
                case const.CONST_ROOM_TEMPERATURE:
                    entity = TemperatureSensor(device, measurement)
                case const.CONST_ROOM_HUMIDITY:
                    entity = HumiditySensor(device, measurement)
                case const.CONST_BATTERY_VOLTAGE:
                    new_devices.append(BatterySensor(device, measurement))
                    entity = BatteryVoltageSensor(device, measurement)
                case const.CONST_CURRENT_POWER_CONSUMPTION:
                    entity = PowerSensor(device, measurement)
                case const.CONST_CURRENT_POWER_GENERATION:
                    entity = PowerSensor(device, measurement)
                case const.CONST_ENERGY_CONSUMPTION:
                    entity = EnergySensor(device, measurement)
                case const.CONST_ENERGY_GENERATION:
                    entity = EnergySensor(device, measurement)
                case const.CONST_ERROR_CODE:
                    entity = ErrorCodeSensor(device, measurement)
                case const.CONST_FREE_HEAP:
                    entity = FreeHeapSensor(device, measurement)
                case const.CONST_LARGEST_HEAP_BLOCK:
                    entity = LargestHeapBlockSensor(device, measurement)
                case const.CONST_LORA_RSSI:
                    entity = RssiSensor(device, measurement)
                case const.CONST_LORA_SNR:
                    entity = SnrSensor(device, measurement)
                case const.CONST_MESSAGE_COUNT:
                    entity = MessageCountSensor(device, measurement)
                case const.CONST_REACTIVE_ENERGY_CONSUMPTION:
                    entity = ReactiveEnergySensor(device, measurement)
                case const.CONST_REACTIVE_ENERGY_GENERATION:
                    entity = ReactiveEnergySensor(device, measurement)
            new_devices.append(entity)
    if new_devices:
        async_add_entities(new_devices)


class SensorBase(RestoreSensor):
    """Base representation of a Hello World Sensor."""

    _attr_should_poll = False

    def __init__(self, device, measurement):
        """Initialize the sensor."""
        self._device = device
        self._measurement = measurement
        self._attr_unique_id = f"{self._device._id}_{measurement}"
        self._attr_name = const.SENSOR_NAME_MAP[measurement]
        slug = slugify(f"{self._device._serial}_{measurement}")
        self.entity_id = f"sensor.{slug}"

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(const.DOMAIN, self._device._id)}}

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        data = await self.async_get_last_sensor_data()
        if data is not None:
            self._attr_native_value = data.native_value
        # Sensors should also register callbacks to HA when their state changes
        self._device.register_callback(self._measurement, self.update_measurement)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._device.remove_callback(self._measurement, self.update_measurement)

    @callback
    def update_measurement(self) -> None:
        """Return the state of the sensor."""
        self._attr_native_value = self._device._measurements[self._measurement]
        self.async_write_ha_state()


class HumiditySensor(SensorBase):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT


class TemperatureSensor(SensorBase):
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT


class PowerSensor(SensorBase):
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT


class EnergySensor(SensorBase):
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING


class ReactiveEnergySensor(SensorBase):
    _attr_native_unit_of_measurement = "VArh"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING


class DiagnosticSensorBase(SensorBase):
    _attr_entity_category = EntityCategory.DIAGNOSTIC


class RssiSensor(DiagnosticSensorBase):
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_entity_registry_enabled_default = False
    disabled = True


class BatteryVoltageSensor(DiagnosticSensorBase):
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    entity_registry_enabled_default = False
    disabled = True


class BatterySensor(DiagnosticSensorBase):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY

    def __init__(self, device, measurement):
        super().__init__(device, measurement)
        self._attr_unique_id = f"{self._device._id}_{measurement}_battery"

        self._attr_name = f"Battery"
        slug = slugify(f"{self._device._serial}_{measurement}_battery")
        self.entity_id = f"sensor.{slug}"

    @callback
    def update_measurement(self):
        """Return the state of the sensor."""
        self._attr_native_value = min(
            100,
            max(
                0,
                round(
                    ((self._device._measurements[self._measurement] - 4000.0) / 2000.0)
                    * 100.0
                ),
            ),
        )
        self.async_write_ha_state()


class SnrSensor(DiagnosticSensorBase):
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS
    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    entity_registry_enabled_default = False
    disabled = True


class MessageCountSensor(DiagnosticSensorBase):
    _attr_state_class = SensorStateClass.MEASUREMENT
    entity_registry_enabled_default = False
    disabled = True


class ErrorCodeSensor(DiagnosticSensorBase):
    _attr_icon = "mdi:alert-circle-outline"
    entity_registry_enabled_default = False
    disabled = True


class FreeHeapSensor(DiagnosticSensorBase):
    entity_registry_enabled_default = False
    disabled = True


class LargestHeapBlockSensor(DiagnosticSensorBase):
    entity_registry_enabled_default = False
    disabled = True
