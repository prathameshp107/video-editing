"""Reframe any source range for a wide, vertical, square, or portrait-feed canvas."""

import argparse
import json
import subprocess
from pathlib import Path

from video_profiles import PROFILES, dimensions, video_filter


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float, help="Omit to use the remainder of the source")
    parser.add_argument("--profile", choices=PROFILES, default="vertical")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--mode", choices=("fit", "crop"), default="fit")
    parser.add_argument("--focus-x", type=float, default=0.5)
    parser.add_argument("--focus-y", type=float, default=0.5)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Missing input: {args.input}")
    if args.input.resolve() == args.output.resolve():
        parser.error("Output must differ from input")
    if args.start < 0 or (args.duration is not None and args.duration <= 0):
        parser.error("Use a nonnegative start and positive duration")
    try:
        width, height = dimensions(args.profile, args.width, args.height)
        vf = video_filter(width, height, args.mode, args.focus_x, args.focus_y, args.fps)
    except ValueError as exc:
        parser.error(str(exc))
    source = probe(args.input)
    source_duration = float(source["format"]["duration"])
    remaining = source_duration - args.start
    actual_duration = args.duration if args.duration is not None else remaining
    if remaining <= 0 or actual_duration > remaining + 0.1:
        parser.error(f"Requested range exceeds source duration {source_duration:.2f}s")
    has_audio = any(stream["codec_type"] == "audio" for stream in source["streams"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(args.start),
           "-i", str(args.input), "-t", str(actual_duration), "-filter_complex", vf,
           "-map", "[v]"]
    if has_audio:
        cmd += ["-map", "0:a:0", "-c:a", "aac", "-b:a", "160k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(args.fps),
            "-movflags", "+faststart", str(args.output)]
    subprocess.run(cmd, check=True)
    result = probe(args.output)
    video = next(stream for stream in result["streams"] if stream["codec_type"] == "video")
    summary = {"output": str(args.output.resolve()), "source_start_s": args.start,
               "duration_s": float(result["format"]["duration"]), "width": video["width"],
               "height": video["height"], "profile": args.profile, "mode": args.mode,
               "audio": has_audio}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
