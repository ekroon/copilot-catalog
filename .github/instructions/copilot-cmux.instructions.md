---
applyTo: "plugins/copilot-cmux/**,.github/plugin/marketplace.json"
---

# copilot-cmux guidance

## Architecture

`copilot-cmux` bridges Copilot CLI hook events to [cmux](https://cmux.dev) workspace sidebar updates and macOS notifications.

Relevant files:

- `.github/plugin/marketplace.json` — marketplace metadata pointing at `plugins/` root. Keep the version aligned with the plugin version when publishing.
- `plugins/copilot-cmux/plugin.json` — plugin manifest. The `repository` field is required for `copilot plugin update` to work.
- `plugins/copilot-cmux/hooks.json` — maps Copilot CLI hook events to the Python handler.
- `plugins/copilot-cmux/scripts/cmux_notify.py` — single-file handler implementing sidebar and notification logic.

## Hook event flow

All three hooks invoke `cmux_notify.py` with the event name as `argv[1]` and the hook payload on stdin.

- `sessionStart` clears previous state, signals `cmux claude-hook session-start`, and sets the running indicator.
- `preToolUse` dispatches by tool name.
  - `report_intent` updates sidebar title and intent status silently.
  - interactive tools such as `ask_user` update the attention indicator.
  - non-interactive tools clear the attention indicator and restore running status.
- `sessionEnd` clears indicators, signals `cmux claude-hook stop`, and removes temp state.

## Conventions

- State is stored per workspace in `/tmp/cmux-copilot-<safe_ref>.json`.
- Prefer the bundled cmux binary at `/Applications/cmux.app/Contents/Resources/bin/cmux`, then fall back to `$PATH`.
- If cmux is unavailable, fall back to `osascript` for notifications.
- Never let notification failures break the Copilot CLI session.
- Keep the implementation dependency-free and stdlib-only.
