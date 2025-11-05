from pathlib import Path
from PIL import Image

FILES_TO_COMPRESS = [
    "understairs carousel 2 image 1.jpeg",
    "understairs carousel 2 image 2.jpeg",
    "understairs carousel 2 image 3.jpeg",
    "understairs carousel 2 image 4.jpeg",
]


def compress_to_jpeg(input_path: Path) -> Path:
    output_name = "compressed_" + input_path.stem.replace(" ", "_") + ".jpg"
    output_path = input_path.with_name(output_name)

    with Image.open(input_path) as image:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(output_path, "JPEG", quality=75, optimize=True, progressive=True)

    return output_path


def main() -> None:
    for file_name in FILES_TO_COMPRESS:
        src = Path(file_name)
        if not src.exists():
            print(f"SKIP (not found): {file_name}")
            continue
        try:
            dst = compress_to_jpeg(src)
            print(f"WROTE: {dst.name}")
        except Exception as error:
            print(f"ERROR processing {file_name}: {error}")


if __name__ == "__main__":
    main()
