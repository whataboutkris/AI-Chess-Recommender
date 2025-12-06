import chess

# TEMPORARY EVALUATION FUNCTION
# Replace with your real evaluate(board) later.
def evaluate(board: chess.Board) -> int:
    """
    Placeholder evaluation function.
    Returns a simple material score for now.
    Positive = White is better.
    Negative = Black is better.
    """
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 300,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0  # don't evaluate king numerically
    }
    
    score = 0
    for piece_type, val in piece_values.items():
        score += (len(board.pieces(piece_type, chess.WHITE)) -
                  len(board.pieces(piece_type, chess.BLACK))) * val

    return score


def alphabeta(board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool):
    """
    Minimax with Alpha-Beta pruning.

    Args:
        board: A python-chess Board object
        depth: Remaining search depth
        alpha: Best already explored option along maximizing path
        beta:  Best already explored option along minimizing path
        maximizing: True if it's white's turn in search, False for black

    Returns:
        (score, best_move)
    """
    # Terminal position or depth reached
    if depth == 0 or board.is_game_over():
        return evaluate(board), None

    best_move = None

    # MAXIMIZING PLAYER (White)
    if maximizing:
        max_eval = -float("inf")

        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = alphabeta(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  # beta cut-off

        return max_eval, best_move

    # MINIMIZING PLAYER (Black)
    else:
        min_eval = float("inf")

        for move in board.legal_moves:
            board.push(move)
            eval_score, _ = alphabeta(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # alpha cut-off

        return min_eval, best_move
