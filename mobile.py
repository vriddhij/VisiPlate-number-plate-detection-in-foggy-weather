import torch
from dehazenet import DehazeNet

model = DehazeNet()
model.eval()

example = torch.rand(1, 3, 224, 224)
traced_script_module = torch.jit.trace(model, example)
traced_script_module.save("dehazenet_mobile.pt")
