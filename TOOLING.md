# Choosing an editing tool

Start with the story and source media. The choice of rendering framework follows the edit, not the other way around.

**Watch:** Use the MIT-licensed local `watch` skill to inspect source clips or perform deep forensic post-mortem analysis of reference videos (Instagram Reels, YouTube Shorts, competitor edits) with timestamped frames and native captions. It examines every frame for camera angles, typography styling, motion graphics, pacing, and audio design. In this free-only kit, pass `--engine local --no-whisper`; the visual workflow needs no API key.

**FFmpeg + Kdenlive:** A good fit for many phone clips, trim decisions, rotation fixes, portrait footage in a 16:9 canvas, straightforward dissolves, and an editable timeline. FFmpeg can normalize media before timeline editing and verify the export. Keep normalized media next to the project file.

**Remotion:** Choose for custom React-based titles, maps, animated labels, and reusable visual components. Open the installed Remotion skill before creating a project. A skill installation alone does not install the Remotion runtime. Pin and install dependencies in the individual video project, preview there, and render when an MP4 is requested.

**HyperFrames:** Choose for HTML-based compositions, motion graphics, captions, and designed transitions. Start with the installed HyperFrames entry skill; it routes the work to the appropriate workflow. The CLI may require installation or network access. If unavailable, keep the footage plan and use a local editing path for the requested deliverable.

The official HyperFrames `general-video` workflow has been installed for future multi-scene vlog work. For motion inserts inside an existing edit, read the local `motion-overlay` skill and the relevant Remotion or HyperFrames skill before building.

**Mixing tools:** Render a motion graphic from Remotion or HyperFrames as an asset, then place it on a Kdenlive timeline or in an FFmpeg assembly. Match frame rate, dimensions, and audio sample rate before combining. Keep the source project and rendered overlay together in the per-video project folder.

## Default vlog checks

1. Inventory all clips and photos. Look at contact sheets or representative frames, and listen where speech or ambience matters.
2. Plan the experience as a sequence suited to the footage: hook, context, main experience, close. Change this shape if the footage calls for it.
3. List required shots in `SHOT_LOG.csv`. Check them against `EDIT_DECISIONS.csv` before rendering.
4. Keep portrait images upright in a wide frame without stretching. Use a motivated crop or soft background.
5. Use transitions at story changes or between stills when they help. Keep text cards readable long enough to pause.
6. Label subjects and factual claims only with details supported by the footage or supplied by the creator.
7. Review the rendered file at opening, key transitions, text, still photos, and ending. Check audio and decode the export.

## Agent compatibility

This kit is designed to work with any AI agent that reads `.agents/skills/` directories (Antigravity, Claude Code, Codex, and compatible systems). Skills are loaded on demand from their `SKILL.md` files. The `AGENTS.md` file at the repository root is the always-on rule set. No agent-specific CLI is assumed to be installed.
