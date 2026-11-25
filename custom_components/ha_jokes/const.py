"""Constants for the Jokes integration."""

DOMAIN = "ha_jokes"
NAME = "Jokes"
VERSION = "1.8.0"

# API Configuration for icanhazdadjoke.com
API_URL_ICANHAZDADJOKE = "https://icanhazdadjoke.com"
API_HEADERS_ICANHAZDADJOKE = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

# API Configuration for JokeAPI v2
API_URL_JOKEAPI = "https://v2.jokeapi.dev/joke/Any?safe-mode&type=single"
API_HEADERS_JOKEAPI = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

API_URL_WITZAPI = "https://witzapi.de/api/joke/"
API_HEADERS_WITZAPI = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

# API Configuration for Official Joke API
API_URL_OFFICIAL = "https://official-joke-api.appspot.com/random_joke"
API_HEADERS_OFFICIAL = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

# API Configuration for Geek Jokes (unfiltered — largely Chuck Norris + crude material;
# not family-friendly, so it is opt-in rather than a default provider)
API_URL_GEEKJOKES = "https://geek-jokes.sameerkumar.website/api?format=json"
API_HEADERS_GEEKJOKES = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

# API Configuration for Yo Mama Jokes (adult/roast humour — not family-friendly)
API_URL_YOMAMA = "https://www.yomama-jokes.com/api/v1/jokes/random/"
API_HEADERS_YOMAMA = {
    "Accept": "application/json",
    "User-Agent": "Home Assistant Jokes Integration",
}

# Legacy API constants (for backward compatibility)
API_URL = API_URL_ICANHAZDADJOKE
API_HEADERS = API_HEADERS_ICANHAZDADJOKE

# Default Configuration
DEFAULT_REFRESH_INTERVAL = 5  # minutes
MIN_REFRESH_INTERVAL = 1     # minute
MAX_REFRESH_INTERVAL = 1440  # 24 hours in minutes

# Sensor Configuration
SENSOR_NAME = "Joke"
SENSOR_ICON = "mdi:emoticon-happy-outline"

# Configuration Keys
CONF_REFRESH_INTERVAL = "refresh_interval"
CONF_PROVIDERS = "providers"
CONF_JOKEAPI_LANGUAGE = "jokeapi_language"
CONF_MAX_JOKE_LENGTH = "max_joke_length"
DEFAULT_MAX_JOKE_LENGTH = 0  # unlimited

# Attributes
ATTR_JOKE = "joke"
ATTR_JOKE_ID = "joke_id"
ATTR_LAST_UPDATED = "last_updated"
ATTR_REFRESH_INTERVAL = "refresh_interval"
ATTR_SOURCE = "source"
ATTR_EXPLANATION = "explanation"

# Provider names
PROVIDER_ICANHAZDADJOKE = "icanhazdadjoke"
PROVIDER_JOKEAPI = "jokeapi"
PROVIDER_OFFICIAL = "official_joke_api"
PROVIDER_GEEKJOKES = "geek_jokes"
PROVIDER_YOMAMA = "yomama_jokes"
PROVIDER_WITZAPI = "witzapi"

# Default providers (family-friendly sources enabled by default).
# PROVIDER_GEEKJOKES and PROVIDER_YOMAMA are intentionally excluded — both serve
# unfiltered adult/edgy content (Geek Jokes is largely Chuck Norris + crude material;
# Yo Mama is roast humour) and must be opted into explicitly.
DEFAULT_PROVIDERS = [
    PROVIDER_ICANHAZDADJOKE,
    PROVIDER_JOKEAPI,
    PROVIDER_OFFICIAL,
]
DEFAULT_NEW_PROVIDERS = [PROVIDER_WITZAPI, *DEFAULT_PROVIDERS]
DEFAULT_JOKEAPI_LANGUAGE = "en"  # existing entries without a stored language
DEFAULT_NEW_LANGUAGE = "de"
# JokeAPI declares six joke languages, but we query it with type=single and its
# French and Portuguese corpora contain *only* two-part (setup/delivery) jokes.
# Asking for either returns HTTP 400 "No matching joke found" on every call, so
# offering them in the dropdown would let someone pick a value that can never
# produce a joke. Verified live 2026-10-17 against /joke/Any and /info:
#   safe single-type jokes -- en 183, de 29, es 6, cs 2, pt 0, fr 0
# To offer French and Portuguese we would have to stop hard-coding
# type=single and render two-part jokes; see the note in BREAKING_CHANGES.md.
JOKEAPI_LANGUAGE_OPTIONS = {
    "cs": "Čeština",
    "de": "Deutsch",
    "en": "English",
    "es": "Español",
}

PROVIDER_LANGUAGES = {
    PROVIDER_ICANHAZDADJOKE: {"en"},
    PROVIDER_JOKEAPI: JOKEAPI_LANGUAGE_OPTIONS.keys(),
    PROVIDER_OFFICIAL: {"en"},
    PROVIDER_GEEKJOKES: {"en"},
    PROVIDER_YOMAMA: {"en"},
    PROVIDER_WITZAPI: {"de", "en"},
}

# States
STATE_OK = "OK"
STATE_ERROR = "Error"


def providers_for_language(providers: list[str], language: str) -> list[str]:
    """Return the configured providers that serve the requested language."""
    return [
        provider
        for provider in providers
        if language in PROVIDER_LANGUAGES.get(provider, ())
    ]
