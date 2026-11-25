"""Regression tests for provider language and joke length settings."""

from unittest.mock import AsyncMock

import pytest
import voluptuous as vol
from homeassistant.config_entries import ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry
from yarl import URL

from custom_components.ha_jokes import sensor
from custom_components.ha_jokes.const import (
    API_URL_JOKEAPI,
    API_URL_WITZAPI,
    ATTR_JOKE,
    ATTR_SOURCE,
    CONF_JOKEAPI_LANGUAGE,
    CONF_MAX_JOKE_LENGTH,
    CONF_PROVIDERS,
    CONF_REFRESH_INTERVAL,
    DOMAIN,
    PROVIDER_ICANHAZDADJOKE,
    PROVIDER_JOKEAPI,
    PROVIDER_WITZAPI,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def enable_jokes(hass, enable_custom_integrations, monkeypatch):
    """Exercise the config entry without loading the dashboard frontend."""
    hass.config.components.update({"http", "frontend"})
    monkeypatch.setattr("custom_components.ha_jokes._async_register_frontend", AsyncMock())


async def test_setup_defaults_and_rejects_incompatible_providers(
    hass, enable_jokes, aioclient_mock
):
    """New entries require a compatible provider and baseline German settings."""
    flow = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    defaults = flow["data_schema"]({})
    assert defaults[CONF_JOKEAPI_LANGUAGE] == "de"
    assert PROVIDER_WITZAPI in defaults[CONF_PROVIDERS]
    assert defaults[CONF_MAX_JOKE_LENGTH] == 0
    for invalid_limit in (-1, -0.5, 1.5):
        with pytest.raises(vol.Invalid):
            flow["data_schema"]({**defaults, CONF_MAX_JOKE_LENGTH: invalid_limit})

    result = await hass.config_entries.flow.async_configure(
        flow["flow_id"], {**defaults, CONF_PROVIDERS: [PROVIDER_ICANHAZDADJOKE]}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {CONF_PROVIDERS: "no_compatible_providers"}

    text = "Langer deutscher Witz. " * 20 + "Die Pointe."
    aioclient_mock.get(
        f"{API_URL_WITZAPI}?language=de&limit=1",
        json=[{"language": "de", "text": text}],
    )
    options = {**defaults, CONF_PROVIDERS: [PROVIDER_WITZAPI]}
    result = await hass.config_entries.flow.async_configure(flow["flow_id"], options)
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].options == options
    assert hass.states.get("sensor.joke").attributes[ATTR_JOKE] == text


@pytest.mark.parametrize(
    "providers",
    [
        [PROVIDER_ICANHAZDADJOKE, PROVIDER_JOKEAPI],
        [PROVIDER_ICANHAZDADJOKE],
    ],
)
async def test_existing_german_entry_uses_only_german_sources(
    hass, enable_jokes, aioclient_mock, providers
):
    """Mixed and English-only legacy selections can still load in German."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        options={CONF_JOKEAPI_LANGUAGE: "de", CONF_PROVIDERS: providers},
    )
    entry.add_to_hass(hass)
    url = f"{API_URL_JOKEAPI}&lang=de"
    aioclient_mock.get(url, json={"joke": "Ein deutscher Witz.", "id": 1, "lang": "de"})

    assert await hass.config_entries.async_setup(entry.entry_id)
    assert hass.states.get("sensor.joke").attributes[ATTR_JOKE] == "Ein deutscher Witz."
    assert [call[1] for call in aioclient_mock.mock_calls] == [URL(url)]


async def test_strict_length_keeps_options_usable(
    hass, enable_jokes, aioclient_mock
):
    """An empty first refresh loads, and a saved limit takes effect on reload."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_JOKEAPI_LANGUAGE: "de",
            CONF_MAX_JOKE_LENGTH: 1,
            CONF_PROVIDERS: [PROVIDER_WITZAPI],
        },
    )
    entry.add_to_hass(hass)
    aioclient_mock.get(
        f"{API_URL_WITZAPI}?language=de&limit=20",
        json=[
            {"language": "en", "text": "A"},
            {"language": "de", "text": "Viel zu lang"},
            {"language": "de", "text": "  Gr&ouml;&szlig;e  "},
        ],
    )

    assert await hass.config_entries.async_setup(entry.entry_id)
    assert hass.states.get("sensor.joke").state == "Error"
    assert ATTR_JOKE not in hass.states.get("sensor.joke").attributes

    form = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        form["flow_id"],
        {
            CONF_JOKEAPI_LANGUAGE: "de",
            CONF_MAX_JOKE_LENGTH: 5,
            CONF_PROVIDERS: [PROVIDER_WITZAPI],
            CONF_REFRESH_INTERVAL: 5,
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert entry.state is ConfigEntryState.LOADED
    state = hass.states.get("sensor.joke")
    assert state.state == "OK"
    assert state.attributes[ATTR_JOKE] == "Größe"
    assert state.attributes[ATTR_SOURCE] == "witzapi.de"


async def test_jokeapi_no_match_loads_empty_sensor(hass, enable_jokes, aioclient_mock):
    """JokeAPI's no-match response leaves a configurable, empty sensor."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        options={CONF_JOKEAPI_LANGUAGE: "cs", CONF_PROVIDERS: [PROVIDER_JOKEAPI]},
    )
    entry.add_to_hass(hass)
    aioclient_mock.get(
        f"{API_URL_JOKEAPI}&lang=cs", status=400, json={"error": True, "code": 106}
    )

    assert await hass.config_entries.async_setup(entry.entry_id)
    assert hass.states.get("sensor.joke").state == "Error"
    assert ATTR_JOKE not in hass.states.get("sensor.joke").attributes


async def test_falls_back_to_suitable_jokeapi_candidate(
    hass, enable_jokes, aioclient_mock, monkeypatch
):
    """Discard overlong and wrong-language candidates across provider formats."""
    monkeypatch.setattr(sensor.random, "shuffle", lambda providers: None)
    entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_JOKEAPI_LANGUAGE: "de",
            CONF_MAX_JOKE_LENGTH: 6,
            CONF_PROVIDERS: [PROVIDER_WITZAPI, PROVIDER_JOKEAPI],
        },
    )
    entry.add_to_hass(hass)
    witzapi_url = f"{API_URL_WITZAPI}?language=de&limit=20"
    jokeapi_url = f"{API_URL_JOKEAPI}&lang=de&amount=10"
    aioclient_mock.get(
        witzapi_url, json=[{"language": "de", "text": "Viel zu lang"}]
    )
    aioclient_mock.get(
        jokeapi_url,
        json={
            "error": False,
            "jokes": [
                {"lang": "en", "joke": "Hello", "id": 1},
                {"lang": "de", "joke": "Ein passender Witz wäre kürzer", "id": 2},
                {"lang": "de", "joke": "Schnee", "id": 3},
            ],
        },
    )

    assert await hass.config_entries.async_setup(entry.entry_id)
    state = hass.states.get("sensor.joke")
    assert state.attributes[ATTR_JOKE] == "Schnee"
    assert state.attributes[ATTR_SOURCE] == "jokeapi.dev"
    assert [call[1] for call in aioclient_mock.mock_calls] == [
        URL(witzapi_url),
        URL(jokeapi_url),
    ]
