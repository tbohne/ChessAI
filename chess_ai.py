#!/usr/bin/python3 -w

import chess
import chess.svg
import random
from flask import Flask, request
import base64

app = Flask(__name__)

# back rows for black and white
BLACK_BACK = [56, 57, 58, 59, 60, 61, 62, 63]
WHITE_BACK = [0, 1, 2, 3, 4, 5, 6, 7]

@app.route("/")
def root(ai_move="", human_move="", hint_text=""):
    """Returns the html page that displays the current board state.

    Args:
        ai_move: last move of the AI
        human_move: last move of the human player
        hint_text: info msg for the user (invalid moves etc.)

    Returns:
        html page with current board state

    """
    html = '<html><head></head><body style="background-color: #6e6862; text-align: center">'
    html += '<img width=680 src="data:image/svg+xml;base64,%s"></img>' % get_board_svg(board)
    html += '<form action="/move"><input name="move" type="text"></input><br/><input type="submit" value="Move"></input></form>'
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % ai_move
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % human_move
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % hint_text
    html += '</body></html>'
    return html

@app.route("/move")
def move():
    """Performs a human and an answering AI move and checks for game over situations.

    Returns:
        html page for updated board after performed moves

    """
    ai_move = ""
    human_move = ""
    hint_text = ""

    if not board.is_game_over():
        move = request.args.get('move', default="")
        human_move_performed = False

        if move is not None and move != "":
            print("HUMAN MOVE: " + move)
            human_move = "human move: " + move
            try:
                move = pawn_queen_promotion(board, chess.Move.from_uci(move))
                board.push_uci(move)
                human_move_performed = True
            except Exception as e:
                print(e)
                human_move = "invalid move: " + move
                if (move == "q"):
                    exit(1)

        if human_move_performed and board.is_game_over():
            # TODO: check for draw
            hint_text = "HUMAN WINS"
        elif human_move_performed:
            # move = get_random_move()
            print("COMPUTER MOVE")
            move = minimax(3, board, False)
            print("COMPUTER MOVE: " + str(move))
            ai_move = "computer move: " + str(move)
            board.push_uci(str(move))
            if board.is_game_over():
                hint_text = "AI WINS"

    return root(ai_move, human_move, hint_text)

def get_board_svg(board):
    """Returns an SVG representation of the current board state."""
    return base64.b64encode(chess.svg.board(board=board).encode('utf-8')).decode('utf-8')

def get_random_move():
    """Returns a random move from the set of legal moves."""
    legal_moves = [move for move in board.legal_moves]
    move = random.choice(legal_moves)
    return str(move)

def pawn_queen_promotion(board, move):
    """Checks whether the move to be performed could lead to a pawn promotion.
       If so, the pawn always gets promoted to queen.

    Args:
        board: chess board
        move: currently considered move to be performed

    Returns:
        move to be performed

    """
    piece = board.piece_at(move.from_square)
    if piece is not None and piece.piece_type == chess.PAWN:
        if move.to_square in BLACK_BACK or move.to_square in WHITE_BACK and move.promotion is None:
            move = chess.Move(move.from_square, move.to_square, chess.QUEEN)
    return str(move)

###################################################################
###################################################################

def get_piece_rating(piece):
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
        return 999999
    return 0

def evaluation(board):
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
        if board.piece_at(i) != None:
            white = board.piece_at(i).color
            piece_rating = get_piece_rating(str(board.piece_at(i)))
            if white:
                val += piece_rating
            else:
                val -= piece_rating
    return val

def minimax_step(depth, board, maximizing):

    if depth == 0:
        return evaluation(board)

    if maximizing:
        maxVal = float('-inf')
        for move in board.legal_moves:
            board.push_uci(str(move))
            maxVal = max(maxVal, minimax_step(depth - 1, board, not maximizing))
            board.pop()
        return maxVal
    else:
        minVal = float('inf')
        for move in board.legal_moves:
            board.push_uci(str(move))
            minVal = min(minVal, minimax_step(depth - 1, board, not maximizing))
            board.pop()
        return minVal

def minimax(depth, board, maximizing):

    bestVal = float('inf')
    bestMove = None

    for move in board.legal_moves:
        board.push_uci(str(move))
        val = min(bestVal, minimax_step(depth - 1, board, not maximizing))
        board.pop()
        if val < bestVal:
            bestVal = val
            bestMove = move
    return bestMove

###################################################################
###################################################################

if __name__ == '__main__':
    board = chess.Board()
    app.run(debug=True)
