from pathlib import Path
from PIL import Image

# Source images for Bespoke Furniture - Carousel 2 (images 1-4)
SOURCE_FILES = [
    "bespoke furniture carousel 2 image 1.jpeg",
    "bespoke furniture carousel 2 image 2.jpeg",
    "bespoke furniture carousel 2 image 3.png",
    "bespoke furniture carousel 2 image 4.png",
]

# Target compressed JPEGs (consistent naming)
TARGET_FILES = [
    "compressed_bespoke_furniture_carousel_2_image_1.jpg",
    "compressed_bespoke_furniture_carousel_2_image_2.jpg",
    "compressed_bespoke_furniture_carousel_2_image_3.jpg",
    "compressed_bespoke_furniture_carousel_2_image_4.jpg",
]

MAX_WIDTH = 1600
JPEG_QUALITY = 82


def compress_to_jpeg(src_path: Path, dst_path: Path) -> None:
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w > MAX_WIDTH:
            scale = MAX_WIDTH / float(w)
            new_size = (int(w * scale), int(h * scale))
            im = im.resize(new_size, Image.LANCZOS)
        im.save(dst_path, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)


def main() -> None:
    root = Path(__file__).parent
    for src_name, dst_name in zip(SOURCE_FILES, TARGET_FILES):
        src = root / src_name
        dst = root / dst_name
        if not src.exists():
            print(f"[SKIP] Source not found: {src}")
            continue
        compress_to_jpeg(src, dst)
        print(f"[OK] Wrote {dst}")


if __name__ == "__main__":
    main()


