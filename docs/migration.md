# Migration to `copilot-catalog`

## Recommended cutover

1. rename `ekroon/copilot-plugins` to `ekroon/copilot-catalog`
2. merge `ekroon/agent-skills` into the renamed repository
3. preserve:
   - `plugins/<plugin-name>/...`
   - `skills/<skill-name>/SKILL.md`
4. update install and migration docs in the new repo
5. archive `ekroon/agent-skills` with a clear forwarding banner

## Path mapping

| Old location | New location |
| --- | --- |
| `copilot-plugins/plugins/<name>` | `copilot-catalog/plugins/<name>` |
| `agent-skills/skills/<name>` | `copilot-catalog/skills/<name>` |

## Migration options for local users

### Option A: rewrite config paths

Use the helper script:

```bash
python3 scripts/rewrite_local_paths.py \
  --root ~/.config \
  --old-repo-name copilot-plugins \
  --new-repo-name copilot-catalog \
  --apply
```

If you also embed `agent-skills` paths in config, the same script rewrites those to `copilot-catalog/skills/...`.

### Option B: temporary symlink bridge

If you want existing paths to keep working while you migrate:

```bash
ln -s /absolute/path/to/copilot-catalog/plugins /absolute/path/to/copilot-plugins/plugins
ln -s /absolute/path/to/copilot-catalog/skills /absolute/path/to/agent-skills/skills
```

### Option C: manual path update

Replace:

- `.../copilot-plugins/plugins/...` with `.../copilot-catalog/plugins/...`
- `.../agent-skills/skills/...` with `.../copilot-catalog/skills/...`

## Redirect and deprecation flow

### `copilot-plugins`

- rename to `copilot-catalog`
- rely on GitHub rename redirects for old browser and git URLs
- update the root README immediately after rename

### `agent-skills`

- replace the README with a deprecation banner and migration instructions
- create a final tagged release pointing to `copilot-catalog`
- archive it shortly after cutover
