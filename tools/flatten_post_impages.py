mkdir -p tools
cat > tools/flatten_post_images.py <<'PY'
#!/usr/bin/env python3
from pathlib import Path
import re
import shutil

ROOT = Path(".")
POSTS = ROOT / "content" / "posts"

# Markdown image pattern: ![alt](dest)
IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

def strip_q(s: str) -> str:
    return s.split("?")[0].split("#")[0].strip()

def has_ext(p: str) -> bool:
    return "." in Path(p).name

def main():
    if not POSTS.exists():
        raise SystemExit("Run this from the Hugo site root (where hugo.toml lives).")

    changed_files = 0
    moved_files = 0
    fixed_ext = 0

    for md in POSTS.rglob("index.md"):
        bundle = md.parent
        images_dir = bundle / "images"
        moved_map = {}  # basename -> filename

        # Move images/* up one level (if images folder exists)
        if images_dir.exists() and images_dir.is_dir():
            for f in images_dir.iterdir():
                if not f.is_file():
                    continue
                dest = bundle / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
                    moved_files += 1
                moved_map[f.stem.low]()_
