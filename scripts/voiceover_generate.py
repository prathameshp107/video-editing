"""Generate Hindi voiceover locally from a consented reference voice."""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path


KIT = Path(__file__).resolve().parents[1]
SAMPLE_VOICE_M4A = KIT / "private" / "voice" / "Sample Voice for Clonning.m4a"
SAMPLE_VOICE_WAV = KIT / "private" / "voice" / "Sample Voice for Clonning.wav"
DEFAULT_REFERENCE = (
    SAMPLE_VOICE_WAV if SAMPLE_VOICE_WAV.is_file()
    else (SAMPLE_VOICE_M4A if SAMPLE_VOICE_M4A.is_file()
    else KIT / "private" / "voice" / "reference_23s.wav")
)
DEFAULT_MODEL = KIT / "private" / "models" / "chatterbox-hi-v3"
MODEL_FILES = ("t3_hi.safetensors", "s3gen.pt", "ve.pt",
               "grapheme_mtl_merged_expanded_v1.json")


def text_parts(text: str) -> list[str]:
    text = " ".join(text.split())
    if not text:
        raise ValueError("Voiceover text is empty")
    parts = [s.strip() for s in re.findall(r"[^।!?]+[।!?]?", text) if s.strip()]
    return parts or [text]


def resolve_reference_wav(ref_path: Path) -> Path:
    """Ensure the reference is a 24 kHz mono WAV readable by torchaudio/soundfile."""
    if not ref_path.is_file():
        raise SystemExit(f"Voice reference missing: {ref_path}")
    if ref_path.suffix.lower() == ".wav":
        return ref_path

    wav_path = ref_path.with_suffix(".wav")
    if not wav_path.is_file() or wav_path.stat().st_mtime < ref_path.stat().st_mtime:
        import subprocess
        print(f"Converting reference audio '{ref_path.name}' to 24 kHz mono WAV...", flush=True)
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(ref_path),
             "-vn", "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", str(wav_path)],
            check=True
        )
    return wav_path


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Hindi text to speak")
    source.add_argument("--text-file", type=Path, help="UTF-8 text file to speak")
    p.add_argument("--out", type=Path, required=True, help="New WAV output path")
    p.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE,
                   help="Consented, clean voice reference audio (WAV, M4A, etc.)")
    p.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL)
    p.add_argument("--language", default="hi", choices=["hi"],
                   help="Bundled checkpoint is Hindi-specific")
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--gap", type=float, default=.14, help="Seconds between sentences")
    p.add_argument("--threads", type=int, default=8)
    p.add_argument("--exaggeration", type=float, default=.5)
    p.add_argument("--cfg-weight", type=float, default=.5)
    p.add_argument("--dry-run", action="store_true",
                   help="Check inputs and split text without loading the model")
    return p


def main() -> None:
    args = parser().parse_args()
    text = args.text if args.text is not None else args.text_file.read_text(encoding="utf-8")
    parts = text_parts(text)
    missing = [name for name in MODEL_FILES if not (args.model_dir / name).is_file()]
    if not args.reference.is_file():
        raise SystemExit(f"Voice reference missing: {args.reference}")
    effective_reference = resolve_reference_wav(args.reference)
    if missing:
        raise SystemExit(f"Model files missing in {args.model_dir}: {', '.join(missing)}")
    if args.gap < 0 or args.threads < 1:
        raise SystemExit("--gap must be nonnegative and --threads must be positive")
    summary = {"reference": str(effective_reference.resolve()),
               "source_reference": str(args.reference.resolve()),
               "model_dir": str(args.model_dir.resolve()),
               "sentences": len(parts), "output": str(args.out.resolve())}
    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    if args.out.exists():
        raise SystemExit(f"Output already exists; choose a new path: {args.out}")

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    import torch
    import torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox.models.s3gen import S3Gen

    torch.set_num_threads(args.threads)
    original_load = S3Gen.load_state_dict

    def load_v3_decoder(self, state_dict, strict=True, assign=False):
        result = original_load(self, state_dict, strict=False, assign=assign)
        allowed_missing = {"tokenizer._mel_filters", "tokenizer.window"}
        if set(result.missing_keys) != allowed_missing or result.unexpected_keys:
            raise RuntimeError(f"Unexpected decoder checkpoint mismatch: {result}")
        return result

    print("Loading the local Hindi voice model...", flush=True)
    S3Gen.load_state_dict = load_v3_decoder
    try:
        model = ChatterboxMultilingualTTS.from_local(
            args.model_dir, device="cpu", t3_model="t3_hi.safetensors")
    finally:
        S3Gen.load_state_dict = original_load
    model.prepare_conditionals(str(effective_reference), exaggeration=args.exaggeration)

    waves = []
    started = time.monotonic()
    for index, sentence in enumerate(parts, 1):
        print(f"Generating sentence {index}/{len(parts)}...", flush=True)
        torch.manual_seed(args.seed + index)
        with torch.inference_mode():
            wave = model.generate(sentence, language_id=args.language,
                                  exaggeration=args.exaggeration,
                                  cfg_weight=args.cfg_weight)
        waves.append(wave.cpu())
    gap = torch.zeros(1, round(args.gap * model.sr))
    full = torch.cat([wave if i == len(waves)-1 else torch.cat([wave, gap], dim=-1)
                      for i, wave in enumerate(waves)], dim=-1)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    torchaudio.save(str(args.out), full, model.sr)
    print(json.dumps({**summary, "sample_rate": model.sr,
                      "duration_s": round(full.shape[-1] / model.sr, 3),
                      "elapsed_s": round(time.monotonic() - started, 1)},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
