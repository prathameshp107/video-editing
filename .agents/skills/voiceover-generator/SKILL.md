---
name: voiceover-generator
description: Generate narration locally in a consented speaker's voice using the bundled Chatterbox TTS model. Works with any language supported by the installed checkpoint. Audio finishing and soundtrack mixing are separate steps.
---

# Voiceover generator

Use this skill when the creator wants spoken narration in a voice they supplied or authorized. The consented reference recording goes under `private/voice/`; keep the original beside it. The model and local runtime live under `private/models/` and `private/voice_env/`. All private files are excluded from Git. Never publish, commit, or share the reference or model files with a project export.

Write the narration in short, speakable sentences. Check pronunciation of names, places, and technical terms before generating. Generate a new WAV without overwriting previous takes:

```powershell
# Windows (PowerShell)
.\private\voice_env\Scripts\python.exe scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/voiceover_take_01.wav

# macOS / Linux
python3 scripts/voiceover_generate.py --text-file projects/my-video/voiceover.txt --out projects/my-video/work/voiceover_take_01.wav
```

Use `--dry-run` first to verify the reference path, model directory, text split, and output path before loading the model. For a different consented speaker, prepare a clean 3–60 second speech-only recording with `scripts/prepare_voice_reference.py`, then pass it with `--reference`. A noisy recording or music under speech can transfer artifacts to the output. Listen to every generated take for missing words, unnatural delivery, and mispronounced names. Regenerate only weak sentences and keep chosen takes in the project folder. Split long scripts into scene-sized files so timing can be adjusted against footage.

The bundled Chatterbox checkpoint is language-specific to whichever model is placed in `private/models/`. Confirm the model supports your target language and run a short test before a full script. A Hindi checkpoint does not produce correct Marathi or English; install a compatible multilingual checkpoint and verify it. `scripts/voiceover_generate.py` does not place narration on the video timeline. Use `video-semantic-search` for picture alignment and `audio-finisher` after the voice, music, and effects are mixed. All processing stays local and uses free software.

For open-source contributors: the `private/` folder is intentionally Git-ignored. To use this skill in a new workspace, obtain a consented reference recording, place a compatible Chatterbox model checkpoint under `private/models/`, create a virtual environment with the model's dependencies under `private/voice_env/`, and run `--dry-run` to confirm the paths.
