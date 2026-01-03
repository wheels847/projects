#!/usr/bin/env python3
from pathlib import Path
import sys
from PIL import Image, ImageOps

def resize_max(im: Image.Image, max_dim: int) -> Image.Image:
    w, h = im.size
    scale = max_dim / max(w, h)
    if scale >= 1:
        return im.copy()
    return im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

def main():
    if len(sys.argv) != 3:
        print("Usage: prepare_headshot.py <input.jpg> <output_dir>")
        sys.exit(2)

    inp = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.open(inp).convert("RGB")

    # Crop tuned for your 1592x2048 headshot to remove the bottom-right Gemini mark
    # while keeping a flattering head-and-shoulders portrait.
    crop = img.crop((180, 0, 1450, 1700))  # left, top, right, bottom

    (out_dir / "headshot-cropped-master.jpg").write_bytes(b"")  # ensure path exists on some filesystems
    crop.save(out_dir / "headshot-cropped-master.jpg", quality=95, optimize=True)

    web600 = resize_max(crop, 600)
    web1200 = resize_max(crop, 1200)

    web600.save(out_dir / "headshot-600.jpg", quality=90, optimize=True, progressive=True)
    web1200.save(out_dir / "headshot-1200.jpg", quality=92, optimize=True, progressive=True)

    square = ImageOps.fit(crop, (512, 512), method=Image.Resampling.LANCZOS, centering=(0.5, 0.33))
    square.save(out_dir / "headshot-square-512.jpg", quality=90, optimize=True, progressive=True)

    print("Wrote:")
    print(out_dir / "headshot-600.jpg")
    print(out_dir / "headshot-1200.jpg")
    print(out_dir / "headshot-square-512.jpg")

if __name__ == "__main__":
    main()
