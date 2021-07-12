import torch
from torch import nn
from torch.nn import functional as F


class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.conv_transpose_1 = nn.ConvTranspose2d(100, 512, 4, 1, 0, bias=False)
        self.batch_norm_1 = nn.BatchNorm2d(512)

        self.conv_transpose_2 = nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False)
        self.batch_norm_2 = nn.BatchNorm2d(256)

        self.conv_transpose_3 = nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False)
        self.batch_norm_3 = nn.BatchNorm2d(128)

        self.conv_transpose_4 = nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False)
        self.batch_norm_4 = nn.BatchNorm2d(64)

        self.conv_transpose_5 = nn.ConvTranspose2d(64, 3, 4, 2, 1, bias=False)

    def forward(self, x):
        x = self.conv_transpose_1(x)
        x = self.batch_norm_1(x)
        x = F.relu(x)

        x = self.conv_transpose_2(x)
        x = self.batch_norm_2(x)
        x = F.relu(x)

        x = self.conv_transpose_3(x)
        x = self.batch_norm_3(x)
        x = F.relu(x)

        x = self.conv_transpose_4(x)
        x = self.batch_norm_4(x)
        x = F.relu(x)

        x = self.conv_transpose_5(x)
        x = torch.tanh(x)

        return x


class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.conv_1 = nn.Conv2d(3, 64, 4, 2, 1, bias=False)

        self.conv_2 = nn.Conv2d(64, 128, 4, 2, 1, bias=False)
        self.batch_norm_1 = nn.BatchNorm2d(128)

        self.conv_3 = nn.Conv2d(128, 256, 4, 2, 1, bias=False)
        self.batch_norm_2 = nn.BatchNorm2d(256)

        self.conv_4 = nn.Conv2d(256, 512, 4, 2, 1, bias=False)
        self.batch_norm_3 = nn.BatchNorm2d(512)

        self.conv_5 = nn.Conv2d(512, 1, 4, 1, 0, bias=False)

    def forward(self, x):
        x = self.conv_1(x)
        x = F.leaky_relu(x, 0.2)

        x = self.conv_2(x)
        x = self.batch_norm_1(x)
        x = F.leaky_relu(x, 0.2)

        x = self.conv_3(x)
        x = self.batch_norm_2(x)
        x = F.leaky_relu(x, 0.2)

        x = self.conv_4(x)
        x = self.batch_norm_3(x)
        x = F.leaky_relu(x, 0.2)

        x = self.conv_5(x)
        x = torch.sigmoid(x)

        return x
