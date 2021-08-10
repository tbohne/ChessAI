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
        values = torch.load("data/trained_model.pth")
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
        move_dict = {}

        for move in board.legal_moves:
            board.push_uci(str(move))
            output = self.model(torch.tensor(np.array(preprocess.serialize_board_state(board))[None]).float())
            val = output.data[0].item()
            print("net output:", val)
            board.pop()
            move_dict[move] = val
        # sort moves based on value (best first)
        move_dict = {k: v for k, v in sorted(move_dict.items(), key=lambda item: item[1])}
        print(move_dict)

        moves = []
        for key in move_dict.keys():
            moves.append(key)
            if len(moves) == 10:
                break
        return moves
