import eval

import chess


def minimax_step(depth: int, maximizing: bool, board: chess.Board) -> float:
    """Performs a step in the minimax algorithm.

    Args:
        depth:      current depth in minimax tree
        maximizing: whether the current step is a maximizing step
        board:      board state to perform minimax for

    Returns:
        minimax value

    """
    if depth == 0:
        return eval.evaluation(board)

    if maximizing:
        max_val = float('-inf')
        for move in board.legal_moves:
            board.push_uci(str(move))
            max_val = max(max_val, minimax_step(depth - 1, not maximizing, board))
            board.pop()
        return max_val

    min_val = float('inf')
    for move in board.legal_moves:
        board.push_uci(str(move))
        min_val = min(min_val, minimax_step(depth - 1, not maximizing, board))
        board.pop()
    return min_val


def minimax(depth: int, maximizing: bool, board: chess.Board) -> chess.Move:
    """First minimax step that calls the recursive procedure.
    Since it's black's move here and black tries to minimize the evaluation function,
    the first minimax step should be a minimizing one.

    Args:
        depth:      depth of minimax tree
        maximizing: whether the current step is a maximizing step
        board:      board state to perform minimax for

    Returns:
        best move to be performed

    """
    best_val = float('inf')
    best_move = None

    for move in board.legal_moves:
        board.push_uci(str(move))
        val = min(best_val, minimax_step(depth - 1, not maximizing, board))
        board.pop()
        if val < best_val:
            best_val = val
            best_move = move
    return best_move
