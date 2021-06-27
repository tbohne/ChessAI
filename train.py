#!/usr/bin/env python

from training_data import TrainingData
import torch
import torch.nn as nn
import numpy as np

INPUT_SIZE = 8
HIDDEN_SIZE = 128
NUM_CLASSES = 1
BATCH_SIZE = 256
LEARNING_RATE = 0.0001
NUM_EPOCHS = 64


class Net(nn.Module):

    def __init__(self):
        super().__init__()

        # input shape: [batch_size, 8, 8, 12]
        # 8x8 board and 12 features (one-hot)

        self.conv1 = nn.Conv2d(INPUT_SIZE, INPUT_SIZE * 2, kernel_size=3, padding=2)
        self.conv2 = nn.Conv2d(INPUT_SIZE * 2, INPUT_SIZE * 4, kernel_size=3, padding=2)
        self.conv3 = nn.Conv2d(INPUT_SIZE * 4, INPUT_SIZE * 8, kernel_size=3, padding=2)
        self.conv4 = nn.Conv2d(INPUT_SIZE * 8, HIDDEN_SIZE, kernel_size=3, padding=2)
        self.conv5 = nn.Conv2d(HIDDEN_SIZE, HIDDEN_SIZE, kernel_size=3, padding=2)
        self.conv6 = nn.Conv2d(HIDDEN_SIZE, HIDDEN_SIZE, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 1 * 1, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, 64)
        self.fc3 = nn.Linear(64, NUM_CLASSES)

        self.relu = nn.ReLU()

    def forward(self, x):
        # define feed-forward neural net --> how the data flows through the net

        out = self.pool(self.relu(self.conv1(x)))
        out = self.pool(self.relu(self.conv2(out)))
        out = self.pool(self.relu(self.conv3(out)))
        out = self.pool(self.relu(self.conv4(out)))
        out = self.pool(self.relu(self.conv5(out)))
        out = self.pool(self.relu(self.conv6(out)))

        out = out.view(-1, 128 * 1 * 1)
        out = self.relu(self.fc1(out))
        out = self.relu(self.fc2(out))
        out = self.fc3(out)
        return torch.tanh(out)


def train_model(net):
    # gpu training
    device = 'cuda'
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=LEARNING_RATE)

    for dataset in range(1, 5):
        data = None
        if dataset == 1:
            print("data set 1......")
            data = TrainingData(np.load("data/training_data1.npz"))
        elif dataset == 2:
            print("data set 2......")
            data = TrainingData(np.load("data/training_data2.npz"))
        elif dataset == 3:
            print("data set 3......")
            data = TrainingData(np.load("data/training_data3.npz"))
        else:
            print("data set 4......")
            data = TrainingData(np.load("data/training_data4.npz"))

        # batch size of 1 means to consider only one (board state - result) pair at a time
        train_loader = torch.utils.data.DataLoader(data, batch_size=BATCH_SIZE, shuffle=True)

        for epoch in range(NUM_EPOCHS):
            for i, (input, target) in enumerate(train_loader):

                input = input.to(device).cuda().float()
                target = target.reshape(len(target), 1).to(device).cuda().float()

                # forward
                outputs = model(input)
                loss = criterion(outputs, target)

                # backward
                optimizer.zero_grad()
                # backpropagation
                loss.backward()
                # adjust weights
                optimizer.step()
                if i % 10 == 0:
                    print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch + 1, NUM_EPOCHS, i + 1,
                                                                             len(train_loader), loss.item()))


if __name__ == '__main__':
    model = Net()
    model.cuda()
    train_model(model)
    torch.save(model.state_dict(), "data/trained_model.pth")
