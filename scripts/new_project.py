"""Create the small, editable planning files for one video project."""
import argparse
from pathlib import Path
import re
import shutil

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO / "templates"
FILES = ("BRIEF.md", "STORYBOARD.md", "SHOT_LOG.csv", "EDIT_DECISIONS.csv", "REVIEW.md",
         "ASSET_PLAN.md", "MOTION_PLAN.md", "CUT_AUDIT.md", "STYLE.md", "PLATFORM_PACKAGE.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Short project name, for example weekend-food-vlog")
    parser.add_argument("--media", type=Path, help="Existing source media folder; files are not copied")
    parser.add_argument("--root", type=Path, default=REPO / "projects", help="Parent folder for the new project")
    args = parser.parse_args()

    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    if not slug:
        parser.error("name must contain a letter or number")
    if args.media and not args.media.is_dir():
        parser.error(f"media folder does not exist: {args.media}")
    project = args.root.expanduser().resolve() / slug
    if project.exists() and any(project.iterdir()):
        parser.error(f"project already has files: {project}")
    project.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copyfile(TEMPLATES / name, project / name)
    for folder in ("media", "assets", "work", "review", "exports"):
        (project / folder).mkdir(exist_ok=True)
    if args.media:
        (project / "SOURCE_MEDIA.txt").write_text(str(args.media.expanduser().resolve()) + "\n", encoding="utf-8")
    print(project)


if __name__ == "__main__":
    main()

