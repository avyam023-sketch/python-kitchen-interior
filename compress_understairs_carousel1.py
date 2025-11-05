import os
from PIL import Image


def compress_image(input_path: str, output_path: str, quality: int = 72, max_width: int | None = None) -> None:
    image = Image.open(input_path)
    if image.mode in ("RGBA", "P"):  # ensure JPEG compatible
        image = image.convert("RGB")

    if max_width is not None:
        width, height = image.size
        if width > max_width:
            scale = max_width / float(width)
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.LANCZOS)

    image.save(output_path, format="JPEG", optimize=True, quality=quality, progressive=True)


def main() -> None:
    mapping = [
        ("understairs carousel 1 image 1.jpeg", "compressed_understairs_carousel_1_image_1.jpg"),
        ("understairs carousel 1 image 2.png", "compressed_understairs_carousel_1_image_2.jpg"),
        ("understairs carousel 1 image 3.jpeg", "compressed_understairs_carousel_1_image_3.jpg"),
        ("understairs carousel 1 image 4.jpeg", "compressed_understairs_carousel_1_image_4.jpg"),
    ]

    base_dir = os.path.dirname(__file__)
    for src_name, dst_name in mapping:
        src = os.path.join(base_dir, src_name)
        dst = os.path.join(base_dir, dst_name)
        if not os.path.exists(src):
            print(f"[skip] source not found: {src_name}")
            continue
        compress_image(src, dst, quality=72, max_width=1800)
        print(f"[ok] wrote {dst_name}")


if __name__ == "__main__":
    main()








