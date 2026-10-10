# Skill sources and installation choices

Last reviewed: October 2026. The repository keeps editorial skills local and uses the installed framework skills for implementation.

| Source | Used for | Status |
| --- | --- | --- |
| [Watch by bradautomates](https://github.com/bradautomates/claude-video/tree/main/skills/watch) | Timestamped frames and native captions from local or public reference video | Installed in `.agents/skills/watch` under MIT; configured for free local use without an API key |
| [Official Remotion agent skills](https://github.com/remotion-dev/agent-plugin) | React video compositions, graphics, captions, transitions, and rendering | Available as an agent plugin; no duplicate copy in this repo |
| [Official HyperFrames skills](https://github.com/heygen-com/hyperframes/tree/main/skills) | HTML video compositions, creative direction, media use, and motion | `general-video` and its core skills installed for the agent; use the HyperFrames entry skill |
| [Resemble AI Chatterbox](https://github.com/resemble-ai/chatterbox) | Local voice narration with a consented reference recording | `voiceover-generator` uses the local runtime and model checkpoint in Git-ignored `private/`; no paid API; any compatible language checkpoint may be used |
| Local `asset-plan`, `story-editor`, `motion-overlay`, `cut-audit`, `render-review`, `style-memory` | Repeatable editorial decisions for footage-based videos | Created in this repository |

The public GitHub ecosystem also has community Remotion motion-graphics skills. The official Remotion plugin and HyperFrames motion skills already cover the needed implementation, so this kit does not install overlapping community packs. The local `motion-overlay` skill records how a graphic should support a video and routes implementation to the official framework skill.

The OpenAI `speech` and `transcribe` skills were removed from this kit after the creator specified free-only operation: their live workflows require API usage that may be billed. Watch's optional Gemini, Groq, and OpenAI cloud modes are not configured here. Local WhisperX is free but requires a separate installation (large model download, ~1.5 GB); native captions and visual frame inspection work without it.

## For open-source contributors

This kit is agent-agnostic. It works with Antigravity IDE, Claude Code, OpenAI Codex, and any system that loads `.agents/skills/` skill directories and `AGENTS.md` rules files. To add a skill from the public ecosystem, place its `SKILL.md` and any helper scripts under `.agents/skills/<name>/`, confirm it uses only free local tools, and add a row to this file.
