"""
Compute the gradient with PyTorch and the KFRA approximation with BackPACK.
"""

from torch.nn import CrossEntropyLoss, Flatten, Linear, Sequential

from backpack import backpack, extend, extensions
from utils import load_mnist_data

B = 64
X, y = load_mnist_data(B)

print(f"# Gradient with PyTorch, KFRA approximation with BackPACK (B={B})")

model = Sequential(
    Flatten(),
    Linear(784, 10),
)
lossfunc = CrossEntropyLoss()

model = extend(model)
lossfunc = extend(lossfunc)

loss = lossfunc(model(X), y)

with backpack(extensions.KFRA()):
    loss.backward()

for name, param in model.named_parameters():
    print(
        f"\n{name}:",
        f"\n\t.grad.shape:    {param.grad.shape}",
        f"\n\t.kfra (shapes): {[kfra.shape for kfra in param.kfra]}",
        # f"\n\t.grad:          {param.grad}",
        # f"\n\t.kfra:          {param.kfra}",
    )