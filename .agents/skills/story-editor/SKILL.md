---
name: story-editor
description: Build a coherent travel, food, visit, or topic-driven video from inventoried footage, choosing story beats, clip order, pacing, still-photo placement, and an edit decision list.
---

# Story editor

Read `BRIEF.md`, `SHOT_LOG.csv`, and `ASSET_PLAN.md` first. Write a clear arc in `STORYBOARD.md` suited to the video type: an orientation, the journey or context, a main experience or argument, and an ending. A short hook can precede the setup. Use the footage's actual strengths; do not force a standard beat structure on content that tells its story differently.

Place every `must_use=yes` asset where it advances the story. A travel clip belongs in the route, an earlier context photo belongs near the relevant moment, and subject close-ups belong beside the corresponding footage. Leave detailed text on screen long enough to read or pause.

Record each chosen source range and purpose in `EDIT_DECISIONS.csv`. Vary shot length with information density: a wide establishing shot can be brief, while a text card or important detail needs more time. Use direct cuts for continuous action and transitions where time, place, or medium changes. Avoid decorative transitions at every cut.

Run `scripts/check_edit_plan.py` before rendering. If the creator says the video is too short, add meaningful content before extending stills or repeating shots. Preserve the original sound when it carries context, and identify places that need narration, labels, or ambient sound in the storyboard.
