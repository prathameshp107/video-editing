"""End-to-end offline checks using synthetic media, independent of project files."""

import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat


KIT = Path(__file__).resolve().parents[1]
SCRIPTS = KIT / "scripts"


def run(*args: str, expect_success: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(args, capture_output=True, text=True)
    if expect_success and result.returncode:
        raise RuntimeError(f"Command failed: {args}\n{result.stderr}")
    if not expect_success and not result.returncode:
        raise AssertionError(f"Command unexpectedly succeeded: {args}")
    return result


def probe(path: Path) -> dict:
    return json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format",
                          "-of", "json", str(path)).stdout)


def check_video(path: Path, width: int, height: int, audio: bool | None = None) -> None:
    info = probe(path)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == (width, height)
    if audio is not None:
        assert any(s["codec_type"] == "audio" for s in info["streams"]) == audio
    run("ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-")


def check_skill_headers() -> None:
    for name in ("broll-curator", "audio-finisher", "color-match", "platform-package",
                 "format-repurposer"):
        body = (KIT / ".agents" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert re.match(rf"^---\nname: {name}\ndescription: [^\n]+\n---\n", body)
        assert "[TODO:" not in body


def main() -> None:
    check_skill_headers()
    with tempfile.TemporaryDirectory(prefix="video-skill-test-") as directory:
        root = Path(directory)
        wide = root / "wide.mp4"
        vertical = root / "vertical.mp4"
        for target, size, has_audio in ((wide, "640x360", True), (vertical, "360x640", False)):
            cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                   f"testsrc2=size={size}:rate=24"]
            if has_audio:
                cmd += ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000"]
            cmd += ["-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p"]
            if has_audio:
                cmd += ["-c:a", "aac", "-b:a", "128k"]
            cmd += [str(target)]
            run(*cmd)
        still = root / "still.jpg"
        image = Image.new("RGB", (800, 500), "#d9ac73")
        draw = ImageDraw.Draw(image)
        draw.ellipse((330, 120, 560, 350), fill="#874923")
        image.save(still)

        manifest = root / "broll.csv"
        rows = [
            {"source": "wide.mp4", "start_s": 0.5, "duration_s": 1,
             "filename": "action.mp4", "category": "Action", "usage_note": "Synthetic moving test",
             "rights": "Generated test fixture", "source_url": "", "media_type": "video", "rotation": "auto"},
            {"source": "still.jpg", "start_s": 0, "duration_s": 1,
             "filename": "detail.mp4", "category": "Detail", "usage_note": "Synthetic still test",
             "rights": "Generated test fixture", "source_url": "", "media_type": "photo motion", "rotation": "auto"},
        ]
        with manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        broll = root / "broll"
        run(sys.executable, str(SCRIPTS / "curate_broll.py"), "--manifest", str(manifest),
            "--output", str(broll), "--profile", "vertical")
        with (broll / "catalog.csv").open(newline="", encoding="utf-8") as handle:
            catalog = list(csv.DictReader(handle))
        assert len(catalog) == 2 and all(item["rights"] == "Generated test fixture" for item in catalog)
        check_video(broll / "clips" / "action.mp4", 1080, 1920, True)
        check_video(broll / "clips" / "detail.mp4", 1080, 1920, False)
        first, last = root / "still_first.png", root / "still_last.png"
        for at, target in (("0.05", first), ("0.90", last)):
            run("ffmpeg", "-y", "-v", "error", "-ss", at, "-i",
                str(broll / "clips" / "detail.mp4"), "-frames:v", "1", str(target))
        difference = ImageStat.Stat(ImageChops.difference(Image.open(first), Image.open(last))).mean
        assert max(difference) > 0.5, "Photo-derived clip has no visible motion"
        rows[0]["rights"] = ""
        invalid_manifest = root / "invalid_broll.csv"
        with invalid_manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerow(rows[0])
        run(sys.executable, str(SCRIPTS / "curate_broll.py"), "--manifest", str(invalid_manifest),
            "--output", str(root / "invalid_broll"), expect_success=False)
        print("PASS B-roll from raw video and a still, independent of an edit decision list")

        audio = root / "audio.wav"
        run("ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
            "sine=frequency=220:sample_rate=48000", "-t", "2", str(audio))
        processed = root / "audio_finished.wav"
        report = root / "audio_report.json"
        run(sys.executable, str(SCRIPTS / "audio_finish.py"), "normalize", str(audio),
            str(processed), "--target", "-16", "--out", str(report))
        measured = json.loads(report.read_text(encoding="utf-8"))
        assert measured["peak_limit_pass"] and processed.is_file()
        assert any(s["codec_type"] == "audio" for s in probe(processed)["streams"])
        m4a = root / "audio_finished.m4a"
        run(sys.executable, str(SCRIPTS / "audio_finish.py"), "normalize", str(audio),
            str(m4a), "--target", "-16")
        assert any(s["codec_type"] == "audio" for s in probe(m4a)["streams"])
        print("PASS WAV and M4A audio-only normalization with encoded-output peak verification")

        comparison = root / "color"
        run(sys.executable, str(SCRIPTS / "color_compare.py"), "--input", str(wide),
            "--input", str(vertical), "--input", str(still), "--out-dir", str(comparison))
        measured_color = json.loads((comparison / "measurements.json").read_text(encoding="utf-8"))
        assert [len(item["samples"]) for item in measured_color] == [3, 3, 1]
        assert Image.open(comparison / "comparison.jpg").size == (1440, 990)
        print("PASS three-point color comparison across wide, vertical, and photo sources")

        covers = {"wide": (1280, 720), "vertical": (1080, 1920),
                  "square": (1080, 1080), "portrait-feed": (1080, 1350)}
        for profile, size in covers.items():
            target = root / f"cover_{profile}.jpg"
            run(sys.executable, str(SCRIPTS / "make_thumbnail.py"), "--input", str(still),
                "--title", "TEST/STORY", "--eyebrow", "CREATOR", "--profile", profile,
                "--out", str(target))
            assert Image.open(target).size == size
        print("PASS cover creation in four canvas profiles")

        valid_chapters = root / "chapters.txt"
        valid_chapters.write_text("00:00 Start\n00:01 Detail\n", encoding="utf-8")
        run(sys.executable, str(SCRIPTS / "check_chapters.py"), "--video", str(wide),
            "--chapters", str(valid_chapters))
        valid_chapters.write_text("00:01 Late start\n00:00 Backward\n", encoding="utf-8")
        run(sys.executable, str(SCRIPTS / "check_chapters.py"), "--video", str(wide),
            "--chapters", str(valid_chapters), expect_success=False)
        print("PASS long-form chapter check accepts ordered times and rejects invalid times")

        for profile, size in (("wide", (1920, 1080)), ("vertical", (1080, 1920)),
                              ("square", (1080, 1080)), ("portrait-feed", (1080, 1350))):
            output = root / f"reframe_{profile}.mp4"
            source = vertical if profile == "wide" else wide
            run(sys.executable, str(SCRIPTS / "make_format.py"), str(source), str(output),
                "--start", "0.5", "--duration", "1", "--profile", profile,
                "--mode", "crop" if profile == "vertical" else "fit")
            check_video(output, *size, audio=(source == wide))
        custom = root / "custom.mp4"
        run(sys.executable, str(SCRIPTS / "make_format.py"), str(wide), str(custom),
            "--duration", "1", "--width", "640", "--height", "800", "--mode", "crop")
        check_video(custom, 640, 800, True)
        remainder = root / "remainder.mp4"
        run(sys.executable, str(SCRIPTS / "make_format.py"), str(wide), str(remainder),
            "--start", "1", "--profile", "square", "--mode", "fit")
        assert 1.8 <= float(probe(remainder)["format"]["duration"]) <= 2.2
        run(sys.executable, str(SCRIPTS / "make_format.py"), str(wide), str(root / "bad.mp4"),
            "--start", "99", "--duration", "1", expect_success=False)
        print("PASS all four video canvases with fit/crop and expected audio presence")
        projects = root / "projects"
        run(sys.executable, str(SCRIPTS / "new_project.py"), "generic-reel",
            "--media", str(root), "--root", str(projects))
        new_project = projects / "generic-reel"
        assert (new_project / "PLATFORM_PACKAGE.md").is_file()
        brief = (new_project / "BRIEF.md").read_text(encoding="utf-8")
        assert "Platform(s) and canvas:" in brief and "YouTube, 16:9" not in brief
        print("PASS generic new-project template without a forced vlog canvas")
    print("PASS cross-format skills with only synthetic local fixtures")


if __name__ == "__main__":
    main()
