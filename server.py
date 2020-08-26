#!/usr/bin/python3

from flask import Flask, request
from chess_ai import ChessAI

app = Flask(__name__)

@app.route("/")
def root(ai_move="", human_move="", hint_text="", score=0):
    """Returns the html page that displays the current board state.

    Args:
        ai_move: last move of the AI
        human_move: last move of the human player
        hint_text: info msg for the user (invalid moves etc.)
        score: current evaluation of the board from white's perspective

    Returns:
        html page with current board state

    """
    html = '<html><head></head><body style="background-color: #6e6862; text-align: center">'
    html += '<img width=680 src="data:image/svg+xml;base64,%s"></img>' % ai.get_board_svg()
    html += '<form action="/move"><input name="move" type="text"></input><br/><input type="submit" value="Move"></input></form>'
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % ai_move
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % human_move
    html += '<p style="color: #F5F5DC;"><b>%s</b></p>' % hint_text
    color = "E10000" if score < 0 else "00D439"
    html += '<p style="color: %s;"><b>score: %s</b></p>' % (color, str(score))
    html += '</body></html>'
    return html

@app.route("/move")
def move():
    """Performs a human and an answering AI move and checks for game over situations.

    Returns:
        html page for updated board after performed moves

    """
    move = request.args.get('move', default="")
    ai_move, human_move, hint_text, score = ai.move(move)
    return root(ai_move, human_move, hint_text, score)

if __name__ == '__main__':
    ai = ChessAI()
    app.run(debug=True)
