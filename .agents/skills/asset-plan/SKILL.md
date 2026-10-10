---
name: asset-plan
description: Inventory and classify footage, photos, audio, and factual evidence before a footage-based video edit; record required shots and source-backed labels in this repository.
---

# Asset plan

Use before the first cut, or when new media arrives mid-edit.

1. Run `scripts/scan_media.py` on the source folder. Use the local `watch` skill with `--engine local --no-whisper` to inspect representative frames from every new video, and inspect every new photo; filenames and metadata do not show what a shot contains.
2. Fill `SHOT_LOG.csv` with a story role, quality note, `must_use`, and `selected` status. Honor explicit user requests as must-use. Record why a shot is omitted when the omission could surprise the creator.
3. Fill `ASSET_PLAN.md` using the template. For a menu, price, historical photo, location, or named dish, record the visual or user statement that supports the on-screen wording. If evidence is uncertain, use a neutral label or omit the claim.
4. Note orientation, rotation metadata, resolution, and speech/audio needs. Keep source files untouched.
5. When additional media is added, rerun the inventory, update this plan, and check the final edit for coverage. Do not restart editorial choices that the user already accepted.

The asset plan records decisions and gaps. It does not require approval before ordinary, already-authorized editing.
