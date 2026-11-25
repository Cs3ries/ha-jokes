"""Config flow for Jokes integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import selector

from .const import (
    CONF_JOKEAPI_LANGUAGE,
    CONF_MAX_JOKE_LENGTH,
    CONF_PROVIDERS,
    CONF_REFRESH_INTERVAL,
    DEFAULT_JOKEAPI_LANGUAGE,
    DEFAULT_MAX_JOKE_LENGTH,
    DEFAULT_NEW_LANGUAGE,
    DEFAULT_NEW_PROVIDERS,
    DEFAULT_PROVIDERS,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
    JOKEAPI_LANGUAGE_OPTIONS,
    MAX_REFRESH_INTERVAL,
    MIN_REFRESH_INTERVAL,
    NAME,
    PROVIDER_GEEKJOKES,
    PROVIDER_ICANHAZDADJOKE,
    PROVIDER_JOKEAPI,
    PROVIDER_OFFICIAL,
    PROVIDER_WITZAPI,
    PROVIDER_YOMAMA,
    providers_for_language,
)


def _options_schema(values: dict[str, Any]) -> vol.Schema:
    """Build the shared setup and options form."""
    return vol.Schema(
        {
            vol.Required(
                CONF_REFRESH_INTERVAL, default=values[CONF_REFRESH_INTERVAL]
            ): vol.All(
                cv.positive_int,
                vol.Range(min=MIN_REFRESH_INTERVAL, max=MAX_REFRESH_INTERVAL),
            ),
            vol.Required(CONF_PROVIDERS, default=values[CONF_PROVIDERS]): cv.multi_select(
                {
                    PROVIDER_WITZAPI: "WitzAPI (witzapi.de)",
                    PROVIDER_ICANHAZDADJOKE: "icanhazdadjoke.com",
                    PROVIDER_JOKEAPI: "JokeAPI (jokeapi.dev)",
                    PROVIDER_OFFICIAL: "Official Joke API",
                    PROVIDER_GEEKJOKES: "Geek Jokes (⚠️ not family-friendly)",
                    PROVIDER_YOMAMA: "Yo Mama Jokes (⚠️ not family-friendly)",
                }
            ),
            vol.Required(
                CONF_JOKEAPI_LANGUAGE, default=values[CONF_JOKEAPI_LANGUAGE]
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        selector.SelectOptionDict(value=code, label=label)
                        for code, label in JOKEAPI_LANGUAGE_OPTIONS.items()
                    ],
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_MAX_JOKE_LENGTH, default=values[CONF_MAX_JOKE_LENGTH]
            ): vol.All(int, vol.Range(min=0)),
        }
    )


def _provider_errors(values: dict[str, Any]) -> dict[str, str]:
    """Check that the selection can serve the chosen language."""
    providers = values[CONF_PROVIDERS]
    if not providers:
        return {CONF_PROVIDERS: "no_providers_selected"}
    if not providers_for_language(providers, values[CONF_JOKEAPI_LANGUAGE]):
        return {CONF_PROVIDERS: "no_compatible_providers"}
    return {}


class JokesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jokes."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        values: dict[str, Any] = {
            CONF_REFRESH_INTERVAL: DEFAULT_REFRESH_INTERVAL,
            CONF_PROVIDERS: DEFAULT_NEW_PROVIDERS,
            CONF_JOKEAPI_LANGUAGE: DEFAULT_NEW_LANGUAGE,
            CONF_MAX_JOKE_LENGTH: DEFAULT_MAX_JOKE_LENGTH,
        }
        errors = {}
        if user_input is not None:
            values.update(user_input)
            errors = _provider_errors(values)
            if not errors:
                return self.async_create_entry(title=NAME, data={}, options=values)

        return self.async_show_form(
            step_id="user", data_schema=_options_schema(values), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> JokesOptionsFlow:
        """Get the options flow for this handler."""
        return JokesOptionsFlow(config_entry)


class JokesOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Jokes."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        values: dict[str, Any] = {
            CONF_REFRESH_INTERVAL: DEFAULT_REFRESH_INTERVAL,
            CONF_PROVIDERS: DEFAULT_PROVIDERS,
            CONF_JOKEAPI_LANGUAGE: DEFAULT_JOKEAPI_LANGUAGE,
            CONF_MAX_JOKE_LENGTH: DEFAULT_MAX_JOKE_LENGTH,
            **self._config_entry.options,
        }
        if values[CONF_JOKEAPI_LANGUAGE] not in JOKEAPI_LANGUAGE_OPTIONS:
            values[CONF_JOKEAPI_LANGUAGE] = DEFAULT_JOKEAPI_LANGUAGE

        errors = {}
        if user_input is not None:
            values.update(user_input)
            errors = _provider_errors(values)
            if not errors:
                return self.async_create_entry(title="", data=values)

        return self.async_show_form(
            step_id="init", data_schema=_options_schema(values), errors=errors
        )
