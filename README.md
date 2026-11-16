# ai-excited-01-entry

Entry for [make.fun's "Make the AI judge excited" bounty](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01), $250 in USDC.

An AI agent generated a 512×512 PNG (`entry.png`) and wrote `main.ts`, a tiny ESM script that copies `/bot/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). Deterministic: two runs produce byte-identical output.

## Run

```bash
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Regenerate the image

```bash
python3 generate_image.py
```

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/rayhankey3/ai-excited-01-entry/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/rayhankey3/ai-excited-01-entry/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
