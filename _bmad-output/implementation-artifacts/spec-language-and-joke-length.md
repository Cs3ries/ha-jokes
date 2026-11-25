---
title: 'Joke language and maximum length'
type: 'feature'
created: '2026-11-25'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

Add WitzAPI to the Home Assistant fork. Apply the selected joke language to every source and let users set a maximum joke length during setup or in the integration options. Update the README, HACS description and upgrade notes.

- Given German is selected, when the integration polls, then only German-capable providers are contacted and responses that lack a matching language are discarded.
- Given a positive character limit, when a provider returns candidate jokes, then only complete jokes at or below that limit can become the sensor value. Given zero, any length is allowed.
- Given every responding provider has no matching candidate, when the refresh ends, then the sensor shows no new joke and the options remain usable.
- Given an existing configuration, when the integration loads after the update, then it honors the stored language, refresh interval and compatible providers. New installations default to German and enable WitzAPI.

</frozen-after-approval>

## Implementation Notes

- The existing `jokeapi_language` storage key preserves current configurations. The shared provider-language mapping drives runtime eligibility and form validation. Existing entries with no language retain English and entries without a compatible source can use JokeAPI.
- WitzAPI returns `text` and `language` in a list. Filter the decoded, stripped joke text locally across all providers. Use batch requests where supported when a limit is enabled.
- Verify with repository checks and Home Assistant config-flow and coordinator tests. Keep generated navigation files out of the change.
- The setup flow defaults to WitzAPI and JokeAPI for German. Existing entries keep their chosen sources. The settings and docs describe WitzAPI's lack of safe mode.
- Successful polls with no suitable joke leave the sensor empty and clear its explanation. Failed requests can fall back to another compatible source. The setup uses the first result without a second immediate poll.

## Review Triage Log

- Medium, fixed. An AI response arriving after the joke changes is discarded. The card also hides explanations when the joke is empty.
- Medium, fixed. JokeAPI's documented HTTP 400 with code 106 is treated as an empty result.
- Low, fixed. Unexpected WitzAPI response shapes count as provider failures.
- Medium, fixed. The length schema rejects fractional and negative inputs.
- Medium, fixed. README cards and notifications handle missing joke attributes.
- Low, rejected for this change. The regression tests have a documented local command. CI configuration is outside the feature scope.
- Medium, fixed. A successful setup-flow test checks saved options and publishes a joke longer than 255 characters when the maximum is zero.

## Verification

- Six regression cases passed with Home Assistant 2024.11.3. The version and card checks, Python compilation, JavaScript syntax check and diff check passed.
- Live calls through the coordinator returned German jokes within 120 characters from both WitzAPI and JokeAPI.
- The HACS and Hassfest GitHub Actions require Docker and remain pending.
