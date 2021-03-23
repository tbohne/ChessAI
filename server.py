#!/usr/bin/env python

from flask import Flask, render_template, request

from chess_ai import ChessAI

app = Flask(__name__)


@app.route("/")
def root(ai_move="", human_move="", hint_text="", score=0) -> str:
    """
    Returns the html page that displays the current board state.

    Args:
        ai_move:    last move of the AI
        human_move: last move of the human player
        hint_text:  info msg for the user (invalid moves etc.)
        score:      current evaluation of the board from white's perspective

    Returns:
        html page with current board state
    """

    img = "data:image/svg+xml;base64," + ai.get_board_svg()
    score_class = ""
    if score != 0:
        score_class = "neg_score" if score < 0 else "pos_score"

    return render_template('index.html', board_img=img, ai_move=ai_move, human_move=human_move,
                           hint_text=hint_text, score=str(score), score_class=score_class)


@app.route("/move")
def move() -> str:
    """
    Performs a human and an answering AI move and checks for game over situations.

    Returns:
        html page for updated board after performed moves
    """
    player_move = request.args.get('move', default="")
    ai_move, human_move, hint_text, score = ai.move(player_move)
    return root(ai_move, human_move, hint_text, score)


if __name__ == '__main__':
    ai = ChessAI()
    app.run(debug=True)
