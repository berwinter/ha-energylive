"""Config Flow for energyLIVE."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant

from .const import DOMAIN  # pylint:disable=unused-import
from .energylive import EnergyLive

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required(CONF_API_KEY): str})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Check if valid API key was provided."""
    if not data[CONF_API_KEY]:
        raise InvalidApiKey

    energylive = EnergyLive(data[CONF_API_KEY])
    result = await energylive.getDevices()

    if not result:
        raise CannotConnect

    return {"title": "energyLIVE"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for energyLIVE API key and re-auth."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH

    async def async_step_reauth(self, entry_data):
        """Perform reauthentication upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None):
        """Confirm reauthentication dialog."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidApiKey:
                errors[CONF_API_KEY] = "invalid_apikey"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
        return self.async_show_form(
            step_id="reauth_confirm", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_user(self, user_input=None):
        """Request API Key."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidApiKey:
                errors[CONF_API_KEY] = "invalid_apikey"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Cannot connect."""


class InvalidApiKey(exceptions.HomeAssistantError):
    """Invalid API key provided."""
