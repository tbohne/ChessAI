import numpy as np


class TrainingData:

    def __init__(self):
        data = np.load("data/training_data.npz")
        self.X = data['arr_0']
        self.Y = data['arr_1']

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.Y[idx]
