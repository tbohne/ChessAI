from torch.utils.data import Dataset
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class ChessValueDataset(Dataset):

    def __init__(self):
        dat = np.load("data/dataset.npz", allow_pickle=True)
        self.X = dat['arr_0']
        self.Y = dat['arr_1']

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return (self.X[idx], self.Y[idx])

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

        # value oputput
        return torch.tanh(x)

if __name__ == '__main__':

    chess_dataset = ChessValueDataset()
    model = Net()
    num_epochs = 10
    device = 'cpu' #torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_function = nn.CrossEntropyLoss()
    model.to(device)

    train_loader = torch.utils.data.DataLoader(chess_dataset, batch_size=256, shuffle=True)

    total_step = len(chess_dataset)
    for epoch in range(num_epochs):
        for i, (input, target) in enumerate(train_loader):

            target = target.to(device)

            input = input.float()

            print("input during training:", np.array(input).shape)

            target = target.float()

            # Forward pass
            outputs = model(input)

            target = target.reshape(len(target), 1)

            floss = nn.MSELoss()
            loss = floss(outputs, target)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, total_step, loss.item()))
        torch.save(model.state_dict(), "data/value.pth")

