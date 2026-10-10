"""Compare several moments from videos or stills before and after a color adjustment."""

import argparse
import io
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageStat

from video_profiles import font


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def frame(path: Path, at: float) -> Image.Image:
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return Image.open(path).convert("RGB")
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(at), "-i", str(path),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True,
    )
    return Image.open(io.BytesIO(result.stdout)).convert("RGB")


def metrics(image: Image.Image) -> dict:
    sample = image.resize((320, 180), Image.Resampling.LANCZOS)
    rgb = ImageStat.Stat(sample).mean
    hsv = ImageStat.Stat(sample.convert("HSV")).mean
    return {"mean_rgb": [round(v, 1) for v in rgb],
            "mean_brightness_0_255": round(hsv[2], 1),
            "mean_saturation_0_255": round(hsv[1], 1)}


def sample_times(path: Path, count: int, at: list[float] | None) -> list[float]:
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return [0.0]
    length = duration(path)
    if at:
        if any(time < 0 or time >= length for time in at):
            raise ValueError(f"Sample time outside {path.name} ({length:.2f}s)")
        return at
    # Avoid the first and last frames, which often contain fades or motion blur.
    return [round(length * (index + 1) / (count + 1), 3) for index in range(count)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--at", type=float, action="append", help="Exact time in each video; repeat as needed")
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if len(args.input) < 2 or not 1 <= args.samples <= 8:
        parser.error("Give at least two inputs and 1-8 samples")
    if any(not path.is_file() for path in args.input):
        parser.error("Every input must exist")
    columns = len(args.input)
    sampled = []
    for path in args.input:
        try:
            times = sample_times(path, args.samples, args.at)
        except ValueError as exc:
            parser.error(str(exc))
        sampled.append((path, [(time, frame(path, time)) for time in times]))
    rows = max(len(items) for _, items in sampled)
    tile_w, tile_h = 480, 330
    sheet = Image.new("RGB", (tile_w * columns, tile_h * rows), "#151719")
    draw = ImageDraw.Draw(sheet)
    label_font = font(size=20)
    report = []
    for column, (path, items) in enumerate(sampled):
        records = []
        for row, (time, image) in enumerate(items):
            x, y = column * tile_w, row * tile_h
            fit = image.copy()
            fit.thumbnail((tile_w, tile_h - 38), Image.Resampling.LANCZOS)
            sheet.paste(fit, (x + (tile_w - fit.width) // 2,
                              y + 38 + (tile_h - 38 - fit.height) // 2))
            draw.text((x + 8, y + 8), f"{path.name}  {time:.1f}s", fill="white", font=label_font)
            records.append({"sample_s": round(time, 2), **metrics(image)})
        report.append({"file": str(path.resolve()), "samples": records})
    args.out_dir.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out_dir / "comparison.jpg", quality=90)
    (args.out_dir / "measurements.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"inputs": len(report), "samples_per_video": args.samples,
                      "comparison": str((args.out_dir / "comparison.jpg").resolve())}, indent=2))


if __name__ == "__main__":
    main()
