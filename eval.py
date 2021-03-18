import chess


def get_piece_rating(piece: str) -> int:
    """Returns a rating for the specified piece.

    Args:
        piece: chess piece

    Returns:
        rating for the piece

    """
    # pawn
    if piece in ('P', 'p'):
        return 1
    # knight or bishop
    if piece in ('N', 'n', 'B', 'b'):
        return 3
    # rook
    if piece in ('R', 'r'):
        return 5
    # queen
    if piece in ('Q', 'q'):
        return 9
    # king
    if piece in ('K', 'k'):
        return 9999
    return 0


def evaluation(board: chess.Board) -> int:
    """Evaluates the current board state.

        Large values would favor white while small values would favor black.
        --> white tries to maximize the evaluation
        --> black tries to minimize the evaluation

    Args:
        board: board to be evaluated

    Returns:
        evaluation value

    """
    val = 0
    for i in range(64):
        if board.piece_at(i) is not None:
            white = board.piece_at(i).color
            piece_rating = get_piece_rating(str(board.piece_at(i)))
            if white:
                val += piece_rating
            else:
                val -= piece_rating
    return val
