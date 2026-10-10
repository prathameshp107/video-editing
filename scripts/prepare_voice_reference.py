"""Convert a selected clean portion of a voice recording to 24 kHz mono WAV."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--duration", type=float, default=23)
    args = p.parse_args()
    if not args.input.is_file() or args.output.exists():
        p.error("input must exist and output must be a new path")
    if args.start < 0 or not 3 <= args.duration <= 60:
        p.error("start must be nonnegative; duration must be 3–60 seconds")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(args.start),
                    "-i", str(args.input), "-t", str(args.duration),
                    "-vn", "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le",
                    str(args.output)], check=True)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
