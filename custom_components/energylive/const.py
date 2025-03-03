"""Constants for the energyLIVE integration."""

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "energylive"


CONST_CURRENT_POWER_CONSUMPTION = "0100010700"
CONST_ENERGY_CONSUMPTION = "0100010800"
CONST_CURRENT_POWER_GENERATION = "0100020700"
CONST_ENERGY_GENERATION = "0100020800"
CONST_REACTIVE_ENERGY_CONSUMPTION = "0100030800"
CONST_REACTIVE_ENERGY_GENERATION = "0100040800"
CONST_BATTERY_VOLTAGE = "batteryVoltage"
CONST_ERROR_CODE = "errorCode"
CONST_FREE_HEAP = "freeHeap8Bit"
CONST_LARGEST_HEAP_BLOCK = "largestHeapBlock8Bit"
CONST_LORA_RSSI = "loraRssi"
CONST_LORA_SNR = "loraSnr"
CONST_MESSAGE_COUNT = "messageCount"
CONST_ROOM_HUMIDITY = "roomHumidity"
CONST_ROOM_TEMPERATURE = "roomTemperature"
CONST_INTERFACE_DEVICE = "interface"
CONST_GATEWAY_DEVICE = "gateway"

SENSOR_NAME_MAP = {
    CONST_CURRENT_POWER_CONSUMPTION: "Current Power Consumption",
    CONST_ENERGY_CONSUMPTION: "Energy Consumed",
    CONST_CURRENT_POWER_GENERATION: "Current Power Return to Grid",
    CONST_ENERGY_GENERATION: "Energy Returned to Grid",
    CONST_REACTIVE_ENERGY_CONSUMPTION: "Reactive Energy Consumed",
    CONST_REACTIVE_ENERGY_GENERATION: "Reactive Energy Returned to Grid",
    CONST_BATTERY_VOLTAGE: "Battery Voltage",
    CONST_ERROR_CODE: "Error Code",
    CONST_FREE_HEAP: "Free Heap",
    CONST_LARGEST_HEAP_BLOCK: "Largest Heap Block",
    CONST_LORA_RSSI: "RSSI",
    CONST_LORA_SNR: "SNR",
    CONST_MESSAGE_COUNT: "Message Count",
    CONST_ROOM_HUMIDITY: "Humidity",
    CONST_ROOM_TEMPERATURE: "Temperature",
}

DEVICE_TYPE_MAP = {CONST_GATEWAY_DEVICE: "Gateway", CONST_INTERFACE_DEVICE: "Interface"}
