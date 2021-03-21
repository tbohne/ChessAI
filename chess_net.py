import torch
import chess
from train import Net
import preprocess
import numpy as np


class ChessNet:

    def __init__(self):
        # load trained model
        values = torch.load("data/value.pth")
        self.model = Net()
        self.model.load_state_dict(values)

    def __call__(self, board_state):
        output = self.model(torch.tensor(board_state).float())
        return output.data[0]


def chess_net_move(net, board: chess.Board) -> chess.Move:
    # TODO: is 1-0 a win for white? then the AI should go for the min value, otherwise max?

    best_val = 1
    best_move = None

    for move in board.legal_moves:
        board.push_uci(str(move))
        val = net(np.array(preprocess.serialize_board_state(board))[None])
        board.pop()
        if val < best_val:
            print(val)
            print(move)
            best_val = val
            best_move = move
    return best_move
