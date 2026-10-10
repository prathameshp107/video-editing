"""Check that a long-form chapter list is ordered and fits the actual export."""

import argparse
import json
import re
import subprocess
from pathlib import Path


def seconds(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    if len(parts) not in (2, 3) or any(part > 59 for part in parts[1:]):
        raise ValueError(f"Invalid timestamp: {value}")
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--chapters", type=Path, required=True,
                        help="Plain text, one 'MM:SS Label' or 'HH:MM:SS Label' per line")
    args = parser.parse_args()
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "json", str(args.video)], capture_output=True, text=True, check=True)
    duration = float(json.loads(result.stdout)["format"]["duration"])
    chapters = []
    for line in args.chapters.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)", line.strip())
        if not match:
            parser.error(f"Bad chapter line: {line}")
        try:
            at = seconds(match.group(1))
        except ValueError as exc:
            parser.error(str(exc))
        chapters.append((at, match.group(2)))
    if not chapters or chapters[0][0] != 0:
        parser.error("First chapter must start at 00:00")
    if any(right[0] <= left[0] for left, right in zip(chapters, chapters[1:])):
        parser.error("Chapter times must increase strictly")
    if chapters[-1][0] >= duration:
        parser.error(f"Last chapter starts after the video ends ({duration:.2f}s)")
    print(json.dumps({"chapters": len(chapters), "video_duration_s": round(duration, 2),
                      "last_chapter_s": chapters[-1][0], "timing_valid": True}, indent=2))


if __name__ == "__main__":
    main()
