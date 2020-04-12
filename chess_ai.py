import chess
import random
from flask import Flask, Response, request
import chess.svg
import time
import base64


app = Flask(__name__)


def random_move():
    legal_moves = [move for move in board.legal_moves]
    move = random.choice(legal_moves)
    board.push_uci(str(move))


def to_svg(board):
    return base64.b64encode(chess.svg.board(board = board).encode('utf-8')).decode('utf-8')


@app.route("/")
def root():
    board_svg = to_svg(board)
    html = '<html><head></head><body>'
    html += '<html><body><img width=680 src="data:image/svg+xml;base64,%s"></img>' % board_svg
    html += '<form action="/move"><input name="move" type="text"></input><input type="submit" value="Move"></form><br/>'
    return html


@app.route("/move")
def move():
    if not board.is_game_over():
        move = request.args.get('move', default = "")
        human_move_performed = False

        if move is not None and move != "":
            print("move:", move)
            try:
                board.push_uci(move)
                human_move_performed = True
            except:
                print("invalid move..", move)
                if (move == "q"):
                    exit(1)

        if human_move_performed:
            random_move()

    return root()


if __name__ == '__main__':
    board = chess.Board()
    app.run(debug = True)