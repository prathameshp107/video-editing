# Skill test report

This standalone kit is checked with synthetic media so no existing video project is required.

Run these from the kit root:

```powershell
python scripts/test_cross_format.py
python scripts/test_semantic_search.py
```

`test_cross_format.py` exercises B-roll from raw video and a still, audio normalization, color contact sheets, covers in wide/vertical/square/portrait-feed canvases, chapter validation, and aspect-ratio conversion. It checks resulting dimensions and decodes video outputs.

`test_semantic_search.py` checks three outcomes: a beat with reviewed frame evidence is `EXACT`; the same beat at the wrong time is `MISSING`; and a changed frame invalidates its saved SHA-256 evidence. This is a structural regression test, not automatic visual recognition. For a real edit, a person must review frames and label what is actually visible.

All workflows use local Python, Pillow, FFmpeg, and FFprobe. No paid API or private media is needed for these checks. Framework-specific compositions using Remotion or HyperFrames require their separate runtime and project setup.

The `voiceover-generator` was also tested with the creator's authorized 23-second reference and the local Chatterbox checkpoint. A short narration line rendered as a 24 kHz mono WAV using CPU inference. A `--dry-run` check validates the input paths and text split without loading the model. The private recording, model weights, and voice runtime are excluded from Git. The same workflow applies to any language-specific or multilingual Chatterbox checkpoint placed under `private/`.

