# fun-colleague Copilot CLI plugin

This plugin adds a higher-energy collaboration mode for GitHub Copilot CLI.
It is meant to feel like working with a sharp colleague who is fun to pair with, without turning the session into a comedy routine.

## What it includes

- `agents/fun-colleague.agent.md` - a user-selectable custom agent for richer interactive sessions
- `skills/fun-colleague/SKILL.md` - reusable behavior rules for playful but useful responses
- `plugin.json` - plugin manifest for marketplace installs

## Intended behavior

- Keep engineering quality first
- Add light flair only when the interaction invites it
- Stay dry during autopilot, background work, routine command summaries, and critical execution steps
- Optionally use live web lookups when a fresh sports, trivia, or movie reference would genuinely add value

## Install

From the marketplace after publishing:

```bash
copilot plugin install fun-colleague@ekroon-copilot-plugins
```

During local development:

```bash
copilot plugin install /absolute/path/to/copilot-plugins/plugins/fun-colleague
```

## Update

After publishing a new version to the marketplace:

```bash
copilot plugin update fun-colleague
```

## Notes

- The marketplace entry should always carry the same version as `plugin.json`.
- This plugin pairs well with a thin `~/.copilot/copilot-instructions.md` bootstrap file so the base assistant stays consistent across projects.
