"""Forwarding entry point to .agents/skills/video-semantic-search/scripts/match_timeline.py."""
import sys
from pathlib import Path
import importlib.util

TARGET = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "video-semantic-search" / "scripts" / "match_timeline.py"
if str(TARGET.parent) not in sys.path:
    sys.path.insert(0, str(TARGET.parent))

spec = importlib.util.spec_from_file_location("match_timeline", TARGET)
_mod = importlib.util.module_from_spec(spec)
sys.modules["match_timeline"] = _mod
spec.loader.exec_module(_mod)

CONCEPTS = getattr(_mod, "CONCEPTS", {})
tags = getattr(_mod, "tags", None)
audit = getattr(_mod, "audit", None)

if __name__ == "__main__":
    _mod.main()
