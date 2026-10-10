---
name: story-editor
description: Build a coherent travel, food, or visit vlog from inventoried footage, choosing story beats, clip order, pacing, still-photo placement, and an edit decision list.
---

# Story editor

Read `BRIEF.md`, `SHOT_LOG.csv`, and `ASSET_PLAN.md` first. Write a clear arc in `STORYBOARD.md`: why we are going, the journey, arrival, place, main experience, and an ending. A short hook can precede the journey. Use the footage's actual strengths; do not force each vlog into identical beats.

Place every `must_use=yes` asset where it advances the story. A new driving clip belongs in the route, an earlier venue photo belongs near the current venue, and food photos belong beside the corresponding meal footage. Leave detailed text on screen long enough to read or pause.

Record each chosen source range and purpose in `EDIT_DECISIONS.csv`. Vary shot length with information density: a moving road view can be brief, while a menu card needs more time. Use direct cuts for continuous action and transitions where time, place, or medium changes. Avoid decorative transitions at every cut.

Run `scripts/check_edit_plan.py` before rendering. If the user says the vlog is too short, add meaningful journey or experience material before extending stills or repeating shots. Preserve the original sound when it carries context, and identify places that need narration, labels, or ambient sound in the storyboard.
