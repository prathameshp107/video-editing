---
name: render-review
description: Review a finished video export for story coverage, readable text, framing, motion graphics, audio, and technical integrity before delivery.
---

# Render review

Review the actual export after the edit is assembled. Run `scripts/verify_export.py <file> --aspect 16:9 --decode` with the project's intended aspect, and use `scripts/review_contact_sheet.py` for a whole-video visual scan. Then watch the opening, each story change, every must-use asset, text-heavy shot, portrait shot, motion insert, and ending at normal speed. Listen to the soundtrack and speech.

Check `SHOT_LOG.csv` and `EDIT_DECISIONS.csv` for required-shot coverage. Inspect menu prices and captions at original resolution. Verify that still-photo zooms feel smooth and that graphics stay out of important image areas. Record findings with timestamps and severity in `REVIEW.md`; fix material problems and review the revised export. A technically valid MP4 is not by itself an editorial pass.

For a significant or final release, ask an independent reviewer or a separate model to critique the rendered file if one is available. Their notes are evidence to inspect, not automatic edit instructions. Do not claim independent review when only the editor reviewed the cut.
