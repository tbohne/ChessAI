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
def root(hint_text = ""):
    board_svg = to_svg(board)
    html = '<html><head></head><body style="background-color: #6e6862; text-align: center">'
    html += '<html><body><img width=680 src="data:image/svg+xml;base64,%s"></img>' % board_svg
    html += '<form action="/move"><input name="move" type="text"></input><br/><input type="submit" value="Move"></form><br/>'
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % hint_text
    return html


@app.route("/move")
def move():

    hint_text = ""

    if not board.is_game_over():
        move = request.args.get('move', default = "")
        human_move_performed = False

        if move is not None and move != "":
            print("move:", move)
            try:
                board.push_uci(move)
                human_move_performed = True
            except:
                hint_text = "invalid move: " + move
                print(hint_text)
                if (move == "q"):
                    exit(1)

        if human_move_performed and board.is_game_over():
            hint_text = "HUMAN WINS"
        elif human_move_performed:
            random_move()
            if board.is_game_over():
                hint_text = "AI WINS"

    return root(hint_text)


if __name__ == '__main__':
    board = chess.Board()
    app.run(debug = True)