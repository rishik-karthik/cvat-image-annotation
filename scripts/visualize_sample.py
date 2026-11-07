"""Render the first COCO defect annotation as a red bounding box."""

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--annotations",
        type=Path,
        default=Path("annotations/instances_default.json"),
        help="Path to the COCO annotation JSON file",
    )
    parser.add_argument(
        "--images",
        type=Path,
        default=Path("DAGM2007/Class2_def"),
        help="Directory containing the original DAGM images",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("samples"),
        help="Directory for the original and annotated samples",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with args.annotations.open(encoding="utf-8") as file:
        coco = json.load(file)

    if not coco.get("images"):
        raise ValueError("The COCO file contains no images")

    image_record = coco["images"][0]
    image_id = image_record["id"]
    file_name = Path(image_record["file_name"]).name
    source_path = args.images / file_name
    if not source_path.is_file():
        raise FileNotFoundError(f"Original image not found: {source_path}")

    annotations = [
        annotation
        for annotation in coco.get("annotations", [])
        if annotation["image_id"] == image_id
    ]

    original_directory = args.output / "original"
    annotated_directory = args.output / "annotated"
    original_directory.mkdir(parents=True, exist_ok=True)
    annotated_directory.mkdir(parents=True, exist_ok=True)

    original_path = original_directory / file_name
    annotated_path = annotated_directory / file_name
    shutil.copy2(source_path, original_path)

    with Image.open(source_path).convert("RGB") as image:
        draw = ImageDraw.Draw(image)
        for annotation in annotations:
            x, y, width, height = annotation["bbox"]
            draw.rectangle(
                (x, y, x + width, y + height),
                outline=(255, 0, 0),
                width=2,
            )
        image.save(annotated_path)

    print(f"Image:       {file_name}")
    print(f"Annotations: {len(annotations)}")
    print(f"Original:    {original_path}")
    print(f"Annotated:   {annotated_path}")


if __name__ == "__main__":
    main()
