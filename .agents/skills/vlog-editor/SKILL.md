---
name: vlog-editor
description: Plan and quality-check footage-based travel or food vlogs in this repository, including source inventory, story structure, required-shot coverage, portrait framing, photos, titles, audio, and export review.
---

# Vlog editor

Use this for a visit or travel vlog under `projects/`. Read its `BRIEF.md`, `SHOT_LOG.csv`, `STORYBOARD.md`, and `EDIT_DECISIONS.csv` if present. Inventory new media before editing; filenames alone are not enough to understand what a shot shows. Load the local `asset-plan` skill for new media, `watch` for video evidence or a reference style, `story-editor` for the cut structure, `broll-curator` for a reusable cutaway pack, `motion-overlay` for graphics, `audio-finisher` for the mixed soundtrack, `color-match` for inconsistent shots, `cut-audit` for edit boundaries, `render-review` for the final export, `platform-package` for upload assets, `format-repurposer` for another canvas, and `style-memory` when the creator gives corrections. Load only the relevant focused skills for the current task.

Build the story from what was actually filmed. For a visit, establish how the creator traveled there, what changed on arrival, what the place looks like, and the main experience. A food hook can precede the journey. Give required photos and videos a purposeful place in the sequence.

Treat `must_use=yes` in the shot log and direct user requests as coverage requirements. Run `scripts/check_edit_plan.py` before export. Record any deliberately omitted source with a reason in the shot log.

Use stills with gentle motion when it helps, especially detailed food photos; preserve readable menu text and natural framing. Use a few motivated transitions rather than adding one at every cut. Do not stretch portrait footage to fill 16:9. Label dishes, prices, and history only when source material or the user supports the claim.

Choose the editing implementation from `TOOLING.md`. If using Remotion or HyperFrames, load the installed framework skill and follow its setup and preview/render process. This skill covers editorial decisions and review; it does not replace framework documentation.

Before delivery, inspect representative frames in the final render, listen to the mix, and run `scripts/verify_export.py`. Give the user the final video and the editable project when available. Keep all referenced media with that project.

