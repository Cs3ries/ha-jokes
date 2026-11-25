---
title: 'GitHub documentation for Jokes 1.8'
type: 'chore'
created: '2026-11-25'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent">

## Intent

Refresh the GitHub landing page and release documentation for Jokes 1.8. The page should make installation and dashboard setup easy, explain which features the fork added, and credit Loryan Strant and contributors for the original project.

- Given a visitor opens the fork, when they read the start page, then they can identify the current release, the original repository, the compatible installation paths, and the changes in 1.8.
- Given a user installs or upgrades, when they follow the instructions, then they can configure the joke language, character limit, and dashboard card, with existing configurations accounted for.
- Given a user opens the GitHub release notes, when they look for changes and attribution, then they find the same release information and credits.

</frozen-after-approval>

## Implementation Notes

- Use a German landing page, the existing dashboard screenshot with attribution, and a small set of badges.
- Use the built-in Marketplace instructions for Home Assistant 2026.11 and newer. Keep HACS instructions for compatible older installations and a manual ZIP path.
- Update the current documentation and published release notes for the existing package version 1.8.0. The change is documentation-only.

## Review Triage Log

- Medium, fixed. Explain Marketplace GitHub authorization, v1.8.0 selection, restart after updates, and automatic HACS migration.
- Medium, fixed. Explain the shared integration ID and the effect of uninstalling the upstream version before installing the fork.
- Medium, fixed. Describe provider validation, legacy language fallback to English, and the AI Task minimum version and preferred entity.
- Low, fixed. Document manual dashboard resource registration and link the standalone project summary.
- Low, rejected for this change. The generated internal navigation map requires the upstream navgen tool, which is unavailable locally.

## Verification

- Validate GitHub and repository links, Marketplace markers, and YAML examples.
- Run the version check and six integration regression cases. Compare the release manifest with the current version.
