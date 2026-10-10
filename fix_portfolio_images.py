from pathlib import Path
import re

root = Path.cwd()
html_file = root / "portfolio.html"

if not html_file.exists():
    raise SystemExit("ERROR: portfolio.html was not found.")

content = html_file.read_text(encoding="utf-8")
original = content
updated = 0

for number in list(range(1, 9)) + list(range(10, 15)):
    filename = f"portfolio-{number:02d}"
    pattern = rf"({re.escape(filename)})\.jpg"

    content, count = re.subn(
        pattern,
        r"\1.webp",
        content,
        flags=re.IGNORECASE
    )
    updated += count

html_file.write_text(content, encoding="utf-8")

print(f"Portfolio references updated: {updated}")

if updated == 13:
    print("SUCCESS: All 13 portfolio references now use WebP.")
elif updated == 0 and content == original:
    print("No changes made. The references may already be updated.")
else:
    print("Please verify the output before publishing.")
