#!/usr/bin/env python3
from pathlib import Path
import re

POSTS = Path("content/posts")

wp_upload = re.compile(
    r'https?://wheels847\.wordpress\.com/wp-content/uploads/\d{4}/\d{2}/([^\s\)"]+)',
    re.I
)
wp_files = re.compile(
    r'https?://wheels847\.files\.wordpress\.com/\d{4}/\d{2}/([^\s\)"]+)',
    re.I
)

def strip_q(s: str) -> str:
    return s.split("?")[0].split("#")[0]

def fix(text: str) -> str:
    # remove (escaped or unescaped) caption wrappers
    text = re.sub(r'\\?\[caption[^\]]*\]\\?', '', text, flags=re.I)
    text = re.sub(r'\\?\[/caption\\?\]', '', text, flags=re.I)

    # rewrite WP URLs to local images/<filename>
    text = wp_upload.sub(lambda m: f'images/{strip_q(m.group(1))}', text)
    text = wp_files.sub(lambda m: f'images/{strip_q(m.group(1))}', text)

    # unwrap linked images: [![alt](images/x)](whatever) -> ![alt](images/x)
    text = re.sub(r'\[!\[([^\]]*)\]\((images/[^)]+)\)\]\([^)]+\)', r'![\1](\2)', text)
    return text

def main():
    changed = 0
    for md in POSTS.rglob("index.md"):
        orig = md.read_text(encoding="utf-8", errors="ignore")
        new = fix(orig)
        if new != orig:
            md.write_text(new, encoding="utf-8")
            changed += 1
    print(f"Updated {changed} files.")

if __name__ == "__main__":
    if not POSTS.exists():
        raise SystemExit("Run this from the Hugo site root (where hugo.toml lives).")
    main()