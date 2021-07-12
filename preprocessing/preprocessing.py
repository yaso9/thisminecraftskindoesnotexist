import os
from glob import glob
from uuid import uuid4
from multiprocessing import Pool
from PIL import Image, ImageDraw

INPUT_IMAGES_GLOB = "../data/raw/*.png"
OUTPUT_IMAGES_PATH = "../data/preprocessed"


def process_image(path):
    image = Image.open(path).convert("RGB")
    width, height = image.size

    if width == height:
        image.thumbnail((64, 64))
        draw = ImageDraw.Draw(image)
        draw.rectangle([(0, 32), (64, 64)], fill=(1, 1, 1))
    else:
        new_image = Image.new(mode="RGB", size=(64, 64))
        image.thumbnail((64, 32))
        new_image.paste(image, (0, 0))
        image = new_image
    image.save(os.path.join(OUTPUT_IMAGES_PATH, f"{uuid4()}.png"))


if __name__ == "__main__":
    paths = glob(INPUT_IMAGES_GLOB)

    pool = Pool(16)
    list(pool.map(process_image, paths))
