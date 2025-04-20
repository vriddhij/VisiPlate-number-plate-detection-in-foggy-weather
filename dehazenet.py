import torch
import torch.nn as nn
import torch.nn.functional as F

class DehazeNet(nn.Module):
    def __init__(self):
        super(DehazeNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, padding=2),
            nn.ReLU()
        )
        self.layer2 = nn.Sequential(
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 16, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(16, 1, kernel_size=3, padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        t = self.layer1(x)
        t = self.layer2(t)
        t = self.layer3(t)
        t = self.layer4(t)
        t = F.interpolate(t, size=x.shape[2:], mode='bilinear', align_corners=False)

        # Atmospheric light A assumed as 1 for simplicity
        A = 1.0
        J = (x - A * (1 - t)) / t
        return torch.clamp(J, 0, 1)
