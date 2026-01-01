#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

POSTS_ROOT = Path("content/posts")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
FEATURE_NAMES_PREFIX = ("feature", "featured", "cover", "thumbnail")

# Markdown image: ![alt](path "title")
MD_IMG_RE = re.compile(r'!\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
# HTML image: <img src="...">
HTML_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def strip_query_fragment(s: str) -> str:
    s = s.strip().strip('"').strip("'")
    s = s.split("?", 1)[0].split("#", 1)[0]
    return unquote(s)


def is_remote(path: str) -> bool:
    return path.startswith(("http://", "https://", "data:"))


def any_feature_exists(bundle: Path) -> bool:
    for p in bundle.iterdir():
        if not p.is_file():
            continue
        name = p.stem.lower()
        if name.startswith(FEATURE_NAMES_PREFIX) and p.suffix.lower() in IMAGE_EXTS:
            return True
    return False


def build_file_index(bundle: Path) -> dict[str, Path]:
    """
    Map lowercase filename -> Path for quick case-insensitive lookup,
    including both bundle root and bundle/images.
    """
    idx: dict[str, Path] = {}

    def add_dir(d: Path) -> None:
        if not d.exists():
            return
        for p in d.iterdir():
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                idx[p.name.lower()] = p

    add_dir(bundle)
    add_dir(bundle / "images")
    return idx


def resolve_local_image(bundle: Path, raw: str, file_idx: dict[str, Path]) -> Path | None:
    p = strip_query_fragment(raw)
    if not p or is_remote(p):
        return None

    # Normalize a few common forms
    if p.startswith("./"):
        p = p[2:]
    p = p.lstrip("/")  # treat as relative for our local check

    # Try direct relative path from bundle
    direct = bundle / p
    if direct.exists() and direct.is_file() and direct.suffix.lower() in IMAGE_EXTS:
        return direct

    # Try if it was written as images/foo.jpg but file is elsewhere (or case mismatch)
    base = Path(p).name
    hit = file_idx.get(base.lower())
    if hit:
        return hit

    # Try stem match (extension may be missing in markdown)
    stem = Path(base).stem.lower()
    for k, v in file_idx.items():
        if Path(k).stem.lower() == stem:
            return v

    return None


def extract_first_referenced_image(md_text: str) -> list[str]:
    refs = []
    refs.extend(MD_IMG_RE.findall(md_text))
    refs.extend(HTML_IMG_RE.findall(md_text))
    return refs


def pick_largest_image(bundle: Path) -> Path | None:
    candidates: list[Path] = []

    for d in (bundle, bundle / "images"):
        if not d.exists():
            continue
        for p in d.iterdir():
            if not p.is_file():
                continue
            if p.suffix.lower() not in IMAGE_EXTS:
                continue
            if p.stem.lower().startswith(FEATURE_NAMES_PREFIX):
                continue
            candidates.append(p)

    if not candidates:
        return None

    candidates.sort(key=lambda x: x.stat().st_size, reverse=True)
    return candidates[0]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create Blowfish feature images for post bundles by copying the first referenced (or largest) image to feature.<ext>."
    )
    ap.add_argument("--dry-run", action="store_true", help="Show what would happen without writing files.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing feature.* if present.")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of bundles processed (0 = no limit).")
    args = ap.parse_args()

    if not POSTS_ROOT.exists():
        print("ERROR: content/posts not found. Run from site root (where hugo.toml lives).")
        return 2

    bundles = sorted(POSTS_ROOT.rglob("index.md"))
    if args.limit:
        bundles = bundles[: args.limit]

    created = 0
    skipped = 0
    missing = 0

    for md in bundles:
        bundle = md.parent

        # Skip if feature already exists, unless --force
        if any_feature_exists(bundle) and not args.force:
            skipped += 1
            continue

        text = md.read_text(encoding="utf-8", errors="ignore")
        file_idx = build_file_index(bundle)

        chosen: Path | None = None

        # 1) Prefer first referenced local image
        for ref in extract_first_referenced_image(text):
            chosen = resolve_local_image(bundle, ref, file_idx)
            if chosen:
                break

        # 2) Fallback: largest image in bundle/images
        if not chosen:
            chosen = pick_largest_image(bundle)

        if not chosen:
            missing += 1
            continue

        # Create feature.<ext> in bundle root
        dest = bundle / f"feature{chosen.suffix.lower()}"

        # Overwrite handling
        if dest.exists() and not args.force:
            skipped += 1
            continue

        rel_bundle = bundle.relative_to(Path("."))
        rel_chosen = chosen.relative_to(Path("."))
        rel_dest = dest.relative_to(Path("."))

        if args.dry_run:
            print(f"[DRY] {rel_bundle}: {rel_chosen} -> {rel_dest}")
            continue

        shutil.copy2(chosen, dest)
        created += 1
        print(f"[OK]  {rel_bundle}: {rel_chosen.name} -> {dest.name}")

    print("\nSummary")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  No image found: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
