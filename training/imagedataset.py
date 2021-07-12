import os

from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms, utils


class ImageDataset(Dataset):
    def __init__(self, path, transform=None):
        self.image_paths = [
            f
            for f in [os.path.join(path, f) for f in os.listdir(path)]
            if f.endswith(".png") and os.path.isfile(f)
        ]
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        with Image.open(self.image_paths[idx]) as img:
            if self.transform is not None:
                img = self.transform(img)
            return img
