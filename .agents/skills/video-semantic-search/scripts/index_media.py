"""Build a local shot review sheet and optional speech transcript from source videos."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

VIDEO = {".mp4", ".mov", ".m4v", ".mkv", ".webm"}
IMAGE = {".jpg", ".jpeg", ".png", ".webp"}


def probe(path: Path) -> dict:
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,width,height", "-of", "json", str(path)],
                       check=True, capture_output=True, text=True)
    data = json.loads(p.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    return {"duration": float(data["format"]["duration"]),
            "width": video.get("width"), "height": video.get("height"),
            "has_audio": any(s.get("codec_type") == "audio" for s in data.get("streams", []))}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--media-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--transcribe", action="store_true", help="Use installed local faster-whisper")
    p.add_argument("--language", default=None)
    args = p.parse_args()
    paths = sorted(x for x in args.media_dir.rglob("*") if x.suffix.casefold() in VIDEO | IMAGE)
    args.out.mkdir(parents=True, exist_ok=True)
    model = None
    if args.transcribe:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8", local_files_only=True)
    records = []
    tiles = []
    for i, path in enumerate(paths):
        is_image = path.suffix.casefold() in IMAGE
        if is_image:
            with Image.open(path) as im:
                meta = {"duration": 0.0, "width": im.width, "height": im.height,
                        "has_audio": False}
        else:
            meta = probe(path)
        samples = []
        for j, fraction in enumerate((.5,) if is_image else (.2, .5, .8)):
            stamp = max(0, meta["duration"] * fraction)
            dest = args.out / f"{i:03d}_{j}.jpg"
            if is_image:
                with Image.open(path) as im:
                    frame = im.convert("RGB")
                    frame.thumbnail((360, 202))
                    tile = Image.new("RGB", (360, 202), "black")
                    tile.paste(frame, ((360-frame.width)//2, (202-frame.height)//2))
                    tile.save(dest)
            else:
                subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                                "-ss", str(stamp), "-i", str(path), "-frames:v", "1",
                                "-vf", "scale=360:202:force_original_aspect_ratio=decrease:"
                                       "force_divisible_by=2,pad=360:202:(ow-iw)/2:(oh-ih)/2", str(dest)],
                               check=True)
            samples.append({"time": round(stamp, 2), "frame": str(dest)})
            with Image.open(dest) as im:
                tiles.append((path.name, round(stamp, 1), im.convert("RGB")))
        transcript = []
        if model is not None and meta["has_audio"]:
            segments, _ = model.transcribe(str(path), language=args.language,
                                            beam_size=3, vad_filter=True)
            transcript = [{"start": round(s.start, 2), "end": round(s.end, 2),
                           "text": s.text.strip()} for s in segments]
        records.append({"path": str(path.resolve()), **meta, "samples": samples,
                        "transcript": transcript, "visual_description": "",
                        "observed_tags": []})
    sheet = Image.new("RGB", (1080, ((len(tiles)+2)//3)*228), "#111111")
    d = ImageDraw.Draw(sheet)
    for k, (name, stamp, im) in enumerate(tiles):
        x, y = (k%3)*360, (k//3)*228
        sheet.paste(im, (x, y))
        d.text((x+4, y+205), f"{name[:43]} @ {stamp}s", fill="white")
    sheet.save(args.out / "contact_sheet.jpg", quality=88)
    (args.out / "shot_index.json").write_text(json.dumps(records, ensure_ascii=False, indent=2),
                                                encoding="utf-8")
    print(f"Indexed {len(records)} videos; review {args.out / 'contact_sheet.jpg'}")


if __name__ == "__main__":
    main()
