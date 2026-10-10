---
name: cut-audit
description: Audit the picture and audio at edit boundaries in a rendered vlog, catching clipped speech, sudden sound changes, black frames, awkward dissolves, and visible jump cuts.
---

# Cut audit

Use after a rough cut when the video has speech, synced sound, or many transitions. Inspect the rendered file, not only the transcript or timeline data.

At each suspicious boundary, watch and listen from roughly one second before to one second after. Check whether a word is cut before its final sound, whether ambient noise changes abruptly, whether music masks speech, and whether a visual transition creates a flash, duplicate frame, or unintended jump. Log the time and the smallest repair in `CUT_AUDIT.md`.

Prioritize speech and chapter boundaries; for a music-only montage, focus on audible pops, timing, and picture continuity. If needed, extract a short local review clip with FFmpeg rather than repeatedly rendering the whole film. Recheck repaired boundaries in the new export.

Do not make a transcript the sole evidence that a spoken sentence survives the cut. Automated silence detection can nominate areas to inspect but cannot confirm complete words.
