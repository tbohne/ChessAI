import torch
import chess
from train import Net
import preprocess
import numpy as np


class ChessNet:

    def __init__(self):
        """
        Loads the trained model.
        """
        values = torch.load("data/value.pth")
        self.model = Net()
        self.model.load_state_dict(values)

    def __call__(self, board: chess.Board) -> chess.Move:
        """
        Evaluates the specified board state using the trained network and suggests a move to be performed.

        Args:
            board: board state to be evaluated

        Returns:
            move to be performed based on the neural nets evaluation
        """
        best_val = 1
        best_move = None
        for move in board.legal_moves:
            board.push_uci(str(move))
            output = self.model(torch.tensor(np.array(preprocess.serialize_board_state(board))[None]).float())
            val = output.data[0].item()
            print("net output:", val)
            board.pop()
            if val < best_val:
                best_val = val
                best_move = move
        print("perf. move:", best_move, " with val:", best_val)
        return best_move
