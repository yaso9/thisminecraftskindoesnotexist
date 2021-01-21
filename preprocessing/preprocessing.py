import os
from glob import glob
from uuid import uuid4
from PIL import Image

INPUT_IMAGES_GLOB = "../data/raw/*.png"
OUTPUT_IMAGES_PATH = "../data/preprocessed"

if __name__ == "__main__":
    paths = glob(INPUT_IMAGES_GLOB)
    for path in paths:
        image = Image.open(path).convert("RGB")
        width, height = image.size

        if width == height:
            image.thumbnail((64, 64))
            image = image.crop((0, 0, 64, 32))
        else:
            image.thumbnail((64, 32))
        image.save(os.path.join(OUTPUT_IMAGES_PATH, f"{uuid4()}.png"))
