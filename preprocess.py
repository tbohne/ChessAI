#!/usr/bin/env python

import chess.pgn
import numpy as np

CHESS_DICT = {
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


def get_board_matrix(board: chess.Board) -> list:
    """
    Transforms the specified board into a matrix form (list of rows).

    Args:
        board: chess board state

    Returns:
        matrix: board in matrix form
    """
    rows = board.fen().split(" ", 1)[0].split("/")
    matrix = []
    for row in rows:
        digits = [e for e in row if e.isdigit()]
        for d in digits:
            row = row.replace(d, ("." * int(d)))
        matrix.append(list(row))
    return matrix


def get_neural_board_representation(matrix: list) -> list:
    """
    Transforms the board matrix into a representation the neural net can deal with (bitboard).

    Args:
        matrix: board matrix to be transformed

    Returns:
        bit_board: bitboard representation
    """
    bit_board = [[CHESS_DICT[i] for i in row] for row in matrix]
    return bit_board


def value_func(res: str) -> int:
    """
    Returns a value for the specified chess result.
         1 --> white wins
         0 --> draw
        -1 --> black wins

    Args:
        res: result of chess game

    Returns:
        value for given result
    """
    if res == "1/2-1/2":  # draw
        return 0
    elif res == "1-0":  # white wins
        return 1
    elif res == "0-1":  # black wins
        return -1
    else:
        print("problem - invalid game result:", res)
        exit(1)


def serialize_board_state(board: chess.Board) -> list:
    """
    Serializes the specified board.

    Args:
        board: chess board to be serialized

    Returns:
        bit board representation (serialized version)
    """
    matrix = get_board_matrix(board.copy())
    bit_board = get_neural_board_representation(matrix)
    return bit_board


def get_training_data(num_of_examples, training_data_path):
    """
    Retrieves the training examples from the specified training set.

    Args:
        num_of_examples:    number of examples to be used for training
        training_data_path: path to the training data file (.pgn file - portable game notation)

    Returns:
        board_states: serialized board states
        outcomes:     target values (chess game outcomes)
    """
    pgn = open(training_data_path)
    board_states = []
    outcomes = []
    game = chess.pgn.read_game(pgn)
    cnt = 0

    while game:
        if cnt == num_of_examples:
            break
        board = game.board()

        for move in game.mainline_moves():
            board.push(move)
            board_state = serialize_board_state(board)
            board_states.append(board_state)
            outcomes.append(value_func(game.headers["Result"]))

        print("parsed game ", cnt, "with", len(list(game.mainline_moves())), "board states")
        game = chess.pgn.read_game(pgn)
        cnt += 1

    print("#########################################")
    print("total number of training games:", cnt)
    print("total number of board states:", len(board_states))
    print("#########################################")

    board_states = np.array(board_states)
    outcomes = np.array(outcomes)
    return board_states, outcomes


if __name__ == '__main__':
    X, Y = get_training_data(500, "data/training_games.pgn")
    np.savez("data/training_data.npz", X, Y)
