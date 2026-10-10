---
name: broll-curator
description: Prepare source-linked cutaway clips for any long or short video, with timecodes, rights, clear names, format-aware framing, and a contact sheet.
---

# B-roll curator

Use for a Reel, Short, long video, vlog, product video, or other footage edit when supporting shots need to be selected or stored. Establish the video's subject and delivery canvas first. Inspect each candidate visually; a name or one midpoint frame can hide unusable motion or a misleading shot. Favor footage that advances the story or covers a specific edit point.

For a new project, fill `templates/BROLL_MANIFEST.csv` with source path, in-point, duration, output name, category, usage note, rights, and any source URL. Then run `python scripts/curate_broll.py --manifest <csv> --output <folder> --profile wide|vertical|square|portrait-feed --mode fit|crop`. This trims raw video or animates a still into a clean MP4, writes `catalog.csv`, and makes a contact sheet. Source paths in the CSV are relative to that CSV. Use `rotation=none|cw|ccw|180` only after inspecting a clip with incorrect orientation; `auto` follows normal metadata. Use `fit` to keep the whole shot or `crop` only when the subject survives the crop. Preserve source audio when useful; the helper adds no title or music.

Keep source media untouched. If third-party footage is used, verify its current license and record its exact URL, creator, and attribution requirement. Label photo-derived motion honestly. Review the contact sheet and play the start and end of uncertain clips; check that no person, menu, sign, or important action was cut off. Report format, count, rights, and any unusable shots. Preparing a pack does not insert clips into the final edit.
