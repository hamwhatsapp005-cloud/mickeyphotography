from pathlib import Path
from PIL import Image
import os

ROOT = Path.cwd()
PORTFOLIO = ROOT / "Portfolio Images"

# Only process the website's actual image folders.
folders = [ROOT]

if PORTFOLIO.exists():
    folders.append(PORTFOLIO)

extensions = {".jpg", ".jpeg", ".png"}
minimum_size = 200 * 1024  # Skip images smaller than 200 KB.
max_dimension = 2000
quality = 82

total_original = 0
total_optimized = 0
converted = 0

print("\nMICKEY EDITS - IMAGE OPTIMIZATION")
print("=" * 65)

for folder in folders:
    for source in folder.iterdir():
        if not source.is_file():
            continue

        if source.suffix.lower() not in extensions:
            continue

        # Skip small files that are already lightweight.
        if source.stat().st_size < minimum_size:
            continue

        destination = source.with_suffix(".webp")

        try:
            with Image.open(source) as original:
                original_size = source.stat().st_size

                # Work on a copy so the original is never changed.
                image = original.copy()

                # Resize oversized images while preserving proportions.
                image.thumbnail(
                    (max_dimension, max_dimension),
                    Image.Resampling.LANCZOS
                )

                # Preserve transparency when present.
                if "A" in image.getbands():
                    image = image.convert("RGBA")
                else:
                    image = image.convert("RGB")

                image.save(
                    destination,
                    "WEBP",
                    quality=quality,
                    method=6
                )

            optimized_size = destination.stat().st_size

            total_original += original_size
            total_optimized += optimized_size
            converted += 1

            reduction = (
                (1 - optimized_size / original_size) * 100
            )

            print(f"\nOriginal:   {source.relative_to(ROOT)}")
            print(f"Optimized:  {destination.relative_to(ROOT)}")
            print(f"Before:     {original_size / 1024 / 1024:.2f} MB")
            print(f"After:      {optimized_size / 1024 / 1024:.2f} MB")
            print(f"Reduction:  {reduction:.1f}%")

        except Exception as error:
            print(f"\nCould not process {source.name}: {error}")

print("\n" + "=" * 65)
print(f"Images converted: {converted}")

if total_original:
    saved = total_original - total_optimized
    reduction = (saved / total_original) * 100

    print(f"Original total:   {total_original / 1024 / 1024:.2f} MB")
    print(f"WebP total:       {total_optimized / 1024 / 1024:.2f} MB")
    print(f"Space saved:      {saved / 1024 / 1024:.2f} MB")
    print(f"Overall reduction: {reduction:.1f}%")

print("\nOriginal images have not been modified.")
print("These are optimized copies; website references are unchanged.")
