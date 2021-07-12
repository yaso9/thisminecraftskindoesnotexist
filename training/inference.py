from argparse import ArgumentParser

import torch
from torchvision.utils import save_image

from models import Generator

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a skin")
    parser.add_argument(
        "save_path", type=str, help="The path to load the saved model from"
    )
    parser.add_argument(
        "image_path", type=str, help="The path to save the generated image to"
    )
    args = parser.parse_args()

    generator = Generator().to("cuda")
    generator.load_state_dict(torch.load(args.save_path)['generator'])

    image = generator(torch.randn(1, 100, 1, 1).to("cuda"))
    save_image(image[0], args.image_path)
