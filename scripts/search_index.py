"""Forwarding entry point to .agents/skills/video-semantic-search/scripts/search_index.py."""
import sys
from pathlib import Path
import importlib.util

TARGET = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "video-semantic-search" / "scripts" / "search_index.py"
if str(TARGET.parent) not in sys.path:
    sys.path.insert(0, str(TARGET.parent))

spec = importlib.util.spec_from_file_location("search_index", TARGET)
_mod = importlib.util.module_from_spec(spec)
sys.modules["search_index"] = _mod
spec.loader.exec_module(_mod)

rank = getattr(_mod, "rank", None)

if __name__ == "__main__":
    _mod.main()
