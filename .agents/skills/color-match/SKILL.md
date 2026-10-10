---
name: color-match
description: Compare multiple frames from videos or photos across cameras, lighting, and output formats, then review a deliberate color adjustment.
---

# Color match

Use when adjacent shots, stills, or camera sources look inconsistent in a long or short video. Pick comparable subjects and lighting; a sunny road and indoor food shot should not be forced to the same averages. Run `python scripts/color_compare.py --input <source-a> --input <source-b> --out-dir <review-dir>` for an early/middle/late comparison sheet and JSON. Use `--samples 1..8` to change coverage or repeat `--at <seconds>` for exact times. Photos are accepted as single-frame sources.

Choose a reference shot by eye. Correct exposure and white balance first, then contrast and saturation in the editable project. The numeric averages are clues, not an automatic grade; preserve intentional warm light, natural skin, and recognizable food or product colors. Save chosen adjustments in the project review, rerender representative segments, and compare again. Watch the actual cut on both the target orientation and a small screen. State what improved and what still differs; do not claim a match from metrics alone.
