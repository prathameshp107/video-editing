---
name: video-semantic-search
description: Match narration or dialogue to indexed footage and audit a video timeline for off-topic shots using local, free tools. Use for footage searches and voiceover-to-picture alignment; do not treat filename similarity as visual proof.
---

# Video Semantic Search

Use this when an edit needs the shot that best illustrates a spoken line, or when checking that the finished timeline follows the narration.

1. Run `scripts/index_media.py --media-dir <source> --out <review>` to sample local video and create a contact sheet plus `shot_index.json`. Add `--transcribe` only when a local cached faster-whisper model is available. Review the frames and write short **observed** descriptions and tags for each shot, with source file and source time. Keep claims from the creator separate from things visible or audible in the file.
2. Divide the script or transcript into timed beats. Map each beat to visual concepts, including location, action, object, and story role. When timing is unknown, estimate from a scratch voice read, then revise after audio is generated.
3. Search `shot_index.json` with `scripts/search_index.py --index <shot_index.json> --query <spoken beat>`. Rank meaning and story position above matching file names. Where a line makes a claim that is not visible, choose a relevant contextual shot and mark the claim as narration-only.
4. Split the **actual narration audio** into short visual beats, using TTS part boundaries or word timestamps when available. A line containing both "counter" and "chicken dish" needs separate beats. Use the rendered audio placement times, not only the planned script windows.
5. Run `scripts/match_timeline.py` for fast candidate search only. It can never certify alignment because broad categories such as "food" can mask a precise mismatch.
6. For the candidate shots, inspect rendered frames and record exact visible objects/actions with `human_verified` evidence and a SHA-256 of each reviewed frame. Run `scripts/audit_visual_beats.py --beats <beats.json> --evidence <visual_evidence.json> --out <report.json>`. Treat missing critical evidence as `MISSING` and missing supporting detail as `PARTIAL`. Keep narration-only claims explicit.
7. Move the narration beat or choose a different shot, then rerun the audit and check the rendered video at the beat boundaries. Leave source footage unchanged.

Use the beat/evidence/critical-requirement method with vocabulary specific to each project. Do not assume a shot contains an object or action because its filename, transcript, or editorial label says so. Use only free local processing for this repository.

**Note for open-source users:** The concept vocabulary in `.agents/skills/video-semantic-search/scripts/match_timeline.py` (the `CONCEPTS` dictionary) is tuned for Indian food and travel vlogs from the original creator's project. For a different video type or language, edit that dictionary to reflect the subjects, actions, and locations that appear in your footage. The audit logic and evidence system work for any vocabulary.
