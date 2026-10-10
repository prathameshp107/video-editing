# Skill sources and installation choices

Checked on 9 October 2026. The repository keeps editorial skills local and uses the installed framework skills for implementation.

| Source | Used for | Status |
| --- | --- | --- |
| [Watch by bradautomates](https://github.com/bradautomates/claude-video/tree/main/skills/watch) | Timestamped frames and native captions from local or public reference video | Installed in `.agents/skills/watch` and Codex's global skills under MIT; configured for free local use without an API key |
| [Official Remotion agent skills](https://github.com/remotion-dev/agent-plugin) | React video compositions, graphics, captions, transitions, and rendering | Already available as a Codex plugin; no duplicate copy in this repo |
| [Official HyperFrames skills](https://github.com/heygen-com/hyperframes/tree/main/skills) | HTML video compositions, creative direction, media use, and motion | `general-video` and its core skills installed for the agent; use the HyperFrames entry skill |
| Local `asset-plan`, `story-editor`, `motion-overlay`, `cut-audit`, `render-review`, `style-memory` | Repeatable decisions for our footage-based vlogs | Created in this repository |

The public GitHub ecosystem also has community Remotion motion-graphics skills. The official Remotion plugin and HyperFrames motion skills already cover the needed implementation, so this kit does not install overlapping community packs. The local `motion-overlay` skill records how a graphic should support a vlog and routes implementation to the official framework skill.

The OpenAI `speech` and `transcribe` skills were removed from this kit after the creator specified free-only operation: their live workflows require API usage that may be billed. Watch's optional Gemini, Groq, and OpenAI cloud modes are not configured here. Local WhisperX is free but was not installed because its Windows setup is unverified and requires a large model download; native captions and visual frame inspection work now.
