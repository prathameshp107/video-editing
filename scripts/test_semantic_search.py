"""Offline regression check for evidence-based narration/visual matching."""
from __future__ import annotations

import hashlib
import importlib.util
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
AUDITOR = ROOT / ".agents" / "skills" / "video-semantic-search" / "scripts" / "audit_visual_beats.py"
spec = importlib.util.spec_from_file_location("audit_visual_beats", AUDITOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="semantic-video-test-") as temp:
        frame = Path(temp) / "reviewed_frame.jpg"
        Image.new("RGB", (64, 64), "#a35d31").save(frame)
        shot = {"name": "reviewed dish shot", "start": 5, "end": 10,
                "observed": ["dish"], "evidence_source": "human_verified",
                "frame": str(frame),
                "frame_sha256": hashlib.sha256(frame.read_bytes()).hexdigest()}
        beat = {"id": "dish_line", "start": 6, "end": 8,
                "critical": ["dish"]}
        assert module.audit([beat], [shot])[0]["status"] == "EXACT"
        wrong_time = {**beat, "start": 1, "end": 3}
        assert module.audit([wrong_time], [shot])[0]["status"] == "MISSING"
        frame.write_bytes(b"changed evidence")
        assert module.audit([beat], [shot])[0]["status"] == "MISSING"
    print("Semantic audit: aligned, mismatched, and changed-evidence cases passed")


if __name__ == "__main__":
    main()
