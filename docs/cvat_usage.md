# CVAT Usage Guide

This guide describes how the annotations in this repository were created with
CVAT Community v2.71.0 on Windows, Docker Desktop, and Ubuntu 22.04 WSL.

## 1. Start CVAT

Start Docker Desktop on Windows. Then open Ubuntu 22.04 and move to the local
CVAT repository:

```bash
cd /mnt/c/Users/<Windows-user-name>/Desktop/cvat
docker compose up -d
docker compose ps
```

The services are ready when the containers are shown as `Up`. Open the CVAT
interface in a Windows web browser:

```text
http://localhost:8080
```

If an administrator account has not been created, run:

```bash
docker exec -it cvat_server bash -ic \
  'python3 ~/manage.py createsuperuser'
```

The URL is entered in a web browser, not executed as a terminal command.

## 2. Create an Annotation Task

1. Sign in to CVAT.
2. Open **Tasks** and select **Create a new task**.
3. Enter a task name such as `Class2 Defect Annotation`.
4. Add one label named `defect` with the **Rectangle** shape.
5. Under **Select files**, upload the 20 defective DAGM Class 2 images.
6. Submit the task and wait for data processing to finish.

The task used in this repository has the following settings:

| Setting | Value |
| --- | --- |
| Dataset | DAGM 2007 Class 2 |
| Images | 20 defective images |
| Label | `defect` |
| Shape | Rectangle |

## 3. Draw Bounding Boxes

1. Open the task and select its job.
2. Select the rectangle tool from the left toolbar.
3. Choose the `defect` label.
4. Drag a tight rectangle around the complete visible defect.
5. Adjust the box using its control points when necessary.
6. Move to the next image with the top navigation controls.

Follow the rules in
[`annotation_guideline.md`](annotation_guideline.md) so every image is labeled
consistently.

## 4. Save and Review

Select **Save** in the upper-left corner after editing annotations. Before
exporting, review all frames and confirm that:

- every visible defect has a `defect` rectangle;
- each box contains the complete defect without excessive background;
- no duplicate boxes exist; and
- the object list on the right shows the expected annotations.

Saving stores annotations in CVAT's database. It does not automatically create
a file in the Windows download directory.

## 5. Export COCO Annotations

1. Return to the task page.
2. Open **Actions** and choose **Export task dataset** or **Export annotations**.
3. Select `COCO 1.0` as the format.
4. Disable image export when only annotations are required.
5. Start the export.
6. Open **Requests**, wait until the export reaches `Finished`, and download the
   generated ZIP file from the request menu.

Extract the archive and keep the COCO annotation file as:

```text
annotations/instances_default.json
```

COCO bounding boxes use the following format:

```text
[x, y, width, height]
```

## 6. Validate the Export

From this repository, run:

```bash
python scripts/validate_annotations.py
```

The expected result is:

```text
Images:      20
Annotations: 20
Categories:  1 (defect)
Validation:  OK
```

## 7. Stop CVAT

From the CVAT repository, stop the containers with:

```bash
cd /mnt/c/Users/<Windows-user-name>/Desktop/cvat
docker compose down
```

This removes the running containers and network while preserving CVAT data in
Docker volumes. Run `docker compose up -d` to use the same CVAT installation
again.

To confirm that the containers have stopped:

```bash
docker compose ps
```

