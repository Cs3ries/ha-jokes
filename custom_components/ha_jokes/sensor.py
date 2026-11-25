"""Jokes sensor platform."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import html
import logging
import random
from typing import Any

import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_HEADERS_GEEKJOKES,
    API_HEADERS_ICANHAZDADJOKE,
    API_HEADERS_JOKEAPI,
    API_HEADERS_OFFICIAL,
    API_HEADERS_WITZAPI,
    API_HEADERS_YOMAMA,
    API_URL_GEEKJOKES,
    API_URL_ICANHAZDADJOKE,
    API_URL_JOKEAPI,
    API_URL_OFFICIAL,
    API_URL_WITZAPI,
    API_URL_YOMAMA,
    ATTR_EXPLANATION,
    ATTR_JOKE,
    ATTR_JOKE_ID,
    ATTR_LAST_UPDATED,
    ATTR_REFRESH_INTERVAL,
    ATTR_SOURCE,
    DEFAULT_JOKEAPI_LANGUAGE,
    DEFAULT_MAX_JOKE_LENGTH,
    DEFAULT_PROVIDERS,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
    PROVIDER_GEEKJOKES,
    PROVIDER_ICANHAZDADJOKE,
    PROVIDER_JOKEAPI,
    PROVIDER_OFFICIAL,
    PROVIDER_WITZAPI,
    PROVIDER_YOMAMA,
    SENSOR_ICON,
    SENSOR_NAME,
    STATE_ERROR,
    STATE_OK,
    providers_for_language,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Jokes sensor platform."""
    # Get coordinator from hass.data
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    
    # The config entry's first refresh has already populated the coordinator.
    async_add_entities([
        JokesSensor(coordinator, config_entry),
        JokeExplanationSensor(coordinator, config_entry),
    ])


class JokesDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def _build_provider_configs(self) -> list[dict[str, Any]]:
        """Build provider configurations."""
        jokeapi_url = f"{API_URL_JOKEAPI}&lang={self._jokeapi_language}"
        witzapi_limit = 1
        if self._max_joke_length:
            jokeapi_url += "&amount=10"
            witzapi_limit = 20
        return [
            {
                "name": PROVIDER_WITZAPI,
                "url": (
                    f"{API_URL_WITZAPI}?language={self._jokeapi_language}"
                    f"&limit={witzapi_limit}"
                ),
                "headers": API_HEADERS_WITZAPI,
                "parser": self._parse_witzapi,
            },
            {
                "name": PROVIDER_ICANHAZDADJOKE,
                "url": API_URL_ICANHAZDADJOKE,
                "headers": API_HEADERS_ICANHAZDADJOKE,
                "parser": self._parse_icanhazdadjoke,
            },
            {
                "name": PROVIDER_JOKEAPI,
                "url": jokeapi_url,
                "headers": API_HEADERS_JOKEAPI,
                "parser": self._parse_jokeapi,
            },
            {
                "name": PROVIDER_OFFICIAL,
                "url": API_URL_OFFICIAL,
                "headers": API_HEADERS_OFFICIAL,
                "parser": self._parse_official_joke_api,
            },
            {
                "name": PROVIDER_GEEKJOKES,
                "url": API_URL_GEEKJOKES,
                "headers": API_HEADERS_GEEKJOKES,
                "parser": self._parse_geekjokes,
            },
            {
                "name": PROVIDER_YOMAMA,
                "url": API_URL_YOMAMA,
                "headers": API_HEADERS_YOMAMA,
                "parser": self._parse_yomama,
            },
        ]

    def __init__(
        self,
        hass: HomeAssistant,
        refresh_interval: int,
        enabled_providers: list[str],
        jokeapi_language: str | None = None,
        config_entry: ConfigEntry | None = None,
        *,
        max_joke_length: int = DEFAULT_MAX_JOKE_LENGTH,
    ) -> None:
        """Initialize."""
        self.platforms = []
        self._refresh_interval = refresh_interval
        self._jokeapi_language = jokeapi_language or DEFAULT_JOKEAPI_LANGUAGE
        self._max_joke_length = max_joke_length
        compatible_providers = providers_for_language(
            enabled_providers or DEFAULT_PROVIDERS, self._jokeapi_language
        )
        # Older entries could save any combination of language and providers.
        if not compatible_providers:
            compatible_providers = [PROVIDER_JOKEAPI]
        self._providers = [
            provider
            for provider in self._build_provider_configs()
            if provider["name"] in compatible_providers
        ]
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=refresh_interval),
            config_entry=config_entry,
        )

    def _parse_icanhazdadjoke(self, data: dict) -> dict[str, Any]:
        """Parse icanhazdadjoke.com response."""
        return {
            ATTR_JOKE: data.get("joke", ""),
            ATTR_JOKE_ID: data.get("id", ""),
            ATTR_SOURCE: "icanhazdadjoke.com",
        }

    def _parse_jokeapi(self, data: dict) -> list[dict[str, Any]]:
        """Parse JokeAPI v2 response."""
        candidates = data.get("jokes", [data])
        if data.get("error") or not isinstance(candidates, list):
            return []
        return [
            {
                ATTR_JOKE: item.get("joke"),
                ATTR_JOKE_ID: str(item.get("id", "")),
                ATTR_SOURCE: "jokeapi.dev",
            }
            for item in candidates
            if isinstance(item, dict) and item.get("lang") == self._jokeapi_language
        ]

    def _parse_witzapi(self, data: list) -> list[dict[str, Any]]:
        """Parse WitzAPI's list of jokes."""
        if not isinstance(data, list):
            raise ValueError("Expected a list of jokes from WitzAPI")
        return [
            {ATTR_JOKE: item.get("text"), ATTR_JOKE_ID: "", ATTR_SOURCE: "witzapi.de"}
            for item in data
            if isinstance(item, dict) and item.get("language") == self._jokeapi_language
        ]

    def _parse_official_joke_api(self, data: dict) -> dict[str, Any]:
        """Parse Official Joke API response."""
        # Official Joke API returns setup and punchline separately
        setup = data.get("setup", "")
        punchline = data.get("punchline", "")
        joke_text = f"{setup} {punchline}" if setup and punchline else ""
        joke_id = str(data.get("id", ""))
        
        return {
            ATTR_JOKE: joke_text,
            ATTR_JOKE_ID: joke_id,
            ATTR_SOURCE: "official-joke-api.appspot.com",
        }

    def _parse_geekjokes(self, data: dict) -> dict[str, Any]:
        """Parse Geek Jokes response."""
        # Geek Jokes returns a single 'joke' field and no id
        return {
            ATTR_JOKE: data.get("joke", ""),
            ATTR_JOKE_ID: "",
            ATTR_SOURCE: "geek-jokes.sameerkumar.website",
        }

    def _parse_yomama(self, data: dict) -> dict[str, Any]:
        """Parse Yo Mama Jokes response (adult/roast humour)."""
        # Yo Mama returns a 'joke' field (plus a 'category') and no id
        return {
            ATTR_JOKE: data.get("joke", ""),
            ATTR_JOKE_ID: "",
            ATTR_SOURCE: "yomama-jokes.com",
        }

    async def _fetch_from_provider(
        self, session: aiohttp.ClientSession, provider: dict
    ) -> dict[str, Any] | None:
        """Fetch a matching joke, or return None if the request failed."""
        try:
            async with session.get(
                provider["url"],
                headers=provider["headers"],
                timeout=aiohttp.ClientTimeout(total=5),
            ) as response:
                if response.status != 200:
                    if response.status == 400 and provider["name"] == PROVIDER_JOKEAPI:
                        error = await response.json()
                        if isinstance(error, dict) and error.get("code") == 106:
                            return {}
                    _LOGGER.warning(
                        "Provider %s returned status %s",
                        provider["name"],
                        response.status,
                    )
                    return None
                parsed = provider["parser"](await response.json())
                candidates = parsed if isinstance(parsed, list) else [parsed]
                for candidate in candidates:
                    text = candidate.get(ATTR_JOKE)
                    if not isinstance(text, str):
                        continue
                    # Measure the text as it will appear in the sensor and card.
                    text = html.unescape(text).strip()
                    if text and (
                        not self._max_joke_length or len(text) <= self._max_joke_length
                    ):
                        return {**candidate, ATTR_JOKE: text}
                return {}
        except Exception as err:
            _LOGGER.warning(
                "Error fetching from provider %s: %s", provider["name"], err
            )
            return None

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library with fault tolerance."""
        # Randomize provider order for each request
        providers = self._providers.copy()
        random.shuffle(providers)
        
        _LOGGER.debug("Attempting to fetch joke from providers in random order")
        
        try:
            async with async_timeout.timeout(30):
                session = async_get_clientsession(self.hass)
                provider_responded = False
                for provider in providers:
                    result = await self._fetch_from_provider(session, provider)
                    if result:
                        result[ATTR_LAST_UPDATED] = datetime.now().isoformat()
                        result[ATTR_REFRESH_INTERVAL] = self._refresh_interval
                        return result
                    if result is not None:
                        provider_responded = True

                if provider_responded:
                    _LOGGER.debug("No joke matched the configured language and length")
                    return {}
                raise UpdateFailed("All compatible joke providers failed to respond")
                    
        except asyncio.TimeoutError as exception:
            raise UpdateFailed(
                f"Timeout communicating with joke APIs: {exception}"
            ) from exception
        except UpdateFailed:
            raise
        except Exception as exception:
            raise UpdateFailed(
                f"Error communicating with joke APIs: {exception}"
            ) from exception


class JokesSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Jokes sensor."""

    def __init__(
        self,
        coordinator: JokesDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = SENSOR_NAME
        self._attr_icon = SENSOR_ICON
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self.coordinator.last_update_success and self.coordinator.data:
            return STATE_OK
        return STATE_ERROR

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        return {
            ATTR_JOKE: self.coordinator.data.get(ATTR_JOKE, ""),
            ATTR_JOKE_ID: self.coordinator.data.get(ATTR_JOKE_ID, ""),
            ATTR_SOURCE: self.coordinator.data.get(ATTR_SOURCE, ""),
            ATTR_LAST_UPDATED: self.coordinator.data.get(ATTR_LAST_UPDATED, ""),
            ATTR_REFRESH_INTERVAL: self.coordinator.data.get(ATTR_REFRESH_INTERVAL, DEFAULT_REFRESH_INTERVAL),
        }

    # No options listener here on purpose: __init__.py registers
    # async_reload_entry, which rebuilds the coordinator and both entities from
    # the saved options. A second listener on the same entry would duplicate
    # that work, and its signature has to match what core calls it with.


class JokeExplanationSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Joke Explanation sensor."""

    def __init__(
        self,
        coordinator: JokesDataUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Joke Explanation"
        self._attr_icon = "mdi:comment-question-outline"
        self._attr_unique_id = f"{DOMAIN}_{config_entry.entry_id}_explanation"
        self._explanation = None
        # Which joke the current explanation belongs to, so we can drop it once the
        # joke rotates. Prefer joke_id; fall back to the joke text for providers that
        # do not supply an id.
        self._explained_joke_key = None

    def _current_joke_key(self) -> str | None:
        """Identify the joke the coordinator is currently serving."""
        data = self.coordinator.data or {}
        return data.get(ATTR_JOKE_ID) or data.get(ATTR_JOKE) or None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Discard the explanation when it no longer matches the current joke.

        Without this the sensor keeps reporting "Explained" with the previous joke's
        explanation forever, so any dashboard showing it displays an explanation for a
        joke that is no longer on screen.
        """
        if self._explanation:
            current = self._current_joke_key()
            # A successful refresh can leave the sensor empty if no joke matched.
            if self.coordinator.last_update_success and current != self._explained_joke_key:
                _LOGGER.debug("Joke rotated; clearing the stale explanation")
                self._explanation = None
                self._explained_joke_key = None
        super()._handle_coordinator_update()

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if self._explanation:
            return "Explained"
        return "Not Explained"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_EXPLANATION: self._explanation or "No explanation available",
            # Lets a dashboard (or automation) tell which joke this explanation is for.
            ATTR_JOKE_ID: self._explained_joke_key or "",
        }

    async def async_explain_joke(self) -> None:
        """Explain the current joke using AI."""
        _LOGGER.info("=== Starting explain_joke service ===")
        # Find the joke sensor entity dynamically
        joke = None
        joke_key = None
        joke_entity_id = None
        
        # Search for the joke sensor entity
        for entity_id in self.hass.states.async_entity_ids("sensor"):
            if entity_id.startswith(f"sensor.{DOMAIN}_") and "explanation" not in entity_id:
                # This is likely our joke sensor
                state = self.hass.states.get(entity_id)
                if state and state.attributes.get(ATTR_JOKE):
                    joke = state.attributes.get(ATTR_JOKE)
                    joke_key = state.attributes.get(ATTR_JOKE_ID) or joke
                    joke_entity_id = entity_id
                    break
            elif entity_id == "sensor.joke":
                # Check for the main joke sensor by name
                state = self.hass.states.get(entity_id)
                if state and state.attributes.get(ATTR_JOKE):
                    joke = state.attributes.get(ATTR_JOKE)
                    joke_key = state.attributes.get(ATTR_JOKE_ID) or joke
                    joke_entity_id = entity_id
                    break
        
        if not joke:
            _LOGGER.warning("No joke available to explain")
            self._explanation = "No joke available to explain"
            self._explained_joke_key = None
            self.async_write_ha_state()
            return

        # Tie everything we set below (explanation *or* error message) to this joke, so it
        # is discarded as soon as the joke rotates.
        self._explained_joke_key = joke_key
        
        # Check if ai_task service is available
        if not self.hass.services.has_service("ai_task", "generate_data"):
            _LOGGER.error("ai_task.generate_data service is not available. Please configure an AI provider.")
            self._explanation = "AI service not configured. Please configure an AI provider in Home Assistant."
            self.async_write_ha_state()
            return
        
        try:
            # Call the ai_task.generate_data service with correct parameters
            _LOGGER.info("Calling ai_task.generate_data for joke from %s", joke_entity_id)
            _LOGGER.info("Joke to explain: %s", joke[:100])
            response = await self.hass.services.async_call(
                "ai_task",
                "generate_data",
                {
                    "task_name": "explain_joke",
                    "instructions": f"Explain the following joke in plain language:\n{joke}",
                },
                blocking=True,
                return_response=True,
            )
            if self._current_joke_key() != joke_key:
                return
            
            _LOGGER.info("AI service response: %s", response)
            _LOGGER.info("Response type: %s", type(response))
            
            if response:
                # The azure_ai_tasks service returns a dict with 'data' key containing the text
                if isinstance(response, dict):
                    self._explanation = response.get("data", "Unable to generate explanation")
                else:
                    self._explanation = str(response)
            else:
                self._explanation = "No response from AI service"
                
            self.async_write_ha_state()
            _LOGGER.debug("Joke explanation generated successfully")
            
        except Exception as err:
            _LOGGER.error("Failed to generate joke explanation: %s", err)
            if self._current_joke_key() != joke_key:
                return
            self._explanation = f"Error: {str(err)}"
            self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        
        # Store reference to this entity in hass.data for service calls
        if DOMAIN in self.hass.data and self._config_entry.entry_id in self.hass.data[DOMAIN]:
            self.hass.data[DOMAIN][self._config_entry.entry_id]["explanation_entity"] = self
