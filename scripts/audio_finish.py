"""Measure or normalize a finished video's or audio file's mixed soundtrack."""

import argparse
import json
import re
import subprocess
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, check=True)


def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(path)]).stdout)


def loudnorm_pass(path: Path, target: float, true_peak: float, start: float | None,
                  duration: float | None) -> dict:
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-v", "info"]
    if start is not None:
        cmd += ["-ss", str(start)]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", str(duration)]
    cmd += ["-vn", "-af", f"loudnorm=I={target}:TP={true_peak}:LRA=11:print_format=json",
            "-f", "null", "-"]
    result = run(cmd)
    matches = re.findall(r"\{\s*\"input_i\".*?\}", result.stderr, re.S)
    if not matches:
        raise RuntimeError("FFmpeg did not return loudnorm measurements")
    return json.loads(matches[-1])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("analyze", "normalize"):
        item = sub.add_parser(name)
        item.add_argument("input", type=Path)
        if name == "normalize":
            item.add_argument("output", type=Path)
        item.add_argument("--target", type=float, default=-14.0)
        item.add_argument("--true-peak", type=float, default=-1.5)
        item.add_argument("--start", type=float)
        item.add_argument("--duration", type=float)
        item.add_argument("--out", type=Path, help="Write measurement report as JSON")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Missing input: {args.input}")
    if args.command == "normalize" and args.input.resolve() == args.output.resolve():
        parser.error("Output must differ from input")
    source = probe(args.input)
    if not any(stream["codec_type"] == "audio" for stream in source["streams"]):
        parser.error("Input has no audio stream")
    source_duration = float(source["format"]["duration"])
    if args.start is not None and (args.start < 0 or args.start >= source_duration):
        parser.error("Start must fall within the source")
    if args.duration is not None and (args.duration <= 0 or
                                      (args.start or 0) + args.duration > source_duration + 0.1):
        parser.error("Duration must be positive and within the source")
    # AAC encoding can create inter-sample overshoot. Reserve 1 dB during processing
    # and measure the encoded output against the user-facing limit afterward.
    processing_peak = args.true_peak - 1.0 if args.command == "normalize" else args.true_peak
    first = loudnorm_pass(args.input, args.target, processing_peak, args.start, args.duration)
    report = {"input": str(args.input.resolve()), "target_lufs": args.target,
              "true_peak_limit_db": args.true_peak, "before": first}
    if args.command == "normalize":
        suffix = args.output.suffix.lower()
        if suffix not in (".mp4", ".m4a", ".wav", ".mp3"):
            parser.error("Output must be .mp4, .m4a, .wav, or .mp3")
        has_video = any(stream["codec_type"] == "video" for stream in source["streams"])
        if suffix != ".mp4" and has_video:
            parser.error("Use .mp4 to retain video; audio-only output would discard picture")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        filt = (
            f"loudnorm=I={args.target}:TP={processing_peak}:LRA=11:"
            f"measured_I={first['input_i']}:measured_TP={first['input_tp']}:"
            f"measured_LRA={first['input_lra']}:measured_thresh={first['input_thresh']}:"
            f"offset={first['target_offset']}:linear=true:print_format=summary"
        )
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
        if args.start is not None:
            cmd += ["-ss", str(args.start)]
        cmd += ["-i", str(args.input)]
        if args.duration is not None:
            cmd += ["-t", str(args.duration)]
        if has_video:
            cmd += ["-map", "0:v:0", "-c:v", "copy"]
        cmd += ["-map", "0:a:0", "-af", filt]
        if suffix == ".wav":
            cmd += ["-c:a", "pcm_s16le", "-ar", "48000"]
        elif suffix == ".mp3":
            cmd += ["-c:a", "libmp3lame", "-b:a", "192k", "-ar", "48000"]
        else:
            cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart"]
        cmd += [str(args.output)]
        run(cmd)
        report["output"] = str(args.output.resolve())
        report["after"] = loudnorm_pass(args.output, args.target, args.true_peak, None, None)
        report["peak_limit_pass"] = float(report["after"]["input_tp"]) <= args.true_peak
        report["target_reached_within_1_lu"] = abs(float(report["after"]["input_i"]) - args.target) <= 1
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
