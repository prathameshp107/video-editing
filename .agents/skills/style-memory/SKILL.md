---
name: style-memory
description: Turn explicit creator feedback on pacing, framing, titles, transitions, and audio into a reusable style note without overgeneralizing one-off corrections.
---

# Style memory

Read the project `STYLE.md` before editing. When the creator corrects an edit, fix the video first, then record the preference in `STYLE.md` with the example, reason, and scope. Mark it as project-specific or reusable. Update the repository's `STYLE_DEFAULTS.md` only when the user states a general preference or the same correction recurs across projects.

Keep preferences concrete: for example, "show the journey before arrival" or "keep portrait footage upright in a wide frame with soft side fill." Avoid rigid rules such as "always crossfade" or "always zoom" from a single clip. Prefer rules that explain what visual problem they solve. If the current user instruction conflicts with a saved preference, follow the current instruction and update the note.

Use the local `watch` skill with `--engine local --no-whisper` when the creator provides a video to emulate: observe its shot duration, framing, typography, and transition frequency, then write measurable notes. Listen separately if audio feel matters. Treat a reference video as a guide, not a mandate to copy every element.

For open-source use: `STYLE_DEFAULTS.md` ships with example preferences from the original creator of this kit. Clear or replace those rows when setting up a new workspace for a different creator. Each row should reflect only that creator's stated preferences.
