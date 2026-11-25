# Jokes für Home Assistant · Version 1.8

Zeige aktuelle Witze auf deinem Dashboard. **WitzAPI** ergänzt die vorhandenen Quellen um deutsche und englische Witze. Bei einer Neueinrichtung ist Deutsch voreingestellt.

- **Sprache der Witze** filtert alle Quellen. Für Deutsch kannst du WitzAPI und JokeAPI wählen.
- **Maximale Witzlänge** begrenzt den vollständigen Text in Zeichen. `0` erlaubt jede Länge. Zu lange Witze werden übersprungen.
- **Aktualisierungsintervall** von 1 bis 1.440 Minuten. Im Standard lädt die Integration alle 5 Minuten einen Witz.
- **Jokes Card** zeigt den Witz aus `sensor.joke`. Mit **New joke** rufst du einen neuen Witz ab. Die optionale KI-Erklärung setzt Home Assistant 2025.8 oder neuer und eine bevorzugte **AI Task**-Entität zur Datengenerierung voraus.

Öffne **Einstellungen → Geräte & Dienste → Jokes → Konfigurieren**, um WitzAPI in einer vorhandenen Installation zu aktivieren. WitzAPI liefert Witze ohne Jugendschutzfilter. JokeAPI nutzt Safe Mode.

Home Assistant Core **2024.11.0** oder neuer wird vorausgesetzt. [Einrichtung öffnen](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_jokes) · [Anleitung für Version 1.8](https://github.com/Cs3ries/ha-jokes#readme) · [Release v1.8.0](https://github.com/Cs3ries/ha-jokes/releases/tag/v1.8.0)

Vielen Dank an **Loryan Strant** und die Community des Originalprojekts für die Integration, die Dashboard-Karte und die KI-Erklärung. [Originalprojekt](https://github.com/loryanstrant/ha-jokes) · [MIT-Lizenz](LICENSE)
