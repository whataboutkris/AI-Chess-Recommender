#RUN TESTS USING python -m tests.test_scenarios
import chess
from .eval_function import EvaluationFunction

# Initialize the evaluation function
evaluator = EvaluationFunction()

# Global node counter (optional for iterative deepening)
NODE_COUNT = 0
#MAX_NODES = 20000  # Adjust for speed vs accuracy (20k vs 1mil nodes)
MAX_NODES = 1000000  

def evaluate(board: chess.Board) -> int:
    """Wrapper for the full evaluation function."""
    return evaluator.evaluate_board(board)


def alphabeta(board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool, metrics=None):
    """
    Minimax with Alpha-Beta pruning, limited node count, move ordering, and metrics tracking.
    metrics: dict containing 'nodes_visited', 'max_depth_reached', 'pruning_count'
    """
    global NODE_COUNT
    NODE_COUNT += 1

    if metrics is None:
        metrics = {"nodes_visited": 0, "max_depth_reached": 0, "pruning_count": 0}

    # Update metrics
    metrics["nodes_visited"] += 1
    metrics["max_depth_reached"] = max(metrics["max_depth_reached"], depth)

    # Stop if max nodes reached
    if NODE_COUNT >= MAX_NODES:
        return evaluate(board), None, metrics

    # Terminal node
    if depth == 0 or board.is_game_over():
        return evaluate(board), None, metrics

    best_move = None

    # --- Generate and order moves ---
    moves = list(board.legal_moves)
    # Prioritize captures for faster pruning
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)

    if maximizing:
        max_eval = -float("inf")
        for move in moves:
            board.push(move)
            eval_score, _, metrics = alphabeta(board, depth-1, alpha, beta, False, metrics)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)
            if beta <= alpha:
                metrics["pruning_count"] += 1  # Count cutoffs
                break  # Beta cut-off
        return max_eval, best_move, metrics
    else:
        min_eval = float("inf")
        for move in moves:
            board.push(move)
            eval_score, _, metrics = alphabeta(board, depth-1, alpha, beta, True, metrics)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)
            if beta <= alpha:
                metrics["pruning_count"] += 1  # Count cutoffs
                break  # Alpha cut-off
        return min_eval, best_move, metrics


def iterative_deepening(board: chess.Board, max_depth: int):
    """
    Iterative deepening wrapper for alphabeta. Stops early if MAX_NODES is reached.
    Returns best move, evaluation, and metrics.
    """
    global NODE_COUNT
    best_move = None
    best_score = None
    metrics = {"nodes_visited": 0, "max_depth_reached": 0, "pruning_count": 0}

    for depth in range(1, max_depth + 1):
        NODE_COUNT = 0  # Reset node counter per iteration
        score, move, metrics = alphabeta(board, depth, -float("inf"), float("inf"), board.turn, metrics)
        if move is not None:
            best_move = move
            best_score = score
        # Stop early if node limit reached
        if NODE_COUNT >= MAX_NODES:
            print(f"Node limit reached at depth {depth}. Stopping search.")
            break

    return best_move, best_score, metrics