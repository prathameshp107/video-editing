"""Audit timed narration against a human-reviewed shot index in a timeline.

Usage: python match_timeline.py --lines narration.json --timeline timeline.json --out report.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONCEPTS = {
    "travel": ["road", "drive", "driving", "journey", "safar", "रास्त", "सफ़र", "सफर", "सड़क", "गाड़ी", "पुणे", "सासवड", "हरियाली", "green", "flower"],
    "arrival": ["arrival", "approach", "entrance", "entry", "gate", "parking", "एंट्रेंस", "एंट्री", "पहुँच", "पास", "करीब"],
    "grounds": ["grounds", "tree", "farm", "place", "atmosphere", "होटल", "पेड़", "जगह", "माहौल", "फार्म", "खुली"],
    "history": ["old hotel", "earlier", "पुरानी", "पहले", "बदल", "छोटी", "तस्वीर"],
    "menu": ["menu", "prices", "banner", "मेन्यू", "दाम", "कीमत"],
    "dining": ["dining", "restaurant", "counter", "बैठने", "काउंटर", "रेस्तराँ"],
    "food": ["food", "dish", "meal", "chicken", "thali", "bites", "थाली", "चिकन", "खाना", "प्लेट", "पीस", "सर्विंग"],
    "thali": ["thali", "थाली", "full meal", "पूरी"],
    "curry": ["curry", "gravy", "rassa", "tari", "रस्सा", "करी", "आलणी", "मसाला"],
    "bread": ["bread", "bhakri", "roti", "भाकरी", "रोटी"],
    "rice": ["rice", "चावल", "इंद्रायणी"],
    "people": ["people", "sharing", "table", "companion", "साथ", "सब", "एक-दूसरे", "टेबल"],
    "closeup": ["close-up", "close up", "नज़दीक", "करीब से", "क्लोज़", "पास ले"],
    "ending": ["closing", "last bites", "आख़िरी", "मिलते", "बाय-बाय"],
}


def tags(s: str) -> set[str]:
    s = s.casefold()
    return {name for name, words in CONCEPTS.items() if any(w in s for w in words)}


def audit(lines: list[dict], starts: dict[str, float], total: float) -> list[dict]:
    shots = sorted(((float(t), name) for name, t in starts.items()), key=lambda x: x[0])
    spans = [(t, shots[i + 1][0] if i + 1 < len(shots) else total, name)
             for i, (t, name) in enumerate(shots)]
    result = []
    for line in lines:
        a, b = float(line["start"]), float(line["end"])
        if not 0 <= a < b <= total + .5:
            raise ValueError(f"Invalid beat: {line}")
        line_tags = tags(line["text"])
        hits = []
        supported_seconds = 0.0
        for x, y, name in spans:
            overlap = max(0.0, min(b, y) - max(a, x))
            if overlap <= 0:
                continue
            shot_tags = tags(name)
            common = line_tags & shot_tags
            if common:
                supported_seconds += overlap
            score = round(overlap / (b - a) * (len(common) / max(1, len(line_tags))), 3)
            hits.append({"shot": name, "seconds": round(overlap, 2), "shared": sorted(common), "score": score})
        hits.sort(key=lambda h: h["score"], reverse=True)
        coverage = round(supported_seconds / (b-a), 3)
        result.append({"id": line.get("id"), "start": a, "end": b,
                       "narration_tags": sorted(line_tags), "best_shots": hits[:5],
                       "supported_picture_fraction": coverage,
                       "status": "review" if coverage < .4 else "candidate_only"})
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lines", type=Path, required=True)
    p.add_argument("--timeline", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    lines = json.loads(args.lines.read_text(encoding="utf-8"))
    if isinstance(lines, dict) and "placed" in lines:
        lines = lines["placed"]
    timeline = json.loads(args.timeline.read_text(encoding="utf-8"))
    result = audit(lines, timeline["shot_starts"], float(timeline["seconds"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(result)} beats: {sum(r['status']=='candidate_only' for r in result)} candidate matches, "
          f"{sum(r['status']=='review' for r in result)} to review")
    for r in result:
        if r["status"] == "review":
            print(f"  {r['id']}: review {r['start']:.1f}-{r['end']:.1f}s — "
                  f"{r['best_shots'][0]['shot'] if r['best_shots'] else 'no shot'}")


if __name__ == "__main__":
    main()
