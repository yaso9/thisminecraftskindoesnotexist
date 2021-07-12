import os
from argparse import ArgumentParser

import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from torchvision import transforms

from models import Discriminator, Generator
from imagedataset import ImageDataset

REAL_LABEL = 0
FAKE_LABEL = 1


def save(
    path,
    generator,
    discriminator,
    optimizerGenerator,
    optimizerDiscriminator,
    criterion,
    epoch,
):
    torch.save(
        {
            "generator": generator.state_dict(),
            "discriminator": discriminator.state_dict(),
            "optimizers": {
                "generator": optimizerGenerator.state_dict(),
                "discriminator": optimizerDiscriminator.state_dict(),
            },
            "criterion": criterion,
            "epoch": epoch,
        },
        path,
    )


def load(
    path,
    generator,
    discriminator,
    optimizerGenerator,
    optimizerDiscriminator,
):
    state = torch.load(path)

    generator.load_state_dict(state["generator"])
    discriminator.load_state_dict(state["discriminator"])
    optimizerGenerator.load_state_dict(state["optimizers"]["generator"])
    optimizerDiscriminator.load_state_dict(state["optimizers"]["discriminator"])

    return state["criterion"], state["epoch"]


def train(
    generator,
    discriminator,
    criterion,
    optimizerGenerator,
    optimizerDiscriminator,
    loader,
    batch_size,
    epochs,
    save_path,
    start_epoch,
):
    for epoch in range(start_epoch, epochs):
        print(epoch)
        for i, images in enumerate(loader, 0):
            batch_size = images.size(0)

            # Train discriminator
            discriminator.zero_grad()

            # Train the discriminator with real images
            labels = torch.full((batch_size,), REAL_LABEL, dtype=torch.float).to("cuda")
            output = discriminator(images.to("cuda")).view(-1)
            err = criterion(output, labels)
            err.backward()
            print(err)

            # Train the discriminator with generated images
            labels = torch.full((batch_size,), FAKE_LABEL, dtype=torch.float).to("cuda")
            noise = torch.randn(batch_size, 100, 1, 1).to("cuda")
            fake_images = generator(noise)
            output = discriminator(fake_images.detach()).view(-1)
            err = criterion(output, labels)
            err.backward()
            print(err)

            optimizerDiscriminator.step()

            # Train generator
            generator.zero_grad()
            labels = torch.full((batch_size,), REAL_LABEL, dtype=torch.float).to("cuda")
            output = discriminator(fake_images).view(-1)
            err = criterion(output, labels)
            err.backward()
            print(err)
            optimizerGenerator.step()

            print()

        if epoch % 10 == 0:
            save(
                os.path.join(save_path, "checkpoint_{}.pth".format(epoch)),
                generator,
                discriminator,
                optimizerGenerator,
                optimizerDiscriminator,
                criterion,
                epoch,
            )

    save(
        os.path.join(args.save_path, "final.pth"),
        generator,
        discriminator,
        optimizerGenerator,
        optimizerDiscriminator,
        criterion,
        epochs - 1,
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="Train the DCGAN")
    parser.add_argument("images", type=str, help="The path to the images folder")
    parser.add_argument("batch_size", type=int, help="The batch size")
    parser.add_argument("epochs", type=int, help="The number of epochs to run")
    parser.add_argument("save_path", type=str, help="The path to save to")
    parser.add_argument("--load", type=str, default=None, help="The save file to load")
    args = parser.parse_args()

    loader = DataLoader(
        ImageDataset(args.images, transform=transforms.ToTensor()),
        batch_size=args.batch_size,
    )

    generator = Generator().to("cuda")
    discriminator = Discriminator().to("cuda")

    optimizerGenerator = optim.Adam(
        generator.parameters(), lr=0.0002, betas=(0.5, 0.999)
    )
    optimizerDiscriminator = optim.Adam(
        discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999)
    )

    if args.load is not None:
        criterion, epoch = load(
            args.load,
            generator,
            discriminator,
            optimizerGenerator,
            optimizerDiscriminator,
        )
        start_epoch = epoch + 1
    else:
        criterion = nn.BCELoss()
        start_epoch = 0

    train(
        generator,
        discriminator,
        criterion,
        optimizerGenerator,
        optimizerDiscriminator,
        loader,
        args.batch_size,
        args.epochs,
        args.save_path,
        start_epoch,
    )
