#!/usr/bin/env python3
"""
ACT WEB HTML Optimization Script
===================================
Adds lazy loading, srcset/sizes, and WebP <picture> elements to all HTML files.

Run this AFTER optimize_images.py so WebP files exist.

Usage:
    python optimize_html.py
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
HTML_FILES = sorted(BASE_DIR.glob("*.html"))

# Images to wrap in <picture> for WebP
PICTURE_IMAGES = {
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
    "bin-photo-1.jpg",
}

# Images to add srcset + sizes
SRCSET_IMAGES = {
    "gallery-1.jpg", "gallery-2.jpg", "gallery-3.jpg", "gallery-4.jpg",
    "wed-gallery-1.jpg", "wed-gallery-2.jpg", "wed-gallery-3.jpg", "wed-gallery-4.jpg", "wed-gallery-5.jpg",
    "wed-walk.jpg",
    "vipingo-drain-before.jpg", "vipingo-sorted.jpg", "vipingo-drain-after.jpg",
    "kuruitu-gallery-1.jpg", "kuruitu-gallery-2.jpg", "kuruitu-gallery-3.jpg",
    "kuruitu-gallery-4.jpg", "kuruitu-gallery-6.jpg", "kuruitu-gallery-7.jpg", "kuruitu-gallery-8.jpg",
    "olive-gallery-2.jpg", "olive-gallery-4.jpg", "olive-gallery-5.jpg",
    "olive-gallery-6.jpg", "olive-gallery-7.jpg", "olive-gallery-8.jpg", "olive-gallery-9.jpg", "olive-gallery-10.jpg",
    "olive-story-1.jpg", "olive-story-2.jpg", "olive-story-3.jpg",
    "copa-sweep.jpg", "copa-briefing.jpg", "copa-debris.jpg", "copa-bins.jpg",
    "eye-consultation.jpg", "eye-crowd.jpg", "eye-dispensing.jpg", "eye-pharmacy.jpg", "eye-triage.jpg", "eye-meal.jpg",
    "infra-welding.jpg", "infra-installed.jpg",
}

# Above-fold images (no lazy loading)
ABOVE_FOLD = {
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


def get_img_filename(src: str) -> str:
    return Path(src).name


def is_picture_candidate(src: str) -> bool:
    return get_img_filename(src) in PICTURE_IMAGES


def is_srcset_candidate(src: str) -> bool:
    return get_img_filename(src) in SRCSET_IMAGES


def should_lazy_load(src: str, existing_loading: str) -> bool:
    if existing_loading:
        return False
    filename = get_img_filename(src)
    if filename in ABOVE_FOLD:
        return False
    if "act-logo.png" in src:
        return True
    return True


def wrap_in_picture(img_tag: str, src: str) -> str:
    webp_src = str(Path(src).with_suffix(".webp"))
    # Only wrap if not already inside picture
    if img_tag.strip().startswith('<picture>'):
        return img_tag
    result = img_tag.replace(
        f'<img src="{src}"',
        f'<picture><source srcset="{webp_src}" type="image/webp"><img src="{src}"'
    )
    # Close the picture tag
    if result != img_tag:
        if result.endswith('/>'):
            result = result[:-2] + '></picture>'
        elif result.endswith('>'):
            result = result + '</picture>'
    return result


def add_srcset(img_tag: str, src: str) -> str:
    if 'srcset=' in img_tag:
        return img_tag
    webp_src = str(Path(src).with_suffix(".webp"))
    sizes = "(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    srcset = f'srcset="{src} 1024w, {webp_src} 1024w" sizes="{sizes}"'
    return img_tag.replace(f'<img src="{src}"', f'<img src="{src}" {srcset}')


def add_lazy_loading(img_tag: str) -> str:
    if 'loading=' in img_tag:
        return img_tag
    return img_tag.replace('<img ', '<img loading="lazy" ', 1)


def process_html(content: str) -> tuple[str, int]:
    changes = 0

    def replace_img(match: re.Match) -> str:
        nonlocal changes
        tag = match.group(0)

        src_match = re.search(r'src=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        if not src_match:
            return tag

        src = src_match.group(1)
        loading_match = re.search(r'loading=["\']([^"\']+)["\']', tag, re.IGNORECASE)
        existing_loading = loading_match.group(1) if loading_match else ""

        original_tag = tag

        # Add lazy loading
        if should_lazy_load(src, existing_loading):
            tag = add_lazy_loading(tag)
            if tag != original_tag:
                changes += 1
                original_tag = tag

        # Wrap in picture for WebP candidates
        if is_picture_candidate(src) and '<picture>' not in tag:
            tag = wrap_in_picture(tag, src)
            if tag != original_tag:
                changes += 1
                original_tag = tag

        # Add srcset for other candidates
        elif is_srcset_candidate(src):
            tag = add_srcset(tag, src)
            if tag != original_tag:
                changes += 1
                original_tag = tag

        return tag

    content = re.sub(r'<img\s[^>]*>', replace_img, content, flags=re.IGNORECASE)
    return content, changes


def main():
    print("=" * 60)
    print("ACT WEB HTML Optimization")
    print("=" * 60)

    total_changes = 0
    for html_file in HTML_FILES:
        if html_file.name in {"optimize_html.py", "optimize_images.py"}:
            continue

        original = html_file.read_text(encoding="utf-8")
        modified, changes = process_html(original)

        if changes > 0:
            html_file.write_text(modified, encoding="utf-8")
            print(f"[OK] {html_file.name}: {changes} changes")
            total_changes += changes
        else:
            print(f"[--] {html_file.name}: no changes needed")

    print(f"\n[SUMMARY] Total changes across all files: {total_changes}")
    print("=" * 60)


if __name__ == "__main__":
    main()
