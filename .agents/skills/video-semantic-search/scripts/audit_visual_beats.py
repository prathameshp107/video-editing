"""Verify timed narration beats against reviewed frame evidence.

Only human-verified or detector-verified observations count. Filenames and
story-role labels never prove a visual claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _required(entry):
    return {"id": entry, "min_seconds": .3} if isinstance(entry, str) else {
        "id": entry["id"], "min_seconds": float(entry.get("min_seconds", .3))}


def audit(beats: list[dict], shots: list[dict]) -> list[dict]:
    report = []
    for beat in beats:
        a, b = float(beat["start"]), float(beat["end"])
        if not a < b:
            raise ValueError(f"Invalid beat timing: {beat.get('id')}")
        checked = []
        for kind in ("critical", "support"):
            for raw in beat.get(kind, []):
                req = _required(raw)
                evidence = []
                seconds = 0.0
                for shot in shots:
                    overlap = max(0.0, min(b, float(shot["end"])) - max(a, float(shot["start"])))
                    if overlap <= 0 or req["id"] not in shot.get("observed", []):
                        continue
                    if shot.get("evidence_source") not in ("human_verified", "detector_verified"):
                        continue
                    frame = shot.get("frame")
                    digest = shot.get("frame_sha256")
                    if not frame or not digest or not Path(frame).is_file():
                        continue
                    if hashlib.sha256(Path(frame).read_bytes()).hexdigest() != digest:
                        continue
                    seconds += overlap
                    evidence.append({"shot": shot["name"], "overlap_seconds": round(overlap, 2),
                                     "frame": frame})
                checked.append({"kind": kind, "concept": req["id"],
                                "observed_seconds": round(seconds, 2),
                                "required_seconds": req["min_seconds"],
                                "pass": seconds >= req["min_seconds"], "evidence": evidence})
        missing_critical = [x["concept"] for x in checked if x["kind"] == "critical" and not x["pass"]]
        missing_support = [x["concept"] for x in checked if x["kind"] == "support" and not x["pass"]]
        status = "MISSING" if missing_critical else "PARTIAL" if missing_support or not checked else "EXACT"
        report.append({"id": beat["id"], "start": a, "end": b,
                       "text": beat.get("text", ""), "status": status,
                       "missing_critical": missing_critical, "missing_support": missing_support,
                       "narration_only": beat.get("narration_only", []), "checks": checked})
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--beats", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    beats = json.loads(args.beats.read_text(encoding="utf-8"))
    shots = json.loads(args.evidence.read_text(encoding="utf-8"))["shots"]
    result = audit(beats, shots)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {status: sum(x["status"] == status for x in result)
              for status in ("EXACT", "PARTIAL", "MISSING")}
    print(f"{len(result)} beats: {counts}")
    for x in result:
        if x["status"] != "EXACT":
            print(f"  {x['id']} {x['start']:.2f}-{x['end']:.2f}: {x['status']}"
                  f" critical={x['missing_critical']} support={x['missing_support']}")


if __name__ == "__main__":
    main()
