# Jokes Integration

Bring some humor to your Home Assistant setup with random jokes from multiple sources!

## What it does

This integration fetches random jokes from six sources, including WitzAPI, and makes them available as a sensor in Home Assistant. It tries compatible providers in random order and **ships its own Lovelace card**.

After installing Jokes and restarting Home Assistant, [open the Jokes setup](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_jokes). HACS shows updates when this fork publishes a new release.

## Key Features

- 🎭 **Multiple Joke Sources** include WitzAPI, JokeAPI v2, icanhazdadjoke.com and Official Joke API. Geek Jokes and Yo Mama Jokes are opt-in sources with unfiltered adult content.
- 🌍 **Joke language** applies to every source. New installations default to German with WitzAPI and JokeAPI enabled.
- 📏 **Maximum joke length (characters)** applies to the full joke. Enter 0 for unlimited length. The sensor stays empty for a refresh when no candidate fits.
- 🃏 **Bundled Lovelace Card**: `custom:ha-jokes-card` is included and auto-registered — nothing extra to install, no resource to add by hand. Just pick **"Jokes Card"** in the card picker
- 🔀 **Random Selection**: Providers are randomly selected for variety
- 🛡️ **Fault Tolerance**: Automatically tries alternative providers if one fails
- 📊 **Sensor Entity**: Clean integration with Home Assistant's sensor platform
- 🏷️ **Rich Attributes**: Joke text, unique ID, source, and metadata stored as attributes
- ⏰ **Configurable Updates**: Set refresh interval from 1 minute to 24 hours
- ⚙️ **Easy Setup**: Simple configuration through the Home Assistant UI
- 🔄 **Options Flow**: Change settings without removing and re-adding the integration
- 🛡️ **Robust**: Handles network errors and API issues gracefully
- 📱 **HACS Ready**: Full HACS compliance for easy installation and updates

## Perfect for

- Adding humor to your dashboard
- Creating fun automations and notifications
- Entertaining family and guests
- Breaking the ice during home automation demos
- Adding personality to your smart home

## Technical Details

- **Entity**: `sensor.joke` with state "OK" when a joke is available, "Error" if no candidate fits, or "unavailable" if the refresh fails
- **Attributes**: `joke`, `joke_id`, `source`, `last_updated`, `refresh_interval`
- **Icon**: 🙂 (mdi:emoticon-happy-outline)
- **Updates**: Configurable interval from 1-1440 minutes
- **APIs**: WitzAPI offers no safe mode. JokeAPI uses safe mode. The APIs require no keys.
- **Languages**: WitzAPI serves German and English. JokeAPI also serves Czech and Spanish. All other sources serve English only.
- **Options**: Change the language, length limit and sources under **Settings → Devices & Services → Jokes → Configure**. Enable WitzAPI there for an existing installation.
- **Card**: `custom:ha-jokes-card` — shows the joke, its source, how long ago it updated, and **Explain it** / **New joke** buttons

Ready to add some humor to your smart home? Install now and let the laughs begin! 😄
