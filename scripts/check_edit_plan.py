"""Check that all marked must-use shots appear in an edit decision list."""
import argparse
import csv
import json
from pathlib import Path


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def yes(value):
    return str(value or "").strip().lower() in {"1", "yes", "y", "true"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    shots = read_csv(project / "SHOT_LOG.csv")
    cuts = read_csv(project / "EDIT_DECISIONS.csv")
    selected = {row.get("source", "").strip().casefold() for row in cuts if row.get("source", "").strip()}
    errors = []
    for shot in shots:
        name = shot.get("filename", "").strip()
        if not name:
            continue
        if yes(shot.get("must_use")) and name.casefold() not in selected:
            errors.append(f"Missing must-use shot: {name}")
        if yes(shot.get("selected")) and name.casefold() not in selected:
            errors.append(f"Marked selected but absent from edit: {name}")
    inventory_path = project / "media_inventory.json"
    if inventory_path.exists():
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        known = {row["filename"].casefold(): row for row in inventory["files"]}
        for cut in cuts:
            source = cut.get("source", "").strip()
            if not source:
                continue
            if source.casefold() not in known:
                errors.append(f"Edit references a file outside the inventory: {source}")
                continue
            duration = known[source.casefold()].get("duration_s")
            if duration is not None and known[source.casefold()].get("kind") != "image":
                try:
                    start = float(cut.get("start_s") or 0)
                    length = float(cut.get("duration_s") or 0)
                    if start < 0 or length <= 0 or start + length > duration + .15:
                        errors.append(f"Invalid trim for {source}: start={start}, duration={length}, source={duration}")
                except ValueError:
                    errors.append(f"Invalid numeric trim for {source}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"Coverage OK: {len(cuts)} edit decisions, {sum(yes(s.get('must_use')) for s in shots)} required shots")


if __name__ == "__main__":
    main()

