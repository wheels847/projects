#!/usr/bin/env python3
from pathlib import Path
import re
import shutil

POSTS = Path("content/posts")

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

        # Move images/* up one level
        if images_dir.exists() and images_dir.is_dir():
            for f in images_dir.iterdir():
                if not f.is_file():
                    continue
                dest = bundle / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
                    moved_files += 1
            # Remove images dir if empty
            try:
                images_dir.rmdir()
            except OSError:
                pass

        # Lookup of files now in the bundle (for fixing extensionless links)
        file_lookup = {p.stem.lower(): p.name for p in bundle.iterdir() if p.is_file()}

        text = md.read_text(encoding="utf-8", errors="ignore")

        # Rewrite HTML src="images/..." to src="..."
        text2 = re.sub(r'src="images/', 'src="', text)

        def repl(m):
            nonlocal fixed_ext
            alt = m.group(1)
            dest = strip_q(m.group(2))

            # Skip remote URLs
            if dest.startswith("http://") or dest.startswith("https://"):
                return m.group(0)

            # Remove leading images/
            if dest.startswith("images/"):
                dest = dest[len("images/"):]

            # Fix links with no extension by matching a real file in the folder
            if not has_ext(dest):
                stem = Path(dest).name.lower()
                if stem in file_lookup:
                    dest = file_lookup[stem]
                    fixed_ext += 1

            return f"![{alt}]({dest})"

        text2 = IMG_RE.sub(repl, text2)

        if text2 != text:
            md.write_text(text2, encoding="utf-8")
            changed_files += 1

    print(f"Moved images up from /images/: {moved_files}")
    print(f"Updated markdown files:      {changed_files}")
    print(f"Fixed no-extension images:   {fixed_ext}")

if __name__ == "__main__":
    main()
