"""energyLIVE API."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import json
import logging
import traceback

import httpx

from homeassistant.core import HomeAssistant
from homeassistant.helpers.start import async_at_start
from homeassistant.util.ssl import get_default_context

_LOGGER = logging.getLogger(__name__)
_FORBIDDEN = 403


class EnergyLive:
    """EnergyLIVE hub base class."""

    def __init__(self, apiKey, hass: HomeAssistant | None = None, entry=None):
        self._entry = entry
        self._hass = hass
        self._apiKey = apiKey
        self._devices = []
        ctx = get_default_context()
        timeout = httpx.Timeout(10.0, connect=60.0)
        self._client = httpx.AsyncClient(
            verify=ctx, timeout=timeout, headers={"X-API-KEY": self._apiKey}
        )

    async def getDevices(self):
        if len(self._devices) == 0:
            devices = await self._client.get(
                "https://backend.energylive.e-steiermark.com/api/v1/devices"
            )
            if devices.status_code == _FORBIDDEN:
                if self._entry is not None and self._hass is not None:
                    self._entry.async_start_reauth(self._hass)
            else:
                for dev in devices.json():
                    self._devices.append(Device(self, dev, self._hass, self._entry))
        return self._devices


class Device:
    def __init__(self, energylive, id, hass: HomeAssistant | None = None, entry=None):
        self._hass = hass
        self._entry = entry
        self._energylive = energylive
        self._id = id
        self._details = False
        self._serial = None
        self._type = None
        self._measurements = dict()
        self._callbacks = dict()
        if self._hass is not None and self._entry is not None:
            async_at_start(self._hass, self._async_startup)

    async def getDetails(self):
        if not self._details:
            response = await self._energylive._client.get(
                f"https://backend.energylive.e-steiermark.com/api/v1/devices/{self._id}"
            )
            if response.status_code == _FORBIDDEN:
                self._entry.async_start_reauth(self._hass)
            else:
                response = response.json()
                self._type = response["type"]
                self._serial = response["serial"]
                measurements = await self._energylive._client.get(
                    f"https://backend.energylive.e-steiermark.com/api/v1/devices/{self._id}/measurements"
                )
                if measurements.status_code == _FORBIDDEN:
                    self._entry.async_start_reauth(self._hass)
                else:
                    for measurement in measurements.json():
                        self._measurements[measurement] = None
                    self._details = True

    async def _async_startup(self, loop):
        self._background_task = self._hass.async_create_background_task(
            self.run_background_task(),
            name=f"energyLIVE background task for {self._id}",
        )

    async def run_background_task(self):
        _LOGGER.debug(f"background task for energylive {self._id}")
        while True:
            request = self._energylive._client.build_request(
                "GET",
                f"https://backend.energylive.e-steiermark.com/api/v1/devices/{self._id}/measurements/live",
                headers={
                    "X-API-KEY": self._energylive._apiKey,
                    "Accept": "text/event-stream",
                },
                timeout=httpx.Timeout(60.0, read=900),
            )
            r = await self._energylive._client.send(request, stream=True)
            if r.status_code == _FORBIDDEN:
                self._entry.async_start_reauth(self._hass)
                break
            try:
                async for line in r.aiter_lines():
                    if line:
                        decoded_line = "{" + line.replace("data", '"data"') + "}"
                        try:
                            data = json.loads(decoded_line)
                            await self.publish_updates(
                                data["data"]["measurement"], data["data"]["value"]
                            )
                        except json.JSONDecodeError:
                            pass
            except (httpx.ReadTimeout, httpx.RemoteProtocolError):
                pass
            except Exception as e:
                _LOGGER.warning(f"{self._id}: restart connection... - {type(e)}\n{e}")
                _LOGGER.warning(traceback.format_exc())
                await asyncio.sleep(100)
            await r.aclose()

    async def publish_updates(self, measurement, value) -> None:
        self._measurements[measurement] = value
        if measurement in self._callbacks:
            for callback in self._callbacks[measurement]:
                callback()

    def register_callback(self, measurement, callback: Callable[[], None]) -> None:
        if not measurement in self._callbacks:
            self._callbacks[measurement] = set()
        self._callbacks[measurement].add(callback)

    def remove_callback(self, measurement, callback: Callable[[], None]) -> None:
        if measurement in self._callbacks:
            self._callbacks[measurement].discard(callback)
