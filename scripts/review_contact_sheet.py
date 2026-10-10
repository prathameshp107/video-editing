"""Make an evenly sampled contact sheet from a rendered video using FFmpeg."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--rows", type=int, default=4)
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error(f"video does not exist: {args.video}")
    if args.columns < 1 or args.rows < 1:
        parser.error("columns and rows must be positive")
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "json", str(args.video)], capture_output=True, text=True, check=True)
    duration = float(json.loads(result.stdout)["format"]["duration"])
    cells = args.columns * args.rows
    rate = cells / max(duration, .1)
    width, height = 480, 270
    filters = (f"fps={rate:.8f},"
               f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
               f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
               f"tile={args.columns}x{args.rows}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(args.video),
                    "-vf", filters, "-frames:v", "1", str(args.out)], check=True)
    print(f"Review sheet: {args.out.resolve()} ({cells} evenly spaced samples)")


if __name__ == "__main__":
    main()
