# Home Assistant Jokes Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat-square)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/Cs3ries/ha-jokes?style=flat-square)](https://github.com/Cs3ries/ha-jokes/releases)
[![Release date](https://img.shields.io/github/release-date/Cs3ries/ha-jokes?style=flat-square)](https://github.com/Cs3ries/ha-jokes/releases)
[![Downloads](https://img.shields.io/github/downloads/Cs3ries/ha-jokes/total?style=flat-square)](https://github.com/Cs3ries/ha-jokes/releases)
[![License](https://img.shields.io/github/license/Cs3ries/ha-jokes?style=flat-square)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Cs3ries/ha-jokes?style=flat-square)](https://github.com/Cs3ries/ha-jokes/commits)
[![Stars](https://img.shields.io/github/stars/Cs3ries/ha-jokes?style=flat-square)](https://github.com/Cs3ries/ha-jokes/stargazers)

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Cs3ries&repository=ha-jokes&category=integration)

A custom Home Assistant integration that serves random jokes from WitzAPI and other sources. Choose a language and cap the joke length for dashboards, notifications or text-to-speech.

<p align="center"><img width="256" height="256" alt="icon" src="https://github.com/user-attachments/assets/ec238fee-508a-4647-9071-d93bf83a9988" /></p>


## Features

- 🎭 Fetches random jokes from **six sources**, including WitzAPI for German and English
- 🔀 Random provider selection for variety
- 🛡️ Fault tolerance - automatically tries alternative providers if one fails
- 📊 Creates a sensor entity with state "OK" when successful
- 🏷️ Stores joke text, ID, and source as attributes (no 255 character state limitation)
- ⏰ Configurable refresh interval (1-1440 minutes, default: 5 minutes)
- 🌍 **Joke language** applies to every source. New installations default to German.
- 📏 **Maximum joke length** applies to every full joke. The default is unlimited.
- 🤖 AI-powered joke explanations using Home Assistant's AI integration
- ⚙️ Easy configuration through Home Assistant UI
- 🔄 Supports options flow for changing settings
- 🛡️ Robust error handling and logging
- 📱 HACS compliant for easy installation

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Add `https://github.com/Cs3ries/ha-jokes` as a custom repository with category **Integration**, then install **Jokes**
3. Restart Home Assistant
4. Go to Configuration > Integrations
5. Click "+ Add Integration" and search for "Jokes"

Or open it directly from here:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Cs3ries&repository=ha-jokes&category=integration)

HACS shows updates when a new release of this fork is available. Install the update through HACS and restart Home Assistant to load the new version.


### Manual Installation

1. Download and extract the [repository archive](https://github.com/Cs3ries/ha-jokes/archive/refs/heads/main.zip) or clone the fork
2. Open the extracted or cloned repository
3. Copy the `custom_components/ha_jokes` folder to your Home Assistant `custom_components` directory
4. Restart Home Assistant
5. Go to Configuration > Integrations
6. Click "+ Add Integration" and search for "Jokes"

## Configuration

### Initial Setup

After installing Jokes and restarting Home Assistant, open its setup directly:

[![Add Jokes to Home Assistant](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_jokes)

You can also open the setup through the Home Assistant menu.

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"Jokes"**
4. Set your desired refresh interval (1-1440 minutes, default: 5)
5. Choose the **Joke language** and at least one provider that serves it
6. Set **Maximum joke length (characters)** if needed
7. Click **"Submit"**

### Changing Options

1. Go to **Settings** → **Devices & Services**
2. Find the **Jokes** integration
3. Click **"Configure"**
4. Adjust the refresh interval as needed
5. Adjust **Joke providers**, **Joke language** and **Maximum joke length (characters)**
6. Click **"Submit"**

### Joke Language

| Language | Compatible sources |
|----------|--------------------|
| German (default for new installations) | WitzAPI, JokeAPI |
| English | WitzAPI, JokeAPI, icanhazdadjoke.com, Official Joke API, Geek Jokes, Yo Mama Jokes |
| Czech | JokeAPI |
| Spanish | JokeAPI |

The integration uses the selected sources that support your chosen language. With **Deutsch** selected, it fetches only German jokes, even when English-only sources are selected. New installations include WitzAPI and JokeAPI in the default selection. To fetch German jokes exclusively from WitzAPI, select **Deutsch** and enable only **WitzAPI (witzapi.de)**.

Existing installations keep their saved language and provider settings. To add WitzAPI to an existing installation, enable it in **Configure**. If a saved selection has no source for its language, the integration uses JokeAPI until you save a compatible selection. Older configurations without a saved language default to English.

### Maximum Joke Length

Enter a character limit, such as **120** for a notification, or **0** for unlimited length. Spaces and line breaks inside the joke count. The integration skips longer jokes and checks other candidates or compatible sources to preserve complete jokes. When none of the candidates fits, the sensor has no joke for that refresh. A very small limit can leave it empty until a later refresh or until you raise the limit.

## Usage

After installation, the integration creates a sensor entity:

- **Entity ID**: `sensor.joke`
- **State**: "OK" when a joke is available, "Error" when a provider responds without a suitable joke, or "unavailable" when the refresh fails
- **Icon**: 🙂 (mdi:emoticon-happy-outline)

### Attributes

The sensor provides the following attributes:

- `joke`: The complete joke text
- `joke_id`: Unique identifier for the joke
- `source`: The joke provider that supplied the joke
- `last_updated`: Timestamp of the last successful update
- `refresh_interval`: Current refresh interval in minutes

### Example Usage in Lovelace

#### Simple Entity Card
```yaml
type: entity
entity: sensor.joke
attribute: joke
name: "Joke of the Moment"
```

#### Markdown Card with last updated time
```yaml
type: markdown
content: |
  ## 😄 Joke
  {% set joke = state_attr('sensor.joke', 'joke') %}
  {% if joke %}
  {{ joke }}

  *Last updated @ {{ as_datetime(state_attr('sensor.joke', 'last_updated')).strftime('%H:%M %d %b %Y') }}*
  *Source: {{ state_attr('sensor.joke', 'source') }}*
  {% else %}
  *No joke available.*
  {% endif %}
```
<img width="515" height="142" alt="image" src="https://github.com/user-attachments/assets/02296d98-f871-4a0f-93fe-df820ee80b16" />



#### Markdown Card with time since last update
```yaml
type: markdown
content: |
  ## 😄 Joke
  {% set joke = state_attr('sensor.joke', 'joke') %}
  {% if joke %}
  {{ joke }}

  *Last updated: {{ relative_time(as_datetime(state_attr('sensor.joke', 'last_updated'))) }} ago*
  *Source: {{ state_attr('sensor.joke', 'source') }}*
  {% else %}
  *No joke available.*
  {% endif %}
```
<img width="518" height="147" alt="image" src="https://github.com/user-attachments/assets/076e83af-d8e4-43a6-bdd8-02635eb8f6cb" />


#### Custom Card with Conditional Display
```yaml
type: conditional
conditions:
  - entity: sensor.joke
    state: "OK"
card:
  type: markdown
  content: |
    ## 🎭 Today's Joke
    {{ state_attr('sensor.joke', 'joke') }}
    
    **Joke ID**: {{ state_attr('sensor.joke', 'joke_id') }}
    **Source**: {{ state_attr('sensor.joke', 'source') }}
    **Updated**: {{ state_attr('sensor.joke', 'last_updated') }}
```

#### Button Card Example (requires button-card from HACS)
```yaml
type: custom:button-card
entity: sensor.joke
name: Daily Joke
show_state: false
styles:
  card:
    - background-color: var(--primary-background-color)
    - padding: 20px
    - border-radius: 15px
  name:
    - font-size: 20px
    - font-weight: bold
    - color: var(--primary-text-color)
custom_fields:
  joke: |
    [[[
      return `<div style="font-size: 16px; line-height: 1.5; margin-top: 10px;">
        ${states['sensor.joke']?.attributes.joke ?? 'No joke available.'}
      </div>`
    ]]]
  source: |
    [[[
      return `<div style="font-size: 12px; color: var(--secondary-text-color); margin-top: 10px;">
        ${states['sensor.joke']?.attributes.source ?? ''}
      </div>`
    ]]]
```

#### Entities Card
```yaml
type: entities
title: Joke
entities:
  - entity: sensor.joke
    type: attribute
    attribute: joke
    name: Current Joke
  - entity: sensor.joke
    type: attribute
    attribute: source
    name: Source
    icon: mdi:information-outline
  - entity: sensor.joke
    type: attribute
    attribute: last_updated
    name: Last Updated
    icon: mdi:clock-outline
```

### Automations

You can use the sensor in automations:

```yaml
automation:
  - alias: "Announce Joke"
    trigger:
      - platform: state
        entity_id: sensor.joke
        attribute: joke
    condition:
      - condition: template
        value_template: "{{ trigger.to_state is not none and trigger.to_state.attributes.get('joke') is not none }}"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "New Joke!"
          message: "{{ trigger.to_state.attributes.joke }}"
```

### AI-Powered Joke Explanations

The integration provides an `ha_jokes.explain_joke` service that uses Home Assistant's AI integration to explain the current joke in plain language. This is perfect for jokes that might have wordplay, cultural references, or puns that need clarification.

<img width="1410" height="536" alt="image" src="https://github.com/user-attachments/assets/90830e78-ccc3-4fe2-8a79-8e862155dc39" />


#### Requirements
- Home Assistant AI integration must be configured (e.g., OpenAI, Google Generative AI, or Azure AI)
- A default AI conversation agent must be set up

#### Usage

**From the Developer Tools:**
1. Go to **Developer Tools** → **Actions**
2. Select the `ha_jokes.explain_joke` action
3. Click **"Perform Action"**

**In Automations:**
```yaml
automation:
  - alias: "Explain Joke on Request"
    trigger:
      - platform: state
        entity_id: input_boolean.explain_joke_trigger
        to: "on"
    action:
      - service: ha_jokes.explain_joke
      - service: notify.mobile_app_your_phone
        data:
          title: "Joke Explanation"
          message: "{{ state_attr('sensor.joke_explanation', 'explanation') }}"
```

**In Scripts:**
```yaml
script:
  get_joke_explanation:
    sequence:
      - service: ha_jokes.explain_joke
      - delay:
          seconds: 5
      - service: notify.persistent_notification
        data:
          title: "Joke Explanation"
          message: "{{ state_attr('sensor.joke_explanation', 'explanation') }}"
```

#### Explanation Sensor

After calling the `explain_joke` service, the explanation is stored in the `sensor.joke_explanation` entity:

- **Entity ID**: `sensor.joke_explanation`
- **State**: "Explained" when an explanation is available, "Not Explained" otherwise
- **Attribute**: `explanation` contains the AI-generated explanation

**Example Lovelace Card:**
```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 😄 Joke
      {{ state_attr('sensor.joke', 'joke') }}
  - type: button
    name: Explain This Joke
    icon: mdi:comment-question-outline
    tap_action:
      action: call-service
      service: ha_jokes.explain_joke
  - type: conditional
    conditions:
      - entity: sensor.joke_explanation
        state: "Explained"
    card:
      type: markdown
      content: |
        ### 💡 Explanation
        {{ state_attr('sensor.joke_explanation', 'explanation') }}
```

### Jokes Card (recommended)

The integration **ships its own Lovelace card**, `custom:ha-jokes-card`. It is bundled
with the integration and **auto-registered** — there is nothing to install in HACS and
no Lovelace resource to add by hand. After a restart, add a card to your dashboard, pick
**"Jokes Card"** from the card picker (or paste the YAML below).

The card shows the current joke in a styled quote, its source and how long ago it
updated, an **Explain it** button (triggers an AI explanation via `ha_jokes.explain_joke`),
a **New joke** button (fetches a fresh joke on demand), and a conditional explanation
panel that appears once an explanation has been generated. It uses your active theme's
colours, so it looks right in both light and dark mode.

The AI writes its explanation in Markdown, and the card renders it properly — **bold**
emphasis, paragraphs, and numbered/bulleted lists — using Home Assistant's own Markdown
renderer, so it matches the styling of the core Markdown card. Two-part jokes keep the line
break between setup and punchline.

<img alt="custom:ha-jokes-card showing a joke, its source, Explain it and New joke buttons, and an explanation panel" src="images/card.png" width="420" />

The card has a **visual editor** — pick it from the card picker and you get proper form
controls for every option below, so there is no need to write YAML by hand.

The explanation panel **clears itself whenever the joke changes** (the **New joke** button, a
manual refresh, or the automatic refresh interval), so you never see an explanation for a joke
that is no longer on screen.

```yaml
type: custom:ha-jokes-card
# all options below are optional — these are the defaults
entity: sensor.joke
explanation_entity: sensor.joke_explanation
title: Joke of the Moment
explanation_position: below
height: 0
width: 0
show_source: true
show_buttons: true
```

| Option | Default | Description |
|---|---|---|
| `entity` | `sensor.joke` | The joke sensor to display. |
| `explanation_entity` | `sensor.joke_explanation` | Sensor holding the AI explanation. |
| `title` | `Joke of the Moment` | Card heading. |
| `explanation_position` | `below` | `below` stacks the explanation under the joke; `side` puts it alongside. `side` automatically falls back to stacking when the card is too narrow for two columns. |
| `height` | `0` | Minimum card height in px (`0` = automatic). Useful to stop the card resizing as the explanation appears and disappears. |
| `width` | `0` | Maximum card width in px (`0` = fill the column). |
| `show_source` | `true` | Show the source/provider line. |
| `show_buttons` | `true` | Show the **Explain it** / **New joke** buttons. |

> If you'd rather not use the custom card, a **built-in-cards-only** alternative (plus an
> optional [Mushroom](https://github.com/piitaya/lovelace-mushroom) variant) lives in
> [`examples/joke-cards.yaml`](examples/joke-cards.yaml) — it works with core cards only.

## API Information

This integration fetches jokes from several different sources, automatically selecting them in random order and providing fault tolerance if one source is unavailable:

### Joke Sources

1. **[icanhazdadjoke.com](https://icanhazdadjoke.com/)** - A curated collection of dad jokes
   - Provides free access to dad jokes
   - Returns jokes in JSON format with unique IDs
   - No API key required

2. **[JokeAPI v2](https://v2.jokeapi.dev/)** - A RESTful API serving jokes
   - Configured in safe mode (no explicit content)
   - Returns single-line jokes only
   - Serves Czech, German, English and Spanish
   - Free and open source
   - No API key required

3. **[Official Joke API](https://github.com/15Dkatz/official_joke_api)** - A simple joke API
   - Community-maintained joke collection
   - Returns setup/punchline format jokes
   - Free and open source
   - No API key required

4. **[Geek Jokes](https://github.com/sameerkumar18/geek-joke-api)** - Random one-liners
   - ⚠️ **Not family-friendly** — despite the name, the feed is mostly Chuck Norris jokes with some crude/edgy content and no safe-mode filter. **Disabled by default**; opt in via the integration options
   - Returns single-line jokes
   - Free, no API key required

5. **[Yo Mama Jokes](https://www.yomama-jokes.com/)** - Roast-style "yo mama" jokes
   - ⚠️ **Not family-friendly** (adult/roast humour) — **disabled by default**; opt in via the integration options
   - Returns single-line jokes
   - Free, no API key required

6. **[WitzAPI](https://witzapi.de/api-docs/)** — German and English jokes
   - Enabled by default for new installations
   - Serves plain joke text without an API key or joke ID
   - The API offers no safe mode. Enable JokeAPI alone if you need its safe-mode filter.

The integration tries compatible providers in random order until it finds a joke within the configured length. When a limit is set, it requests up to 20 candidates from WitzAPI and up to 10 from JokeAPI in a single request per provider.

## Troubleshooting

### Common Issues

1. **Sensor shows "Error" or "unavailable"**
   - For "Error", increase the **Maximum joke length** or set it to 0 to allow any length
   - For "unavailable", check your internet connection and Home Assistant logs for provider errors

2. **Integration not appearing**
   - Ensure you've restarted Home Assistant after installation
   - Check that the `custom_components/ha_jokes` folder is in the correct location
   - Verify all required files are present

3. **Jokes not updating**
   - Check the refresh interval setting
   - Verify the sensor state is "OK"
   - Check logs for any error messages

### Logs

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.ha_jokes: debug
```

## Contributing

This fork builds on [loryanstrant/ha-jokes](https://github.com/loryanstrant/ha-jokes). Contributions are welcome.

## Development Approach

Run the regression tests with the `pytest-homeassistant-custom-component` plugin installed:

```sh
python -m pytest -o asyncio_mode=auto -o asyncio_default_fixture_loop_scope=function tests
```

<img width="256" height="256" alt="Vibe Coding with GitHub Copilot 256x256" src="https://github.com/user-attachments/assets/c8360318-0c18-4152-be59-3f3dcf4964a1" />


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Issues](https://github.com/Cs3ries/ha-jokes/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io/)

## Credits

- Jokes provided by:
  - [WitzAPI](https://witzapi.de/)
  - [icanhazdadjoke.com](https://icanhazdadjoke.com/)
  - [JokeAPI v2](https://v2.jokeapi.dev/) by Sven Fehler
  - [Official Joke API](https://github.com/15Dkatz/official_joke_api) by David Katz
  - [Geek Jokes](https://github.com/sameerkumar18/geek-joke-api) by Sameer Kumar (unfiltered, opt-in)
  - [Yo Mama Jokes](https://www.yomama-jokes.com/) (adult/roast humour, opt-in)
- Integration developed for the Home Assistant community
