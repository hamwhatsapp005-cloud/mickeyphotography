from pathlib import Path
import re

root = Path.cwd()

# Update only website HTML and CSS files.
extensions = {".html", ".css"}

# Match the exact image names, including their extensions.
image_extensions = {".jpg", ".jpeg", ".png"}

updated_files = 0
updated_references = 0

for file in root.rglob("*"):
    if not file.is_file():
        continue

    if file.suffix.lower() not in extensions:
        continue

    # Avoid changing generated or dependency files.
    if any(part.lower() in {".git", "node_modules"} for part in file.parts):
        continue

    text = file.read_text(encoding="utf-8")
    original = text

    def replace_image(match):
        global updated_references

        filename = match.group(0)
        path = Path(filename)

        if path.suffix.lower() not in image_extensions:
            return filename

        webp_path = path.with_suffix(".webp")

        # Check that the optimized image exists beside the original.
        local_path = file.parent / webp_path

        if not local_path.exists():
            return filename

        updated_references += 1
        return str(webp_path).replace("\\", "/")

    # Replace only the filenames that have matching WebP files.
    pattern = r'(?<![\w.-])[\w./% -]+\.(?:jpg|jpeg|png)'
    text = re.sub(pattern, replace_image, text, flags=re.IGNORECASE)

    if text != original:
        file.write_text(text, encoding="utf-8")
        updated_files += 1
        print(f"Updated: {file.relative_to(root)}")

print("\nReference update finished.")
print(f"Files updated: {updated_files}")
print(f"Image references updated: {updated_references}")
