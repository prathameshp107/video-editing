"""Search a reviewed local shot index with English or Hindi story concepts."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from match_timeline import tags


def rank(index: list[dict], query: str) -> list[dict]:
    qtags = tags(query)
    words = {w for w in re.findall(r"[\w\u0900-\u097f]+", query.casefold()) if len(w) > 2}
    hits = []
    for item in index:
        desc = str(item.get("visual_description", ""))
        itags = set(item.get("observed_tags", [])) | tags(desc)
        body = desc.casefold()
        shared = qtags & itags
        keyword = sum(w in body for w in words)
        score = len(shared)*3 + keyword + (3 if "thali" in shared else 0)
        if score:
            hits.append({"path": item["path"], "description": desc,
                         "score": score, "shared_concepts": sorted(shared),
                         "preview": item.get("samples", [{}])[0].get("frame")})
    return sorted(hits, key=lambda x: (-x["score"], x["path"]))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--top", type=int, default=5)
    args = p.parse_args()
    index = json.loads(args.index.read_text(encoding="utf-8"))
    hits = rank(index, args.query)[:args.top]
    print(json.dumps(hits, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
