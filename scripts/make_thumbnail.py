"""Create a source-based cover in wide, vertical, square, or portrait-feed format."""

import argparse
import io
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from video_profiles import COVER_PROFILES, dimensions, font


def load_image(path: Path, at: float) -> Image.Image:
    if path.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"}:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(at), "-i", str(path),
             "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
            capture_output=True, check=True,
        )
        return Image.open(io.BytesIO(result.stdout)).convert("RGB")
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def fitted_font(draw: ImageDraw.ImageDraw, text: str, max_width: int,
                max_size: int) -> ImageFont.FreeTypeFont:
    for size in range(max_size, 18, -2):
        candidate = font(bold=True, size=size)
        if draw.textbbox((0, 0), text, font=candidate)[2] <= max_width:
            return candidate
    raise ValueError("Cover text is too long; shorten it")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--title", required=True, help="Use / between up to three short lines")
    parser.add_argument("--eyebrow", default="")
    parser.add_argument("--profile", choices=COVER_PROFILES, default="wide")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--at", type=float, default=1.0)
    args = parser.parse_args()
    if not args.input.is_file() or args.at < 0:
        parser.error("Input must exist and --at must be nonnegative")
    try:
        width, height = dimensions(args.profile, args.width, args.height, cover=True)
        source = load_image(args.input, args.at)
    except ValueError as exc:
        parser.error(str(exc))
    lines = [line.strip().upper() for line in args.title.split("/") if line.strip()]
    if not 1 <= len(lines) <= 3:
        parser.error("Use one to three short title lines separated by /")
    canvas = ImageOps.fit(source, (width, height), method=Image.Resampling.LANCZOS).filter(
        ImageFilter.GaussianBlur(max(12, width // 50))
    ).convert("RGBA")
    shade = Image.new("RGBA", (width, height), (4, 8, 9, 65))
    canvas = Image.alpha_composite(canvas, shade)
    wide_layout = width / height >= 1.3
    if wide_layout:
        image_box = (int(width * .52), int(height * .95))
        foreground = ImageOps.contain(source, image_box, Image.Resampling.LANCZOS)
        canvas.alpha_composite(foreground.convert("RGBA"),
                               (width - foreground.width - int(width * .025),
                                (height - foreground.height) // 2))
        panel = (int(width * .04), int(height * .06), int(width * .48), int(height * .94))
        text_x, text_y = int(width * .07), int(height * (.31 if not args.eyebrow else .38))
        title_width = int(width * .38)
        max_title_size = int(height * .13)
        eyebrow_y = int(height * .15)
    else:
        vertical_layout = height / width >= 1.5
        image_fraction = .55 if vertical_layout else .60
        image_box = (int(width * .95), int(height * image_fraction))
        foreground = ImageOps.contain(source, image_box, Image.Resampling.LANCZOS)
        canvas.alpha_composite(foreground.convert("RGBA"),
                               ((width - foreground.width) // 2, int(height * .025)))
        panel = (int(width * .035), int(height * (.54 if vertical_layout else .61)),
                 int(width * .965), int(height * (.84 if vertical_layout else .97)))
        text_x = int(width * .075)
        text_y = int(height * (.63 if vertical_layout and not args.eyebrow else
                               .69 if vertical_layout else
                               .70 if not args.eyebrow else .76))
        title_width = int(width * .84)
        max_title_size = int(min(width * .10, height * (.06 if vertical_layout else .075)))
        eyebrow_y = int(height * (.58 if vertical_layout else .66))
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle(panel, radius=max(16, width // 42), fill=(4, 8, 9, 205))
    if args.eyebrow:
        eyebrow = args.eyebrow.upper()
        eyebrow_font = fitted_font(draw, eyebrow, title_width, int(max_title_size * .55))
        draw.text((text_x, eyebrow_y), eyebrow, font=eyebrow_font, fill=(255, 208, 79, 255))
    available_height = panel[3] - text_y - int(height * .035)
    per_line = max(20, int(available_height / len(lines)) - 5)
    for line in lines:
        title_font = fitted_font(draw, line, title_width, min(max_title_size, per_line))
        draw.text((text_x, text_y), line, font=title_font, fill="white",
                  stroke_width=max(1, width // 640), stroke_fill=(0, 0, 0, 220))
        text_y += title_font.size + max(4, int(height * .008))
    canvas = Image.alpha_composite(canvas, overlay).convert("RGB")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(args.out, quality=93, optimize=True)
    print(f"Created {args.out.resolve()} ({width}x{height}, {args.profile})")


if __name__ == "__main__":
    main()
