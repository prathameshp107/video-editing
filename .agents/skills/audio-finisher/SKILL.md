---
name: audio-finisher
description: Measure and finish the mixed audio of a Reel, Short, long video, or audio-only deliverable with local FFmpeg and an encoded-output check.
---

# Audio finisher

Use after the picture or audio mix is assembled. Listen to the opening, any speech, loud effects, quiet sections, and ending. A short-form clip needs an immediate clear sound; a long edit needs consistent levels across sections. First fix competing dialogue, ambience, and music in the editable timeline. Loudness normalization cannot repair a bad balance.

Run `python scripts/audio_finish.py analyze <input> --out <report.json>` on the actual export or a representative excerpt. Review integrated loudness, range, and true peak together with listening. Choose `--target` and `--true-peak` for the deliverable; the script's defaults are working values, not a platform guarantee. For an already balanced single mixed track, run `python scripts/audio_finish.py normalize <input> <new-output> --target <LUFS> --true-peak <dBTP>`. It supports video MP4 and audio-only M4A, WAV, and MP3. It reserves encoding headroom and remeasures the final file.

Check `after.input_i`, `after.input_tp`, and `peak_limit_pass`; the loudness target may remain unmet when the peak ceiling constrains gain. Listen to the processed result and reject it if dynamics, speech clarity, or tone worsens. Never normalize a quiet isolated ambience stem as though it were a finished mix, and never overwrite the source. No paid service or upload is required.
