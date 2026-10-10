# Video Editing Kit

A reusable, local-first workspace for AI-assisted video editing. Covers YouTube long-form, visit and travel vlogs, Shorts, Instagram Reels, and other footage edits. It contains editing skills, project templates, and tested FFmpeg/Python helpers. Start each video in its own `projects/<name>/` folder. Source footage stays wherever you keep it; the kit does not copy or alter it.

This kit is **free, open-source, and agent-agnostic**. It works with Antigravity IDE, Claude Code, OpenAI Codex, and any AI agent that reads `.agents/skills/` directories. No cloud video, transcription, voice, or music service is required.

## Requirements

- Python 3.10 or newer and the free packages in `requirements.txt` (`Pillow`)
- FFmpeg and FFprobe on `PATH`
- Git for versioning plans and scripts

Optional (not required for core workflows):
- Remotion runtime (for React-based motion graphics)
- HyperFrames CLI (for HTML-based motion graphics)
- A Chatterbox voice model and consented reference recording under `private/` (for local narration generation)

From this folder, check the setup:

```powershell
# Windows
python -m pip install -r requirements.txt
ffmpeg -version
python scripts/test_cross_format.py
python scripts/test_semantic_search.py
```

```bash
# macOS / Linux
pip install -r requirements.txt
ffmpeg -version
python3 scripts/test_cross_format.py
python3 scripts/test_semantic_search.py
```

All included workflows run locally with free tools. The `watch` skill should use `--engine local --no-whisper` for private or local videos.

## Quick start

```powershell
# Create a new video project
python scripts/new_project.py my-next-video --media "C:\path\to\footage"

# Scan and inventory source media
python scripts/scan_media.py "C:\path\to\footage" --output-dir projects/my-next-video
```

Fill in `BRIEF.md`, `SHOT_LOG.csv`, `ASSET_PLAN.md`, and `STORYBOARD.md` in the new project. Choose the platform, aspect ratio, length, and style for that video. Mark footage that must appear with `must_use=yes` in the shot log. Record selected cuts in `EDIT_DECISIONS.csv`, then check coverage:

```powershell
python scripts/check_edit_plan.py projects/my-next-video
```

Open this folder as a workspace in your AI agent and read `.agents/skills/video-editor/SKILL.md` first. Use `vlog-editor` for a visit or travel vlog, `video-semantic-search` to check narration against reviewed frames, and the other focused skills as needed.

## Skills

The 16 editing skills under `.agents/skills/` cover every stage of a video project:

| Skill | Purpose |
| --- | --- |
| `video-editor` | Router: routes any video type to the right focused skill |
| `vlog-editor` | Full plan and review workflow for travel, food, or visit vlogs |
| `asset-plan` | Inventory footage, photos, and audio; record required shots |
| `story-editor` | Build story arc, storyboard, and edit decision list |
| `broll-curator` | Select and export source-linked cutaway clips |
| `motion-overlay` | Design and add titles, lower thirds, maps, and transitions |
| `color-match` | Compare frames across cameras and review color adjustments |
| `audio-finisher` | Measure and normalize the final mixed soundtrack |
| `cut-audit` | Audit edit boundaries for clipped speech or abrupt cuts |
| `render-review` | Review the finished export for coverage and technical quality |
| `format-repurposer` | Reframe a source range for a different canvas (9:16, 1:1, etc.) |
| `platform-package` | Create cover art, title, caption, credits, and chapters |
| `video-semantic-search` | Match narration to footage; audit timeline alignment |
| `style-memory` | Record and reuse creator preferences across projects |
| `voiceover-generator` | Generate narration locally with a consented voice model |
| `watch` | Inspect any local or public video with timestamped frames |

## Voiceover (bring your own voice)

This kit supports local, private voice cloning using [Resemble AI Chatterbox](https://github.com/resemble-ai/chatterbox) (free, open-source). No cloud API is required.

To use it:
1. Obtain a clean 3–60 second speech-only reference recording from the speaker (with their consent).
2. Place the reference and a compatible Chatterbox model checkpoint under `private/` (Git-ignored).
3. Create a Python virtual environment with the model's dependencies under `private/voice_env/`.
4. Run `--dry-run` to confirm paths, then generate takes:

```powershell
# Windows
.\private\voice_env\Scripts\python.exe scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/take_01.wav --dry-run
.\private\voice_env\Scripts\python.exe scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/take_01.wav
```

```bash
# macOS / Linux
python3 scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/take_01.wav --dry-run
python3 scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/take_01.wav
```

Read `.agents/skills/voiceover-generator/SKILL.md` for the full workflow.

## Finish and review

```powershell
python scripts/verify_export.py "C:\path\to\final.mp4" --aspect 16:9 --decode
python scripts/review_contact_sheet.py "C:\path\to\final.mp4" --out projects/my-next-video/review/contact_sheet.jpg
```

Use the intended ratio, such as `9:16`, for a vertical video. Watch and listen to the actual export, especially edit points, captions, still durations, and the first and last seconds. `scripts/audio_finish.py` measures and normalizes the finished soundtrack.

## What is included

- **16 local skills** for story, assets, B-roll, motion, color, voiceover, audio, semantic search, review, formats, and packaging.
- **11 project templates** for briefs, shot logs, edit decisions, visual plans, reviews, and upload preparation.
- **Scripts** for media scanning, B-roll curation, reframing, thumbnails, chapters, audio finishing, export verification, and semantic beat auditing.
- **Synthetic tests** that run without any real project footage.

## Contributing

See [SKILL_SOURCES.md](SKILL_SOURCES.md) for the source of each installed skill and the rationale for tool choices. See [TOOLING.md](TOOLING.md) for guidance on choosing an editing framework. New skills should use only free local tools, include a `SKILL.md` with a YAML frontmatter `name` and `description`, and not commit footage or private model files.
