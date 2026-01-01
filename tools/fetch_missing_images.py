#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess

POSTS = Path("content/posts")

# Find markdown images that point to images/<file>
IMG_MD = re.compile(r'!\[[^\]]*\]\(\s*(images/[^)\s]+)\s*\)', re.IGNORECASE)

# Extract year/month from front matter: date: 2015-09-27 (or 2015-09-27T...)
DATE_RE = re.compile(r'(?m)^date:\s*"?(\d{4})-(\d{2})-\d{2}')

def curl_download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            ["curl", "-fL", "-A", "Mozilla/5.0", "-o", str(dest), url],
            check=True,
            capture_output=True,
            text=True,
        )
        return dest.exists() and dest.stat().st_size > 0
    except subprocess.CalledProcessError:
        return False

def get_year_month(text: str, md_path: Path):
    m = DATE_RE.search(text)
    if m:
        return m.group(1), m.group(2)

    # Fallback: infer from path segments .../YYYY/MM/... if present
    parts = md_path.parts
    for i in range(len(parts) - 2):
        if re.fullmatch(r"\d{4}", parts[i]) and re.fullmatch(r"\d{2}", parts[i+1]):
            return parts[i], parts[i+1]
    return None, None

def main():
    if not POSTS.exists():
        raise SystemExit("Run this from the Hugo site root (where hugo.toml lives).")

    total_missing = 0
    fixed = 0
    still_missing = []

    for md in POSTS.rglob("index.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        year, month = get_year_month(text, md)
        if not year or not month:
            # Skip if we can't infer; rare
            continue

        refs = set(IMG_MD.findall(text))
        if not refs:
            continue

        for ref in refs:
            # ref like images/nggn.jpg
            rel = ref.split("?")[0].split("#")[0]
            dest = md.parent / rel
            if dest.exists():
                continue

            total_missing += 1
            filename = Path(rel).name

            # Try expected WP locations for that post month
            candidates = [
                f"https://wheels847.wordpress.com/wp-content/uploads/{year}/{month}/{filename}",
                f"https://wheels847.files.wordpress.com/{year}/{month}/{filename}",
            ]

            ok = False
            for url in candidates:
                if curl_download(url, dest):
                    ok = True
                    fixed += 1
                    break

            if not ok:
                still_missing.append((str(md), filename, year, month))

    print(f"Missing referenced images: {total_missing}")
    print(f"Downloaded successfully:     {fixed}")
    print(f"Still missing:              {len(still_missing)}")
    if still_missing:
        print("\nExamples still missing (post, file, year, month):")
        for row in still_missing[:25]:
            print(" -", row)

if __name__ == "__main__":
    main()
