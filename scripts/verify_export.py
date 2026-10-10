"""Check a rendered video's stream format and optionally decode every frame."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--aspect", help="Expected display aspect, for example 16:9 or 9:16")
    parser.add_argument("--decode", action="store_true", help="Decode the full file to catch corrupt frames")
    args = parser.parse_args()
    if not args.video.is_file():
        parser.error(f"video does not exist: {args.video}")
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate",
                             "-of", "json", str(args.video)], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or "ffprobe failed")
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video:
        raise SystemExit("No video stream found")
    width, height = video["width"], video["height"]
    if args.aspect:
        try:
            a, b = (float(x) for x in args.aspect.split(":"))
        except ValueError:
            parser.error("--aspect must be like 16:9")
        if b <= 0 or abs(width / height - a / b) > .015:
            raise SystemExit(f"Aspect mismatch: got {width}x{height}, expected {args.aspect}")
    duration = float(data["format"]["duration"])
    if duration <= 0:
        raise SystemExit("Duration is zero")
    if args.decode:
        check = subprocess.run(["ffmpeg", "-v", "error", "-i", str(args.video), "-f", "null", "-"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if check.returncode or check.stderr.strip():
            raise SystemExit(f"Decode failed: {check.stderr.strip()}")
    print(json.dumps({"file": str(args.video.resolve()), "duration_s": round(duration, 2),
                      "width": width, "height": height, "fps": video.get("avg_frame_rate"),
                      "video_codec": video.get("codec_name"),
                      "audio": any(s.get("codec_type") == "audio" for s in streams),
                      "full_decode_ok": args.decode}, indent=2))


if __name__ == "__main__":
    main()

