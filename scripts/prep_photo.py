from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


INPUT_FILE = Path("source-photo.png")
OUTPUT_FILE = Path("source-prepped.png")


def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}. "
            "Make sure source-photo.png is in the repository root."
        )

    print("Loading photo...")

    # 1. Remove background
    print("Removing background...")

    with open(INPUT_FILE, "rb") as f:
        input_image = f.read()

    output_image = remove(input_image)

    temp_file = Path("source-no-bg.png")

    with open(temp_file, "wb") as f:
        f.write(output_image)

    # 2. Open image
    image = Image.open(temp_file).convert("RGBA")

    # 3. Put subject on white background
    print("Creating white background...")

    background = Image.new(
        "RGBA",
        image.size,
        (255, 255, 255, 255)
    )

    background.alpha_composite(image)

    rgb_image = background.convert("RGB")

    # 4. Convert to OpenCV format
    img = np.array(rgb_image)

    img = cv2.cvtColor(
        img,
        cv2.COLOR_RGB2BGR
    )

    # 5. Convert to grayscale
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # 6. Improve contrast
    print("Enhancing contrast...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # 7. Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    sharpened = cv2.filter2D(
        enhanced,
        -1,
        kernel
    )

    # 8. Save
    cv2.imwrite(
        str(OUTPUT_FILE),
        sharpened
    )

    print()
    print("Done!")
    print(f"Created: {OUTPUT_FILE}")

    # Remove temporary file
    if temp_file.exists():
        temp_file.unlink()


if __name__ == "__main__":
    main()