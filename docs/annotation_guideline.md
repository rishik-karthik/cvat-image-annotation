# Annotation Guideline

## Scope

- Dataset: DAGM 2007 Class 2
- Sample type: defective surface images
- Label: `defect`
- Shape: rectangle
- Tool: CVAT Community v2.71.0

## Bounding-Box Rules

1. Annotate each visible defect with one bounding box.
2. Include the complete visible defect inside the box.
3. Keep the box tight and minimize surrounding background texture.
4. Use separate boxes for spatially separated defects.
5. Do not annotate normal texture variations as defects.
6. Apply the same criteria consistently to every image.

## Review Checklist

- The label is `defect`.
- No visible defect is missing.
- The entire defect is inside the bounding box.
- The box does not contain excessive background.
- Duplicate boxes have not been created.
- The annotation is saved before moving to the next image.

## Export

Annotations are exported from CVAT using the `COCO 1.0` format without the
original images. COCO bounding boxes follow `[x, y, width, height]` format.
