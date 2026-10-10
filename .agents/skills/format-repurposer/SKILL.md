---
name: format-repurposer
description: Reframe a selected source range for wide YouTube, vertical Reels or Shorts, square, or portrait-feed delivery with fit or intentional crop.
---

# Format repurposer

Use when an existing video or source shot needs another canvas. Select the range by watching for a self-contained hook, action, and ending; a format change alone does not make a useful Short or Reel. Note the source time and any narration or captions that need context.

Run `python scripts/make_format.py <input> <output> --start <seconds> --duration <seconds> --profile wide|vertical|square|portrait-feed --mode fit|crop`. Omit duration for the rest of the source. `fit` preserves the full frame with a soft fill; `crop` fills the canvas and accepts `--focus-x` and `--focus-y` from 0 to 1. For a wide video that already contains an upright portrait shot with soft side fill, a centered crop often recovers the portrait area. Use `--fps` when a project needs a specific frame rate, and `--width` with `--height` for another even-sized canvas. `scripts/make_short.py` remains a compatibility entry point for older commands.

Review the beginning, middle, and end at the target size. Check faces, food, text, signs, and subtitles after the crop; adjust focus or use fit if needed. Source audio is retained, the original is untouched, and the result is only a candidate until the story and sound are reviewed. For platform-specific cover and copy, use `platform-package`.
