"""Copy the installable Bedder skill into the built MkDocs site unchanged."""

from pathlib import Path
from shutil import copy2


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "bedder-skill"


def on_post_build(config, **_kwargs) -> None:
    """Publish skill files after Markdown rendering has completed."""
    site_skill_dir = Path(config["site_dir"]) / "bedder-skill"
    for source in SKILL_DIR.rglob("*"):
        if not source.is_file():
            continue
        destination = site_skill_dir / source.relative_to(SKILL_DIR)
        destination.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, destination)
