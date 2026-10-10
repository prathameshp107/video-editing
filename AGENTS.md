# Video Editing Kit instructions

For any video in this repository, read `.agents/skills/video-editor/SKILL.md` first. It routes long-form YouTube, vlogs, Shorts, Instagram Reels, and other formats to the relevant focused skills. Read `.agents/skills/vlog-editor/SKILL.md` for a visit or travel vlog specifically. Use the project brief and shot log to establish story and required media before building a timeline.

When using Remotion or HyperFrames, read the installed skill for that framework and follow its project contract. Do not assume either package or CLI is installed because its skill is available. For footage or reference-video inspection, use the local `watch` skill with `--engine local --no-whisper` so it does not call a paid API or upload private video. For reference videos (Instagram Reels, YouTube Shorts, competitor videos), execute a full forensic post-mortem across camera angles, typography, motion graphics, pacing, and sound design. Native captions remain available where the source provides them.

For new narration in the creator's voice, read `.agents/skills/voiceover-generator/SKILL.md`. The reference recording, model checkpoint, and local runtime are in Git-ignored `private/`. Keep generated takes in the current project. Never commit or publish the private reference or model. The skill supports any language for which a compatible Chatterbox checkpoint is available.

The creator requested free-only skills and workflows. Do not enable a paid cloud video, transcription, voice, image, or music service as part of this kit. Use local tools or free assets with a verified license; ask only if a future task explicitly calls for a service that may cost money.

Keep source media untouched. Work in the project folder. Do not commit footage, generated previews, or exports. Check `must_use=yes` rows against the final edit plan before delivery. Verify the actual rendered file and report its format, duration, and any known limits.
