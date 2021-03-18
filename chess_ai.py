#!/usr/bin/python3

import base64
import random
import sys
from typing import Tuple
import minimax
import eval

import chess
import chess.svg

# back rows for black and white
BLACK_BACK = [56, 57, 58, 59, 60, 61, 62, 63]
WHITE_BACK = [0, 1, 2, 3, 4, 5, 6, 7]
MINIMAX_DEPTH = 3


class ChessAI:

    def __init__(self):
        self.board = chess.Board()

    def get_board_svg(self):
        """Provides an SVG representation of the current board state.

        Returns:
            SVG representation of current board state

        """
        svg = chess.svg.board(board=self.board)
        return base64.b64encode(svg.encode('utf-8')).decode('utf-8')

    def get_random_move(self):
        """Returns a random move from the set of legal moves.

        Returns:
            random legal move

        """
        legal_moves = list(self.board.legal_moves)
        move = random.choice(legal_moves)
        return str(move)

    def pawn_queen_promotion(self, move: chess.Move) -> str:
        """Checks whether the move to be performed could lead to a pawn promotion.
        If so, the pawn always gets promoted to a queen.

        Args:
            move: currently considered move to be performed

        Returns:
            move to be performed

        """
        piece = self.board.piece_at(move.from_square)
        is_pawn = piece is not None and piece.piece_type == chess.PAWN
        move_to_back = move.to_square in BLACK_BACK or move.to_square in WHITE_BACK

        if is_pawn and move_to_back and move.promotion is None:
            move = chess.Move(move.from_square, move.to_square, chess.QUEEN)

        return str(move)

    def determine_game_over_situation(self, human_move: bool) -> str:
        """Determines the kind of game over situation (checkmate, stalemate, draw).

        Args:
            human_move: whether the last move is by human (AI otherwise)

        Returns:
            hint text describing the game over situation

        """
        if self.board.is_checkmate():
            if human_move:
                return "HUMAN WINS"
            else:
                return "AI WINS"
        elif self.board.is_stalemate():
            return "STALEMATE"
        elif self.board.is_insufficient_material():
            return "DRAW - INSUFFICIENT MATERIAL"

    def move(self, move: str) -> Tuple[str, str, str, int]:
        """Performs one move of the human player, an answering move of the AI and
        checks for game over situations.

        Args:
            move: human move to be performed

        Returns:
            ai_move:    performed move of the AI
            human_move: performed move of the human player
            hint_text:  optional hint msg (e.g. invalid move)
            score:      current evaluation of the board from white's perspective

        """
        ai_move = human_move = hint_text = ""

        if not self.board.is_game_over():
            human_move_performed = False

            if move is not None and move != "":
                human_move = move
                try:
                    move = self.pawn_queen_promotion(chess.Move.from_uci(move))
                    self.board.push_uci(move)
                    human_move_performed = True
                except Exception as err:
                    print(err)
                    hint_text = "invalid move: " + move
                    human_move = ""
                    if move == "q":
                        sys.exit(1)

            if human_move_performed and self.board.is_game_over():
                hint_text = self.determine_game_over_situation(True)
            elif human_move_performed:
                move = minimax.minimax(MINIMAX_DEPTH, False, self.board)
                ai_move = str(move)
                self.board.push_uci(str(move))
                if self.board.is_game_over():
                    self.determine_game_over_situation(False)

        score = eval.evaluation(self.board)
        return ai_move, human_move, hint_text, score
