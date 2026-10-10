"""Forwarding entry point to .agents/skills/video-semantic-search/scripts/index_media.py."""
import runpy
from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "video-semantic-search" / "scripts" / "index_media.py"

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
