#RUN TESTS USING python -m tests.test_scenarios
import chess
from .eval_function import EvaluationFunction

# Initialize the evaluation function
evaluator = EvaluationFunction()

# Global node counter
NODE_COUNT = 0
MAX_NODES = 20000  # Adjust for speed vs accuracy

def evaluate(board: chess.Board) -> int:
    """Wrapper for the full evaluation function."""
    return evaluator.evaluate_board(board)

def alphabeta(board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool):
    """
    Minimax with Alpha-Beta pruning, limited node count, and move ordering.
    """
    global NODE_COUNT
    NODE_COUNT += 1

    # Stop if max nodes reached
    if NODE_COUNT >= MAX_NODES:
        return evaluate(board), None

    # Terminal node
    if depth == 0 or board.is_game_over():
        return evaluate(board), None

    best_move = None

    # --- Generate and order moves ---
    moves = list(board.legal_moves)
    # Prioritize captures for faster pruning
    moves.sort(key=lambda m: board.is_capture(m), reverse=True)

    if maximizing:
        max_eval = -float("inf")
        for move in moves:
            board.push(move)
            eval_score, _ = alphabeta(board, depth-1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in moves:
            board.push(move)
            eval_score, _ = alphabeta(board, depth-1, alpha, beta, True)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move

def iterative_deepening(board: chess.Board, max_depth: int):
    """
    Iterative deepening wrapper for alphabeta. Stops early if MAX_NODES is reached.
    Returns best move and evaluation.
    """
    global NODE_COUNT
    best_move = None
    best_score = None

    for depth in range(1, max_depth + 1):
        NODE_COUNT = 0  # Reset node counter per iteration
        score, move = alphabeta(board, depth, -float("inf"), float("inf"), board.turn)
        if move is not None:
            best_move = move
            best_score = score
        # Stop early if node limit reached
        if NODE_COUNT >= MAX_NODES:
            print(f"Node limit reached at depth {depth}. Stopping search.")
            break

    return best_move, best_score
