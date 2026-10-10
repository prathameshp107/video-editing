---
name: platform-package
description: Prepare source-backed cover art, title or caption, credits, and optional long-form chapters for YouTube videos, Shorts, Instagram Reels, or other delivery formats.
---

# Platform package

Use after a video is nearly final. Read the brief and inspect the actual export so the cover and copy promise what the video really shows. Fill `templates/PLATFORM_PACKAGE.md` for the intended platform. Write a clear first line, accurate title or caption, relevant credits, and only claims supported by the footage or creator. Do not invent prices, reviews, contact information, or sponsorship claims.

Create source-based cover art with `python scripts/make_thumbnail.py --input <image-or-video> --title <text> --profile wide|vertical|square|portrait-feed --out <image.jpg>`. A video accepts `--at <seconds>`. `wide` makes a 1280x720 cover; `vertical` makes 1080x1920. The profiles are editable production canvases, not permanent platform requirements. Inspect the result at full size and small-screen size; keep the key subject and words away from interface overlays for the chosen platform.

For a long-form video with chapters, write a plain-text `MM:SS Label` list and run `python scripts/check_chapters.py --video <final.mp4> --chapters <chapters.txt>`. This checks timing against the final export, not whether the label describes the right scene. Short-form packaging usually uses a concise caption and cover without chapters. Review each platform's current upload requirements before publishing; the skill prepares local assets and copy but does not upload or publish.
