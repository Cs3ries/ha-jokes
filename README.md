# Jokes für Home Assistant

**Deutsche Witze von WitzAPI auf deinem Dashboard.** Wähle Sprache, Quellen und maximale Zeichenlänge. Die integrierte Jokes Card zeigt den aktuellen Witz und ruft auf Knopfdruck einen neuen ab.

<!-- ha-marketplace:exclude-start -->
[![Aktueller Release](https://img.shields.io/github/v/release/Cs3ries/ha-jokes?style=flat-square&label=Release)](https://github.com/Cs3ries/ha-jokes/releases/latest)
[![Home Assistant ab 2024.11.0](https://img.shields.io/badge/Home%20Assistant-ab%202024.11.0-41BDF5?style=flat-square)](https://www.home-assistant.io/)
[![MIT-Lizenz](https://img.shields.io/badge/Lizenz-MIT-6E7781?style=flat-square)](LICENSE)

[![In Home Assistant öffnen](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Cs3ries&repository=ha-jokes&category=integration)
<!-- ha-marketplace:exclude-end -->

Dieser Fork basiert auf der **Jokes-Integration** von **Loryan Strant** und den Mitwirkenden des Originalprojekts. [Zum Originalprojekt](https://github.com/loryanstrant/ha-jokes)

## Neu in Version 1.8

| Änderung | Im Alltag |
| --- | --- |
| **WitzAPI** | Eine zusätzliche Quelle für deutsche und englische Witze. Bei einer Neueinrichtung ist Deutsch voreingestellt. |
| **Sprache für alle Quellen** | Mit Deutsch als Auswahl kommen nur deutsche Witze. Rein englischsprachige Quellen werden bei dieser Auswahl übersprungen. |
| **Maximale Witzlänge** | Setze zum Beispiel **120 Zeichen** für eine Benachrichtigung. Zu lange Witze werden übersprungen, damit der Text vollständig bleibt. `0` erlaubt jede Länge. |
| **Einrichtung auf Deutsch** | Die deutschsprachige Oberfläche enthält die neuen Optionen und Hilfetexte. |

Version **1.8.0** prüft bei einem gesetzten Limit mehrere Kandidaten von WitzAPI und JokeAPI in einem Abruf. Wenn keine passende Antwort dabei ist, bleibt der Sensor für diesen Abruf leer. [Release v1.8.0](https://github.com/Cs3ries/ha-jokes/releases/tag/v1.8.0) · [Update-Hinweise](BREAKING_CHANGES.md#version-180) · [Kurzinfo](info.md)

<!-- ha-marketplace:exclude-start -->
## Installation

**Voraussetzung** ist Home Assistant Core **2024.11.0** oder neuer.

### Home Assistant Marketplace ab 2026.11

1. Öffne **Einstellungen → Marketplace → Über Link hinzufügen**.
2. Gib `https://github.com/Cs3ries/ha-jokes` ein. Wenn eine Kategorie abgefragt wird, wähle **Integration**.
3. Öffne den Eintrag **Jokes** und installiere **v1.8.0**. Wenn GitHub im Marketplace noch nicht verbunden ist, fordert Home Assistant die Verbindung beim Hinzufügen an. [Marketplace-Anleitung](https://www.home-assistant.io/integrations/marketplace/#custom-repositories)

Falls im Installationsdialog eine andere Version angezeigt wird, öffne im Jokes-Eintrag **⋮ → Andere Version installieren**. [Versionsauswahl](https://www.home-assistant.io/integrations/marketplace/#installing-another-version)

Ein bereits in HACS hinzugefügter Fork wird beim Wechsel zum Marketplace übernommen. [Umstieg von HACS](https://www.home-assistant.io/integrations/marketplace/#coming-from-hacs)

### HACS auf älteren Home-Assistant-Versionen

1. Öffne **HACS → ⋮ → Benutzerdefinierte Repositorys** und füge `https://github.com/Cs3ries/ha-jokes` als **Integration** hinzu.
2. Lade **Jokes v1.8.0** herunter und starte Home Assistant neu. [HACS-Anleitung](https://www.hacs.xyz/docs/faq/custom_repositories/)

<details>
<summary>Manuelle Installation über das Release-ZIP</summary>

1. Lade [ha_jokes.zip](https://github.com/Cs3ries/ha-jokes/releases/download/v1.8.0/ha_jokes.zip) aus dem Release herunter.
2. Entpacke die Dateien nach `/config/custom_components/ha_jokes/`. Die Datei `manifest.json` gehört direkt in diesen Ordner.
3. Starte Home Assistant neu.

</details>

Das Original und der Fork verwenden beide die Integrations-ID `ha_jokes`. Wenn du vom Original wechseln möchtest, sichere deine Home-Assistant-Konfiguration, deinstalliere das Original und richte anschließend den Fork ein. Bei der Deinstallation im Marketplace wird die bisherige Integrationseinrichtung entfernt. [Marketplace-Deinstallation](https://www.home-assistant.io/integrations/marketplace/#uninstalling-a-repository)
<!-- ha-marketplace:exclude-end -->

## Einrichtung

Öffne nach der Installation **Einstellungen → Geräte & Dienste → Integration hinzufügen → Jokes**. Starte Home Assistant nach einem Update der Integration neu, um die neue Version zu laden. [Home-Assistant-Dokumentation](https://www.home-assistant.io/integrations/marketplace/#keeping-installations-up-to-date)

<!-- ha-marketplace:exclude-start -->
[![Jokes in Home Assistant einrichten](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ha_jokes)
<!-- ha-marketplace:exclude-end -->

| Einstellung | Verhalten |
| --- | --- |
| **Sprache der Witze** | Deutsch ist bei einer Neueinrichtung voreingestellt. Außerdem stehen Englisch, Tschechisch und Spanisch zur Auswahl. |
| **Witzquellen** | Wähle mindestens eine Quelle, die die gewählte Sprache anbietet. Für Deutsch stehen WitzAPI und JokeAPI zur Verfügung. Aktiviere nur WitzAPI, wenn du ausschließlich diese Quelle verwenden möchtest. |
| **Maximale Witzlänge** | Zeichenlimit für den vollständigen Text. Leerzeichen und Zeilenumbrüche innerhalb des Witzes zählen mit. Standardwert `0`. |
| **Aktualisierungsintervall** | 1 bis 1.440 Minuten. Standardwert **5 Minuten**. |

Nach dem Update behalten vorhandene Installationen ihre gespeicherte Auswahl. Ältere Installationen ohne gespeicherte oder mit einer inzwischen ungültigen Sprache verwenden Englisch. Öffne **Einstellungen → Geräte & Dienste → Jokes → Konfigurieren**, um WitzAPI zu aktivieren und **Deutsch** oder ein Zeichenlimit auszuwählen. Gibt es in einer älteren Konfiguration keine zur Sprache passende Quelle, verwendet die Integration JokeAPI, bis du eine passende Auswahl speicherst.

<a name="jokes-card-recommended"></a>

## Den Witz auf dem Dashboard anzeigen

1. Öffne dein Dashboard und wähle **Bearbeiten → Karte hinzufügen**.
2. Suche nach **Jokes Card** und wähle `sensor.joke` als Entität.
3. Speichere die Karte. Mit **New joke** kannst du jederzeit einen neuen Witz abrufen. [Dashboard-Hilfe](https://www.home-assistant.io/dashboards/cards/#adding-cards-to-your-dashboard)

<p align="center"><img src="images/card.png" alt="Jokes Card aus dem Originalprojekt mit Witz, Quelle, Schaltflächen und optionaler KI-Erklärung" width="520"></p>

Die Karte wird mit der Integration geladen. Für **Explain it** brauchst du Home Assistant **2025.8** oder neuer und einen KI-Anbieter mit einer bevorzugten **AI Task**-Entität für die Datengenerierung. Die Erklärung erscheint unter dem Witz und lässt sich über `ha_jokes.explain_joke` abrufen. [AI Task einrichten](https://www.home-assistant.io/integrations/ai_task/)

<details>
<summary>YAML-Beispiele für die Jokes Card und eine schlichte Textkachel</summary>

```yaml
type: custom:ha-jokes-card
entity: sensor.joke
title: Aktueller Witz
```

```yaml
type: markdown
title: Aktueller Witz
content: |
  {{ state_attr('sensor.joke', 'joke') or 'Noch kein Witz verfügbar.' }}
```

Weitere Dashboard-Beispiele stehen in [examples/joke-cards.yaml](examples/joke-cards.yaml).

</details>

## Witzquellen

| Quelle | Sprachen | Hinweise |
| --- | --- | --- |
| [WitzAPI](https://witzapi.de/) | Deutsch, Englisch | Neu in 1.8. Ohne Jugendschutzfilter. |
| [JokeAPI v2](https://v2.jokeapi.dev/) | Deutsch, Englisch, Tschechisch, Spanisch | Einteilige Witze mit Safe Mode. |
| [icanhazdadjoke](https://icanhazdadjoke.com/) | Englisch | Dad Jokes. |
| [Official Joke API](https://github.com/15Dkatz/official_joke_api) | Englisch | Witze mit Aufbau und Pointe. |
| [Geek Jokes](https://github.com/sameerkumar18/geek-joke-api) | Englisch | Ungefilterte Inhalte. Nur bei ausdrücklicher Auswahl. |
| [Yo Mama Jokes](https://www.yomama-jokes.com/) | Englisch | Ungefilterte Roast-Witze. Nur bei ausdrücklicher Auswahl. |

Die Quellen benötigen keinen API-Schlüssel. Die Integration versucht kompatible Quellen in zufälliger Reihenfolge und wechselt bei Ausfällen oder unpassenden Antworten zur nächsten.

<details>
<summary>Sensorattribute, Automationen und Fehlersuche</summary>

Der Witztext steht in `sensor.joke` unter dem Attribut `joke`. Weitere Attribute sind `joke_id`, `source`, `last_updated` und `refresh_interval`. Damit kannst du Benachrichtigungen und Sprachausgaben erstellen. Einen sofortigen Abruf löst `homeassistant.update_entity` für `sensor.joke` aus.

Diese Automation verschickt nur dann eine Benachrichtigung, wenn nach einer Änderung ein Witztext vorhanden ist. Ersetze den Benachrichtigungsdienst durch deinen eigenen.

```yaml
alias: Witz anzeigen
triggers:
  - trigger: state
    entity_id: sensor.joke
    attribute: joke
conditions:
  - condition: template
    value_template: "{{ trigger.to_state is not none and trigger.to_state.attributes.get('joke') is not none }}"
actions:
  - action: notify.mobile_app_dein_handy
    data:
      title: Neuer Witz
      message: "{{ trigger.to_state.attributes.joke }}"
```

- **Sensor zeigt `Error`.** Erhöhe die maximale Witzlänge oder verwende `0`. Bei kurzen Limits können mehrere Abrufe ohne passenden Witz bleiben.
- **Sensor ist nicht verfügbar.** Prüfe **Einstellungen → System → Protokolle** auf Einträge zu `ha_jokes` und den gewählten Quellen.
- **Dashboard-Karte fehlt.** Richte zuerst die Integration ein und lade das Dashboard neu. Falls die automatische Registrierung laut Protokoll fehlschlägt, füge `/ha_jokes_frontend/ha-jokes-card.js` als JavaScript-Modul in den Dashboard-Ressourcen hinzu. [Ressourcenkonfiguration](https://www.home-assistant.io/dashboards/dashboards/#adding-yaml-dashboards)

</details>

## Credits und Lizenz

**Danke an Loryan Strant und alle Mitwirkenden des Originalprojekts.** Die Integration, der Sensor, die KI-Erklärung und die gezeigte Dashboard-Karte gehen auf ihre Arbeit zurück. Version 1.8 dieses Forks ergänzt WitzAPI, die Sprachauswahl über alle Quellen, das Zeichenlimit und die deutschen Einrichtungstexte. [Originalprojekt](https://github.com/loryanstrant/ha-jokes) · [Mitwirkende am Original](https://github.com/loryanstrant/ha-jokes/graphs/contributors)

Danke auch an die Anbieter der Witze, darunter WitzAPI, icanhazdadjoke, Sven Fehler für JokeAPI, David Katz für Official Joke API, Sameer Kumar für Geek Jokes und das Team hinter Yo Mama Jokes.

Das Projekt steht unter der **MIT-Lizenz**. Der Copyright-Hinweis für das Original nennt Loryan Strant. [Lizenztext](LICENSE)

<details>
<summary>Entwicklung und Tests</summary>

Die Versionsangaben und die Kartenregistrierung prüfst du mit `python3 scripts/check_versions.py`. Für die Regressionstests nutze eine passende Installation von `pytest-homeassistant-custom-component` und führe Folgendes aus.

```sh
python -m pytest -o asyncio_mode=auto -o asyncio_default_fixture_loop_scope=function tests
```

</details>
