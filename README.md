# Video Editing

A reusable, local workspace for YouTube videos, visit vlogs, Shorts, Instagram Reels, and other footage edits. It contains editing skills, project templates, and tested FFmpeg/Python helpers. Start each video in its own `projects/<name>/` folder. Source footage stays wherever you keep it; the kit does not copy or alter it.

## Requirements

- Python 3.10 or newer and the free packages in `requirements.txt` (`Pillow`)
- FFmpeg and FFprobe on `PATH`
- Git is useful for versioning the plans and scripts
- Remotion and HyperFrames are optional. Their Codex skills are installed separately on this machine; this folder does not install their runtimes.

From this folder in PowerShell, check the setup:

```powershell
python -m pip install -r requirements.txt
ffmpeg -version
python scripts/test_cross_format.py
python scripts/test_semantic_search.py
```

All included workflows can run locally with free tools. The `watch` skill should use `--engine local --no-whisper` for private or local videos. Its optional online modes are not part of this kit.

## Start a video

```powershell
python scripts/new_project.py my-next-video --media "C:\path\to\footage"
python scripts/scan_media.py "C:\path\to\footage" --output-dir projects/my-next-video
```

Fill in `BRIEF.md`, `SHOT_LOG.csv`, `ASSET_PLAN.md`, and `STORYBOARD.md` in the new project. Choose the platform, aspect ratio, length, and style for that video. Mark footage that must appear with `must_use=yes` in the shot log. Record selected cuts in `EDIT_DECISIONS.csv`, then check coverage:

```powershell
python scripts/check_edit_plan.py projects/my-next-video
```

The skills under `.agents/skills/` guide the edit. Read `.agents/skills/video-editor/SKILL.md` first. Use `vlog-editor` for a visit or travel vlog, `video-semantic-search` to check narration against reviewed frames, and the other focused skills as needed. Open this Desktop folder as a workspace in Codex to make its `AGENTS.md` instructions available for future videos.

## Finish and review

```powershell
python scripts/verify_export.py "C:\path\to\final.mp4" --aspect 16:9 --decode
python scripts/review_contact_sheet.py "C:\path\to\final.mp4" --out projects/my-next-video/review/contact_sheet.jpg
```

Use the intended ratio, such as `9:16`, for a vertical video. Watch and listen to the actual export, especially edit points, captions, still durations, and the first and last seconds. `scripts/audio_finish.py` measures and normalizes the finished soundtrack.

## What is included

- **15 local skills** for story, assets, B-roll, motion, color, audio, semantic matching, review, formats, packaging, and local video inspection.
- **11 project templates** for briefs, shot logs, edit decisions, visual plans, reviews, and upload preparation.
- **General scripts** for media scanning, B-roll curation, reframing, thumbnails, chapters, audio finishing, and export verification.
- **Synthetic tests** that do not need the Kale Farm footage or any other real project media.

The Kale Farm footage, voice recordings, exports, and project-specific scripts remain in the original Kale Farm folder. This Desktop workspace has no runtime dependency on those files. See [TOOLING.md](TOOLING.md), [SKILL_SOURCES.md](SKILL_SOURCES.md), and [SKILL_TEST_REPORT.md](SKILL_TEST_REPORT.md) for tool choices and checks.
