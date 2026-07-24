#!/usr/bin/env python3
"""
ACT WEB Image Optimization Script
===================================
Compresses images, generates WebP versions, and reports savings.

Requirements:
    pip install Pillow

Usage:
    python optimize_images.py
"""

import os
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is not installed. Run: pip install Pillow")
    exit(1)


BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "Images"
ORIGINALS_DIR = IMAGES_DIR / "originals"

# Targets
LOGO_TARGET_KB = 50
JPEG_QUALITY = 75
WEBP_QUALITY = 75
ABOVE_FOLD_MAX_KB = 200
GALLERY_MAX_KB = 100


def get_size_kb(path: Path) -> float:
    return path.stat().st_size / 1024


def backup_originals():
    if ORIGINALS_DIR.exists():
        print(f"[SKIP] Originals folder already exists: {ORIGINALS_DIR}")
        return
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in IMAGES_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".mp4"}:
            shutil.copy2(f, ORIGINALS_DIR / f.name)
            count += 1
    print(f"[BACKUP] Copied {count} files to {ORIGINALS_DIR}")


def optimize_logo():
    logo = IMAGES_DIR / "act-logo.png"
    if not logo.exists():
        print("[SKIP] act-logo.png not found")
        return
    original_kb = get_size_kb(logo)
    print(f"\n[LOGO] Original size: {original_kb:.1f} KB")
    
    img = Image.open(logo)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
    
    # Try multiple PNG optimization levels
    best_size = original_kb * 1024
    best_bytes = None
    for level in [1, 6, 9]:
        buf = Path("_tmp_logo.png")
        img.save(buf, format="PNG", optimize=True, compress_level=level)
        size = buf.stat().st_size
        if size < best_size:
            best_size = size
            best_bytes = buf.read_bytes()
        if best_size / 1024 <= LOGO_TARGET_KB:
            break
    
    if best_bytes:
        logo.write_bytes(best_bytes)
        new_kb = get_size_kb(logo)
        print(f"[LOGO] Compressed to: {new_kb:.1f} KB (target: <{LOGO_TARGET_KB} KB)")
        if new_kb > LOGO_TARGET_KB:
            print(f"[WARN] Logo still above target. Consider converting to SVG.")
    
    # Cleanup temp
    for tmp in ["_tmp_logo.png"]:
        p = Path(tmp)
        if p.exists():
            p.unlink()


def optimize_jpegs():
    jpegs = sorted([
        f for f in IMAGES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg"}
    ])
    
    total_before = 0
    total_after = 0
    above_fold = {
        "hero-bg-1.jpg", "hero-bg-2.jpg", "hero-bg-3.jpg", "hero-bg-4.jpg", "hero-bg-5.jpg",
        "eye-hero-bg-1.jpg", "eye-hero-bg-2.jpg", "eye-hero-bg-3.jpg", "eye-hero-bg-4.jpg",
        "wed-hero-bg.jpg", "wed-trees.jpg",
        "vipingo-hero-bg.jpg", "vipingo-extraction.jpg", "vipingo-ppe-team.jpg",
        "kuruitu-hero-bg.jpg", "kuruitu-strike-team.jpg", "kuruitu-gallery-5.jpg",
        "olive-hero-bg.jpg", "olive-gallery-1.jpg", "olive-gallery-3.jpg",
        "copa-before.jpg", "copa-after.jpg", "copa-team.jpg",
        "outcomes-hero.jpg", "phase6-main.jpg",
        "intervention-1.jpg", "intervention-2.jpg", "intervention-3.jpg", "intervention-4.jpg",
        "philosophy-main.jpg",
        "director-headshot.jpg",
        "infra-installed.jpg", "infra-welding.jpg",
        "bin-photo-1.jpg",
    }
    
    print(f"\n[JPEG] Found {len(jpegs)} JPEG files")
    
    for img_path in jpegs:
        before_kb = get_size_kb(img_path)
        total_before += before_kb
        
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Determine target
        is_above_fold = img_path.name in above_fold
        target_kb = ABOVE_FOLD_MAX_KB if is_above_fold else GALLERY_MAX_KB
        
        # Progressive quality reduction until target met
        quality = JPEG_QUALITY
        for q in [85, 75, 65, 55, 50]:
            buf = Path("_tmp_opt.jpg")
            img.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
            size_kb = get_size_kb(buf)
            if size_kb <= target_kb or q == 50:
                quality = q
                break
        
        img_path.write_bytes(buf.read_bytes())
        after_kb = get_size_kb(img_path)
        total_after += after_kb
        
        status = "OK" if after_kb <= target_kb else "OVER"
        print(f"  {img_path.name}: {before_kb:.1f}KB -> {after_kb:.1f}KB (q={quality}, target={target_kb}KB) [{status}]")
        
        # Cleanup temp
        buf = Path("_tmp_opt.jpg")
        if buf.exists():
            buf.unlink()
    
    saved = total_before - total_after
    pct = (saved / total_before * 100) if total_before else 0
    print(f"\n[JPEG SUMMARY] {total_before:.1f}KB -> {total_after:.1f}KB (saved {saved:.1f}KB, {pct:.0f}%)")


def generate_webp():
    targets = [
        "archive-cover-phase1.jpg", "archive-cover-phase2.jpg", "archive-cover-phase3.jpg",
        "archive-cover-phase4.jpg", "archive-cover-phase5.jpg", "archive-cover-phase6.jpg",
        "hero-bg-1.jpg", "hero-bg-2.jpg", "hero-bg-3.jpg", "hero-bg-4.jpg", "hero-bg-5.jpg",
        "eye-hero-bg-1.jpg", "eye-hero-bg-2.jpg", "eye-hero-bg-3.jpg", "eye-hero-bg-4.jpg",
        "wed-hero-bg.jpg", "wed-trees.jpg", "wed-bins-handover.jpg",
        "vipingo-hero-bg.jpg", "vipingo-extraction.jpg", "vipingo-ppe-team.jpg",
        "kuruitu-hero-bg.jpg", "kuruitu-strike-team.jpg", "kuruitu-gallery-5.jpg",
        "olive-hero-bg.jpg", "olive-gallery-1.jpg", "olive-gallery-3.jpg",
        "copa-before.jpg", "copa-after.jpg", "copa-team.jpg",
        "outcomes-hero.jpg", "phase6-main.jpg",
        "intervention-1.jpg", "intervention-2.jpg", "intervention-3.jpg", "intervention-4.jpg",
        "philosophy-main.jpg",
        "infra-installed.jpg", "infra-welding.jpg",
        "bin-photo-1.jpg", "bin-photo-2.jpg", "bin-photo-3.jpg", "bin-photo-4.jpg", "bin-photo-5.jpg",
    ]
    
    print(f"\n[WEBP] Generating WebP versions for {len(targets)} images")
    created = 0
    for name in targets:
        src = IMAGES_DIR / name
        if not src.exists():
            print(f"  [SKIP] {name} not found")
            continue
        
        webp_name = src.with_suffix(".webp").name
        webp_path = IMAGES_DIR / webp_name
        if webp_path.exists():
            print(f"  [SKIP] {webp_name} already exists")
            continue
        
        img = Image.open(src)
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        img.save(webp_path, format="WEBP", quality=WEBP_QUALITY, method=6)
        created += 1
        orig_kb = get_size_kb(src)
        webp_kb = get_size_kb(webp_path)
        print(f"  {name}: {orig_kb:.1f}KB -> {webp_kb:.1f}KB ({webp_name})")
    
    print(f"[WEBP] Created {created} WebP files")


def compress_videos():
    videos = sorted([
        f for f in IMAGES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() == ".mp4"
    ])
    if not videos:
        print("\n[VIDEO] No MP4 files found")
        return
    
    print(f"\n[VIDEO] Found {len(videos)} video files")
    print("[VIDEO] Video compression requires ffmpeg. Please run manually:")
    for v in videos:
        size_mb = v.stat().st_size / (1024 * 1024)
        print(f"  ffmpeg -i \"{v.name}\" -vcodec libx264 -crf 28 -preset slow -acodec aac -b:a 128k \"{v.stem}_compressed.mp4\"")


def main():
    print("=" * 60)
    print("ACT WEB Image Optimization")
    print("=" * 60)
    
    backup_originals()
    optimize_logo()
    optimize_jpegs()
    generate_webp()
    compress_videos()
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
