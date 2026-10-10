"""Build a source-linked B-roll pack directly from video and still-image ranges."""

import argparse
import csv
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from video_profiles import PROFILES, dimensions, font, video_filter


FIELDS = ("source", "start_s", "duration_s", "filename", "category", "usage_note",
          "rights", "source_url", "media_type", "rotation")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile", choices=PROFILES, default="wide")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--mode", choices=("fit", "crop"), default="fit")
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()
    try:
        width, height = dimensions(args.profile, args.width, args.height)
    except ValueError as exc:
        parser.error(str(exc))
    with args.manifest.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or any(field not in reader.fieldnames for field in FIELDS[:7]):
            parser.error("Manifest needs source,start_s,duration_s,filename,category,usage_note,rights")
        choices = list(reader)
    if not choices:
        parser.error("Manifest is empty")
    names = [Path(row["filename"]).name for row in choices]
    if len(set(names)) != len(names) or any(not name.lower().endswith(".mp4") for name in names):
        parser.error("Output filenames must be unique .mp4 basenames")
    output = args.output.resolve()
    clips = output / "clips"
    clips.mkdir(parents=True, exist_ok=True)
    stale = sorted(path.name for path in clips.glob("*.mp4") if path.name not in names)
    if stale:
        parser.error("Output contains unlisted clips; use a new folder or review: " + ", ".join(stale))
    catalog = []
    thumbs = []
    for row in choices:
        source = Path(row["source"])
        if not source.is_absolute():
            source = args.manifest.parent / source
        source = source.resolve()
        if not source.is_file():
            parser.error(f"Missing source: {source}")
        start, length = float(row["start_s"]), float(row["duration_s"])
        if start < 0 or length <= 0:
            parser.error(f"Invalid range for {source.name}")
        still = source.suffix.lower() in IMAGE_SUFFIXES
        media_type = "photo motion" if still else (row.get("media_type") or "video")
        rotation = row.get("rotation") or "auto"
        if rotation not in ("auto", "none", "cw", "ccw", "180"):
            parser.error(f"Invalid rotation for {source.name}: {rotation}")
        if still and start != 0:
            parser.error(f"Still-image start must be zero: {source.name}")
        if not still:
            available = float(probe(source)["format"]["duration"])
            if start + length > available + 0.1:
                parser.error(f"Range exceeds {source.name} duration {available:.2f}s")
        if not row["rights"].strip():
            parser.error(f"Rights field is required for {source.name}")
        target = clips / Path(row["filename"]).name
        vf = video_filter(width, height, args.mode, fps=args.fps, rotation=rotation)
        if still:
            step = 0.06 / (length * args.fps)
            vf = vf[:-3] + (
                "[base];[base]zoompan="
                f"z='min(1+on*{step:.8f},1.06)':"
                "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d=1:s={width}x{height}:fps={args.fps},format=yuv420p[v]"
            )
        command = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        if still:
            command += ["-loop", "1", "-framerate", str(args.fps), "-i", str(source)]
        else:
            if rotation != "auto":
                command += ["-noautorotate", "-display_rotation", "0"]
            command += ["-ss", str(start), "-i", str(source)]
        command += ["-t", str(length), "-filter_complex", vf, "-map", "[v]"]
        has_audio = not still and any(s["codec_type"] == "audio" for s in probe(source)["streams"])
        if has_audio:
            command += ["-map", "0:a:0", "-c:a", "aac", "-b:a", "160k", "-ar", "48000"]
        command += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-r", str(args.fps), "-movflags", "+faststart", str(target)]
        subprocess.run(command, check=True)
        result = probe(target)
        video = next(s for s in result["streams"] if s["codec_type"] == "video")
        catalog.append({"file": f"clips/{target.name}", "category": row["category"],
                        "duration_s": round(float(result["format"]["duration"]), 2),
                        "width": video["width"], "height": video["height"],
                        "original_source": str(source), "source_start_s": start,
                        "usage_note": row["usage_note"], "rights": row["rights"],
                        "source_url": row.get("source_url", ""), "media_type": media_type})
        thumb = output / "_broll_thumb.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(length / 2), "-i", str(target),
                        "-frames:v", "1", str(thumb)], check=True)
        with Image.open(thumb) as image:
            thumbs.append((target.name, image.convert("RGB").copy()))
        thumb.unlink()
    with (output / "catalog.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=catalog[0].keys())
        writer.writeheader()
        writer.writerows(catalog)
    tile_w, tile_h, columns = 400, 290, 3
    sheet = Image.new("RGB", (tile_w * columns, tile_h * ((len(thumbs) + 2) // 3)), "#151719")
    draw = ImageDraw.Draw(sheet)
    label_font = font(size=19)
    for index, (name, image) in enumerate(thumbs):
        x, y = (index % columns) * tile_w, (index // columns) * tile_h
        image.thumbnail((tile_w, tile_h - 35), Image.Resampling.LANCZOS)
        sheet.paste(image, (x + (tile_w - image.width) // 2, y + 35 + (tile_h - 35 - image.height) // 2))
        draw.text((x + 8, y + 5), name, font=label_font, fill="white")
    sheet.save(output / "contact_sheet.jpg", quality=90)
    (output / "README.md").write_text(
        f"# B-roll pack\n\n{len(catalog)} clips in {width}x{height} ({args.profile}, {args.mode}). "
        "Preview `contact_sheet.jpg`; `catalog.csv` records source paths, timecodes, rights, and notes. "
        "Original files were not changed. Clip audio, if present, comes from the source; no music or titles were added.\n",
        encoding="utf-8",
    )
    print(json.dumps({"clips": len(catalog), "output": str(output), "profile": args.profile,
                      "dimensions": [width, height]}, indent=2))


if __name__ == "__main__":
    main()
