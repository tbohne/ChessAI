import chess.pgn
import numpy as np


def make_matrix(board):
    pgn = board.epd()
    foo = []
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo


def translate(matrix, chess_dict):
    rows = []
    for row in matrix:
        terms = []
        for term in row:
            terms.append(chess_dict[term])
        rows.append(terms)
    return rows


chess_dict = {
    'p': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'P': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'n': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'N': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'b': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'B': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'r': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'R': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'q': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'Q': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'k': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'K': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}


def value_func(res):
    if res == "1/2-1/2":
        return 0
    elif res == "1-0":
        return 1
    elif res == "0-1":
        return -1
    else:
        print("PROBLEM")
        exit(1)


# def fen_to_vec(fen):
#     positions, move_right, castling, en_passant, half_moves, move_num = fen.split(" ")
#     print(move_right)

# def pass_board_to_vec(board, game):
#     move_vec = []
#     move_val = []
#     for i, move in enumerate(game.mainline_moves()):
#         board.push(move)
#         value = game.headers["Result"]
#         matrix = make_matrix(board.copy())
#         rows = translate(matrix, chess_dict)
#         move_vec.append([rows])
#         move_val.append(value_func(value))
#
#     move_vec = np.array(move_vec)#.reshape(1, 8, 8, 12)
#     move_val = np.array(move_val)
#     return move_vec, move_val

def serialize_board_state(board):
    matrix = make_matrix(board.copy())
    rows = translate(matrix, chess_dict)
    return rows


def get_training_data(num_of_examples):
    pgn = open("data/training_games.pgn")
    X = []
    Y = []
    game = chess.pgn.read_game(pgn)
    cnt = 0

    while game:
        if cnt == num_of_examples:
            break
        board = game.board()
        #vec, val = pass_board_to_vec(board, game)

        for i, move in enumerate(game.mainline_moves()):
            board.push(move)
            value = game.headers["Result"]
            board_state = serialize_board_state(board)
            X.append(board_state)
            Y.append(value_func(value))

        game = chess.pgn.read_game(pgn)
        cnt += 1

    X = np.array(X)
    Y = np.array(Y)
    return X, Y


if __name__ == '__main__':

    X, Y = get_training_data(500)
    np.savez("data/dataset.npz", X, Y)



