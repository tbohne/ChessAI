#!/usr/bin/env python

from torch.utils.data import Dataset
from training_data import TrainingData
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.a1 = nn.Conv2d(8, 16, kernel_size=3)
        self.a2 = nn.Conv2d(16, 16, kernel_size=3)
        self.a3 = nn.Conv2d(16, 32, kernel_size=3)

        self.b1 = nn.Conv2d(32, 32, kernel_size=3, padding=2)
        self.b2 = nn.Conv2d(32, 32, kernel_size=3, padding=2)
        self.b3 = nn.Conv2d(32, 64, kernel_size=3, padding=2)

        self.c1 = nn.Conv2d(64, 64, kernel_size=2)
        self.c2 = nn.Conv2d(64, 64, kernel_size=2)
        self.c3 = nn.Conv2d(64, 128, kernel_size=2, padding=1)

        self.d1 = nn.Conv2d(128, 128, kernel_size=2)
        self.d2 = nn.Conv2d(128, 128, kernel_size=2)
        self.d3 = nn.Conv2d(128, 128, kernel_size=2)

        self.last = nn.Linear(128, 1)

    def forward(self, x):
        x = F.relu(self.a1(x))
        x = F.relu(self.a2(x))
        x = F.relu(self.a3(x))
        x = F.max_pool2d(x, 2)

        # 4x4
        x = F.relu(self.b1(x))
        x = F.relu(self.b2(x))
        x = F.relu(self.b3(x))
        x = F.max_pool2d(x, 2)

        # 2x2
        x = F.relu(self.c1(x))
        x = F.relu(self.c2(x))
        x = F.relu(self.c3(x))
        x = F.max_pool2d(x, 2)

        # 1x128
        x = x.view(-1, 128)
        x = self.last(x)

        # value output
        return torch.tanh(x)


def train_model(net, dataset):
    num_epochs = 10
    # TODO: test gpu training
    device = 'cpu'
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    net.to(device)
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=256, shuffle=True)

    for epoch in range(num_epochs):
        for i, (input, target) in enumerate(train_loader):
            target = target.to(device).float()

            # Forward pass
            outputs = net(input.float())

            target = target.reshape(len(target), 1)
            floss = nn.MSELoss()
            loss = floss(outputs, target)

            # backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(
                epoch + 1, num_epochs, i + 1, len(train_loader), loss.item()))


if __name__ == '__main__':
    data = TrainingData()
    model = Net()
    train_model(model, data)
    torch.save(model.state_dict(), "data/trained_model.pth")
