# RUN TESTS USING python -m tests.test_scenarios
import chess
from .eval_function import EvaluationFunction

evaluator = EvaluationFunction()

TRANSPOSITION_TABLE = {}

NODE_COUNT = 0
MAX_NODES = 20000  # speed vs accuracy
#MAX_NODES = 1000000


def evaluate(board: chess.Board) -> int:
    return evaluator.evaluate_board(board)


def quiescence(board, alpha, beta):
    stand_pat = evaluate(board)

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiescence(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha


def alphabeta(board, depth, alpha, beta, maximizing, metrics=None, root=False):
    """
    Alpha-beta search returning (score, best_move, metrics).
    root=True indicates this call is the root; but function also provides fallbacks if root flag isn't set.
    """
    global NODE_COUNT

    if metrics is None:
        metrics = {
            "nodes_visited": 0,
            "max_depth_reached": 0,
            "pruning_count": 0
        }

    NODE_COUNT += 1
    metrics["nodes_visited"] += 1
    metrics["max_depth_reached"] = max(metrics["max_depth_reached"], depth)

    if NODE_COUNT >= MAX_NODES:
        fallback_move = None
        try:
            fallback_move = next(iter(board.legal_moves))
        except StopIteration:
            fallback_move = None
        return evaluate(board), fallback_move, metrics

    if board.is_checkmate():
        return (-999999 if maximizing else 999999), None, metrics

    if board.is_stalemate() or board.is_insufficient_material():
        return 0, None, metrics

    key = (board.fen(), depth, maximizing)
    if key in TRANSPOSITION_TABLE:
        cached_score, cached_move = TRANSPOSITION_TABLE[key]
        return cached_score, cached_move, metrics

    if depth == 0:
        qscore = quiescence(board, alpha, beta)
        TRANSPOSITION_TABLE[key] = (qscore, None)
        return qscore, None, metrics

    best_move = None

    def move_score(move):
        s = 0
        if board.is_capture(move):
            s += 100
        board.push(move)
        if board.is_check():
            s += 50
        board.pop()
        return s

    moves = sorted(board.legal_moves, key=move_score, reverse=True)

    if maximizing:
        best_score = -float("inf")
        for move in moves:
            if root and best_move is None:
                best_move = move

            board.push(move)
            score, _, metrics = alphabeta(board, depth - 1, alpha, beta, False, metrics, root=False)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if beta <= alpha:
                metrics["pruning_count"] += 1
                break
    else:
        best_score = float("inf")
        for move in moves:
            if root and best_move is None:
                best_move = move

            board.push(move)
            score, _, metrics = alphabeta(board, depth - 1, alpha, beta, True, metrics, root=False)
            board.pop()

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, score)
            if beta <= alpha:
                metrics["pruning_count"] += 1
                break

    if best_move is None:
        try:
            best_move = moves[0]
        except Exception:
            best_move = None

    TRANSPOSITION_TABLE[key] = (best_score, best_move)
    return best_score, best_move, metrics


def iterative_deepening(board: chess.Board, max_depth: int):
    global NODE_COUNT
    best_move = None
    best_score = None

    metrics = {
        "nodes_visited": 0,
        "max_depth_reached": 0,
        "pruning_count": 0
    }

    for depth in range(1, max_depth + 1):
        NODE_COUNT = 0
        score, move, metrics = alphabeta(
            board,
            depth,
            -float("inf"),
            float("inf"),
            board.turn == chess.WHITE,
            metrics,
            root=True
        )

        if move is not None:
            best_move = move
            best_score = score

        if NODE_COUNT >= MAX_NODES:
            break

    return best_move, best_score, metrics