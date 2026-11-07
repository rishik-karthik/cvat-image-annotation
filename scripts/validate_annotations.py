"""Validate the exported CVAT COCO annotation file."""

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "annotation_file",
        nargs="?",
        type=Path,
        default=Path("annotations/instances_default.json"),
        help="Path to the COCO annotation JSON file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with args.annotation_file.open(encoding="utf-8") as file:
        coco = json.load(file)

    images = coco.get("images", [])
    annotations = coco.get("annotations", [])
    categories = coco.get("categories", [])

    if not images:
        raise ValueError("The COCO file contains no images")
    if not categories:
        raise ValueError("The COCO file contains no categories")

    images_by_id = {image["id"]: image for image in images}
    image_ids = set(images_by_id)
    category_ids = {category["id"] for category in categories}
    annotation_ids = {annotation["id"] for annotation in annotations}

    if len(image_ids) != len(images):
        raise ValueError("Duplicate image IDs found")
    if len(category_ids) != len(categories):
        raise ValueError("Duplicate category IDs found")
    if len(annotation_ids) != len(annotations):
        raise ValueError("Duplicate annotation IDs found")

    for annotation in annotations:
        annotation_id = annotation.get("id", "unknown")
        if annotation.get("image_id") not in image_ids:
            raise ValueError(f"Annotation {annotation_id} references an unknown image")
        if annotation.get("category_id") not in category_ids:
            raise ValueError(f"Annotation {annotation_id} references an unknown category")

        bbox = annotation.get("bbox")
        if not isinstance(bbox, list) or len(bbox) != 4:
            raise ValueError(f"Annotation {annotation_id} has an invalid bbox")

        x, y, width, height = bbox
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            raise ValueError(f"Annotation {annotation_id} has a non-positive bbox")

        image = images_by_id[annotation["image_id"]]
        if x + width > image["width"] or y + height > image["height"]:
            raise ValueError(f"Annotation {annotation_id} extends beyond its image")

    category_names = ", ".join(category["name"] for category in categories)
    print(f"Images:      {len(images)}")
    print(f"Annotations: {len(annotations)}")
    print(f"Categories:  {len(categories)} ({category_names})")
    print("Validation:  OK")


if __name__ == "__main__":
    main()
