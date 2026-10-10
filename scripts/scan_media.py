"""Inventory video, audio, and image files without changing the source media."""
import argparse
import csv
import json
from pathlib import Path
import subprocess

EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v",
              ".jpg", ".jpeg", ".png", ".webp", ".heic",
              ".wav", ".mp3", ".m4a", ".aac", ".flac"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}


def probe(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height,nb_frames:stream_tags=rotate:stream_side_data=rotation",
         "-of", "json", str(path)], capture_output=True, text=True)
    if result.returncode:
        return {"error": result.stderr.strip() or "ffprobe failed"}
    data = json.loads(result.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    rotation = video.get("tags", {}).get("rotate", 0)
    for item in video.get("side_data_list", []):
        if "rotation" in item:
            rotation = item["rotation"]
    width, height = video.get("width"), video.get("height")
    display_width, display_height = width, height
    if width and height and int(float(rotation)) % 180:
        display_width, display_height = height, width
    orientation = "unknown"
    if display_width and display_height:
        orientation = "portrait" if display_height > display_width else "landscape" if display_width > display_height else "square"
    duration = data.get("format", {}).get("duration")
    return {
        "duration_s": round(float(duration), 2) if duration else None,
        "width": width, "height": height, "rotation_deg": int(float(rotation)),
        "display_orientation": orientation,
        "has_audio": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if not args.media.is_dir():
        parser.error(f"media folder does not exist: {args.media}")
    media = args.media.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(media.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        row = {"filename": path.name, "relative_path": path.relative_to(media).as_posix(),
               "kind": "image" if path.suffix.lower() in IMAGE_EXTENSIONS else "media",
               "size_bytes": path.stat().st_size}
        row.update(probe(path))
        rows.append(row)
    (output / "media_inventory.json").write_text(json.dumps({"source": str(media), "files": rows}, indent=2), encoding="utf-8")
    fields = ["filename", "relative_path", "kind", "size_bytes", "duration_s", "width", "height",
              "rotation_deg", "display_orientation", "has_audio", "error"]
    with (output / "media_inventory.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Scanned {len(rows)} files into {output}")
    errors = [r for r in rows if "error" in r]
    if errors:
        print(f"Warning: {len(errors)} files could not be probed")


if __name__ == "__main__":
    main()

