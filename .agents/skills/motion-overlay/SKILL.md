---
name: motion-overlay
description: Design and add short motion graphics inside an existing video, such as titles, maps, labels, lower thirds, photo moves, and transitions, using Remotion or HyperFrames where appropriate.
---

# Motion overlays for footage

Use when a motion element explains the story or improves readability. Read the project's `BRIEF.md`, `STORYBOARD.md`, and `MOTION_PLAN.md`. For each insert, write its purpose, exact placement, source evidence, duration, size, safe area, and how it enters and leaves. Motion should support the footage rather than cover a face, subject, key label, or important landmark.

Choose the implementation for the insert:

- Use the installed Remotion skills for React-based graphics, reusable components, animated maps, or data-driven layouts.
- Use the installed HyperFrames entry skill for HTML-based compositions, designed captions, or short motion graphics. Follow its workflow and CLI availability checks.
- For a subtle still-photo pan/zoom or simple dissolve, a timeline editor or FFmpeg may be more direct.

Match the main edit's resolution, frame rate, and color treatment. Render a transparent overlay only if the chosen framework and codec support the needed alpha; otherwise render the graphic over its intended background. Review the graphic in the final assembled video at normal playback speed and on a small screen. Keep the source composition alongside its rendered asset.

**Typography:** Check `STYLE_DEFAULTS.md` and the project's `STYLE.md` for the creator's recorded font preferences before choosing typefaces. If no preference is recorded, choose a legible sans-serif appropriate to the platform and canvas. The free OFL font files are in `assets/fonts/` (Poppins and Open Sans variants); copy them into a project if the renderer needs a local font directory. Verify rendered glyphs; do not rely on a fallback with a similar name. Build a small visual sample before rendering the full timeline.

**Motion style:** Prefer graphic motion tied to a story event, then inspect the entrance, hold, and exit at playback speed. Avoid generic sweep bars and transitions that call more attention to themselves than the footage. Use clean cuts and short dissolves where they support time or place changes.

Do not infer a subject name, price, route, or factual claim from an unclear image. Read `ASSET_PLAN.md` for evidence.
