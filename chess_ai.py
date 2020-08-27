#!/usr/bin/python3

import base64
import random

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
        legal_moves = [move for move in self.board.legal_moves]
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
                except Exception as e:
                    print(e)
                    human_move = "invalid move: " + move
                    if move == "q":
                        exit(1)

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
        if piece == "P" or piece == "p":
            return 1
        # knight or bishop
        elif piece == "N" or piece == "n" or piece == "B" or piece == "b":
            return 3
        # rook
        elif piece == "R" or piece == "r":
            return 5
        # queen
        elif piece == "Q" or piece == "q":
            return 9
        # king
        elif piece == 'K' or piece == 'k':
            return float('inf')
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
            if self.board.piece_at(i) != None:
                white = self.board.piece_at(i).color
                piece_rating = self.get_piece_rating(str(self.board.piece_at(i)))
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
            maxVal = float('-inf')
            for move in board.legal_moves:
                board.push_uci(str(move))
                maxVal = max(maxVal, self.minimax_step(depth - 1, board, not maximizing))
                board.pop()
            return maxVal
        else:
            minVal = float('inf')
            for move in board.legal_moves:
                board.push_uci(str(move))
                minVal = min(minVal, self.minimax_step(depth - 1, board, not maximizing))
                board.pop()
            return minVal

    def minimax(self, depth, board, maximizing):
        """First minimax step that calls the recursive procedure.

        Args:
            depth: depth of minimax tree
            board: current board to be considered
            maximizing: whether the current step is a maximizing step

        Returns:
            best move to be performed

        """
        bestVal = float('inf')
        bestMove = None

        for move in board.legal_moves:
            board.push_uci(str(move))
            val = min(bestVal, self.minimax_step(
                depth - 1, board, not maximizing))
            board.pop()
            if val < bestVal:
                bestVal = val
                bestMove = move
        return bestMove
