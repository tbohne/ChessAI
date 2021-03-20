import torch
import chess
from train import Net
import preprocess
import numpy as np


class ChessNet:

    def __init__(self):

        # load trained model
        values = torch.load("data/value.pth", map_location=lambda storage, loc: storage)
        self.model = Net()
        self.model.load_state_dict(values)

    def __call__(self, board_state):
        output = self.model(torch.tensor(board_state).float())
        return output.data[0]


if __name__ == '__main__':

    empty_board = preprocess.serialize_board_state(chess.Board())
    chess_net = ChessNet()
    print(chess_net(np.array(empty_board)[None]))
