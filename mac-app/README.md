# Claude Usage Tracker

A [SwiftBar](https://swiftbar.app) plugin that shows your **Claude Code token usage** live in the Mac menu bar — no API key needed, all data is read locally from `~/.claude/projects/`.

![Claude Usage Tracker menu bar screenshot](https://img.shields.io/badge/SwiftBar-plugin-7b68ee?style=flat-square) ![Python 3](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square) ![macOS](https://img.shields.io/badge/macOS-only-lightgrey?style=flat-square)

---

## What it shows

- **Today** — total tokens, sessions, and estimated cost
- **This month** — cumulative totals
- **All time** — grand totals + models used
- **Quick links** — Claude.ai and the Anthropic Console

The menu bar icon changes color based on today's usage:

| Icon | Meaning |
|------|---------|
| ⚪ | No usage today |
| 🟢 | Under 100k tokens |
| 🟡 | 100k – 500k tokens |
| 🔴 | Over 500k tokens |

Refreshes automatically every **5 minutes**.

---

## Requirements

- macOS
- [SwiftBar](https://swiftbar.app) (free — App Store or website)
- Python 3.8+
- [Claude Code](https://claude.ai/code) installed and run at least once

---

## Quick install

```bash
git clone https://github.com/knowjoby/claude-usage-tracker.git
cd claude-usage-tracker
bash install.sh
```

The installer will:
1. Check for SwiftBar and Python 3
2. Auto-detect your SwiftBar plugins folder
3. Copy the plugin and set permissions
4. Refresh SwiftBar so it appears immediately

---

## Manual install

1. Download [`claude-usage.5m.py`](claude-usage.5m.py)
2. Copy it to your SwiftBar plugins folder (e.g. `~/Documents/SwiftBar-Plugins/`)
3. Make it executable: `chmod +x claude-usage.5m.py`
4. Click **Refresh All** in SwiftBar

---

## Configuration

Open `claude-usage.5m.py` and edit the two variables near the top:

```python
SHOW_COST = os.environ.get("SHOW_COST", "true").lower() == "true"
PLAN      = os.environ.get("PLAN", "pro")  # "pro" or "api"
```

Or set them as SwiftBar environment variables without editing the file — SwiftBar reads the `<swiftbar.environment>` header at the top of the script.

### Pricing

Token prices are defined in the `PRICES` dict. They match [Anthropic's published pricing](https://www.anthropic.com/pricing) at the time of writing. Update the values there if pricing changes.

---

## How it works

Claude Code writes a `.jsonl` session file for every project under `~/.claude/projects/`. Each line is a JSON object representing one API call. This plugin:

1. Finds all `.jsonl` files under `~/.claude/projects/`
2. Reads every `assistant`-type entry that has a `usage` field
3. Buckets token counts by day / month / all-time
4. Calculates estimated cost using per-model pricing
5. Outputs SwiftBar-formatted text to the menu bar

No data leaves your machine.

---

## Supported models

| Model | Input | Output |
|-------|-------|--------|
| claude-opus-4-6 / 4-5 | $15 / 1M | $75 / 1M |
| claude-sonnet-4-6 / 4-5 | $3 / 1M | $15 / 1M |
| claude-haiku-4-5 | $0.80 / 1M | $4 / 1M |

Cache read/write tokens are tracked and priced separately.

---

## Troubleshooting

**No data shown / ⚙️ icon**
- Make sure Claude Code has been run at least once
- Check that `~/.claude/projects/` exists and contains `.jsonl` files

**Wrong cost estimates**
- Update the `PRICES` dict in the script to match current [Anthropic pricing](https://www.anthropic.com/pricing)

**Plugin not appearing in menu bar**
- Confirm the file is in your SwiftBar plugins folder
- Confirm the file is executable (`chmod +x claude-usage.5m.py`)
- Click **Refresh All** in SwiftBar or restart it

---

## License

MIT
