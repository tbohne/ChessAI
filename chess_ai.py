#!/usr/bin/python3

import base64
import random
import sys

import chess
import chess.svg

# back rows for black and white
BLACK_BACK = [56, 57, 58, 59, 60, 61, 62, 63]
WHITE_BACK = [0, 1, 2, 3, 4, 5, 6, 7]


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

    def pawn_queen_promotion(self, move):
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

    def move(self, move):
        """Performs one move of the human player, an answering move of the AI and
        checks for game over situations.

        Args:
            move: human move to be performed

        Returns:
            ai_move: performed move of the AI
            human_move: performed move of the human player
            hint_text: optional hint msg (e.g. invalid move)
            score: current evaluation of the board from white's perspective

        """
        ai_move = human_move = hint_text = ""

        if not self.board.is_game_over():
            human_move_performed = False

            if move is not None and move != "":
                human_move = "human move: " + move
                try:
                    move = self.pawn_queen_promotion(chess.Move.from_uci(move))
                    self.board.push_uci(move)
                    human_move_performed = True
                except Exception as err:
                    print(err)
                    human_move = "invalid move: " + move
                    if move == "q":
                        sys.exit(1)

            if human_move_performed and self.board.is_game_over():
                # TODO: check for draw
                hint_text = "HUMAN WINS"
            elif human_move_performed:
                move = self.minimax(3, self.board, False)
                ai_move = "computer move: " + str(move)
                self.board.push_uci(str(move))
                if self.board.is_game_over():
                    hint_text = "AI WINS"

        score = self.evaluation(self.board)
        return ai_move, human_move, hint_text, score

    def get_piece_rating(self, piece):
        """Returns a rating for the specified piece.

        Args:
            piece: chess piece

        Returns:
            rating for the piece

        """
        # pawn
        if piece in ('P', 'p'):
            return 1
        # knight or bishop
        if piece in ('N', 'n', 'B', 'b'):
            return 3
        # rook
        if piece in ('R', 'r'):
            return 5
        # queen
        if piece in ('Q', 'q'):
            return 9
        # king
        if piece in ('K', 'k'):
            return 9999
        return 0

    def evaluation(self, board):
        """Evaluates the current board state.

            Large values would favor white while small values would favor black.
            --> white tries to maximize the evaluation
            --> black tries to minimize the evaluation

        Args:
            board: current board

        Returns:
            evaluation value

        """
        val = 0
        for i in range(64):
            if board.piece_at(i) is not None:
                white = board.piece_at(i).color
                piece_rating = self.get_piece_rating(str(board.piece_at(i)))
                if white:
                    val += piece_rating
                else:
                    val -= piece_rating
        return val

    def minimax_step(self, depth, board, maximizing):
        """Performs a step in the minimax algorithm.

        Args:
            depth: current depth in minimax tree
            board: current board to be considered
            maximizing: whether the current step is a maximizing step

        Returns:
            minimax value

        """
        if depth == 0:
            return self.evaluation(board)

        if maximizing:
            max_val = float('-inf')
            for move in board.legal_moves:
                board.push_uci(str(move))
                max_val = max(max_val, self.minimax_step(depth - 1, board, not maximizing))
                board.pop()
            return max_val

        min_val = float('inf')
        for move in board.legal_moves:
            board.push_uci(str(move))
            min_val = min(min_val, self.minimax_step(depth - 1, board, not maximizing))
            board.pop()
        return min_val

    def minimax(self, depth, board, maximizing):
        """First minimax step that calls the recursive procedure.

        Args:
            depth: depth of minimax tree
            board: current board to be considered
            maximizing: whether the current step is a maximizing step

        Returns:
            best move to be performed

        """
        best_val = float('inf')
        best_move = None

        for move in board.legal_moves:
            board.push_uci(str(move))
            val = min(best_val, self.minimax_step(depth - 1, board, not maximizing))
            board.pop()
            if val < best_val:
                best_val = val
                best_move = move
        return best_move
