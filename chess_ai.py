import chess
import random


def random_move():
    legal_moves = [move for move in board.legal_moves]
    move = random.choice(legal_moves)
    board.push_uci(str(move))


def visualize_board():
    print("#####################")
    print("#####################")
    print(board)
    print("#####################")
    print("#####################")


def run_game():
    while not board.is_game_over():
        while True:
            try:
                move = input()
                board.push_uci(move)
                visualize_board()
                if board.is_game_over():
                    print("PLAYER WINS")
                break
            except:
                print("invalid move..", move)
                if (move == "q"):
                    exit(1)
        random_move()
        if board.is_game_over():
            print("AI WINS")
        visualize_board()


if __name__ == '__main__':
    board = chess.Board()
    visualize_board()
    run_game()