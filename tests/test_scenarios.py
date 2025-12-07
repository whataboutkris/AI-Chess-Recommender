import time
import chess
from stockfish import Stockfish
from engine.algorithm import alphabeta
from engine.eval_function import EvaluationFunction

STOCKFISH_PATH = "stockfish/stockfish.exe"


def run_ai_vs_stockfish(board: chess.Board, depth: int):
    evaluator = EvaluationFunction()

    print(board)
    print("Eval:", evaluator.evaluate_board(board))

    # --- Run Our Algorithm ---
    start_time = time.time()
    score, move = alphabeta(board, depth=depth, alpha=-float("inf"), beta=float("inf"), maximizing=board.turn)
    ai_time = time.time() - start_time

    print(f"Custom AI recommends: {move}, Score: {score}")
    print(f"Search latency: {ai_time:.2f}s")

    # Nodes/sec
    legal_moves_count = sum(1 for _ in board.legal_moves)
    nodes_per_second = legal_moves_count / ai_time if ai_time > 0 else 0
    print(f"Approx. nodes/sec: {nodes_per_second:.0f}")

    # --- Run Stockfish ---
    try:
        stockfish = Stockfish(path=STOCKFISH_PATH)
        stockfish.set_fen_position(board.fen())
        sf_move = stockfish.get_best_move()
    except Exception as e:
        sf_move = None
        print("Stockfish failed:", e)

    print(f"Stockfish recommends: {sf_move}")

    if sf_move and move and sf_move == move.uci():
        print("Custom AI matched Stockfish's move!")
    else:
        print("Custom AI differs from Stockfish's move.")

    print("-" * 50)
    print()


# --- Original Tests ---
def test_checkmate_in_1():
    print("=== Checkmate in 1 Test ===")
    board = chess.Board("6k1/5ppp/8/8/8/8/6PP/5QRK w - - 0 1")  # Legal mate-in-1
    run_ai_vs_stockfish(board, depth=3)

def test_checkmate_in_2():
    print("=== Checkmate in 2 Test ===")
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1")
    run_ai_vs_stockfish(board, depth=4)

def test_mate_in_2_1():
    print("=== Mate in 2 Puzzle 1 ===")
    board = chess.Board("r4r1k/qp3pNp/p2P1B2/2p5/P7/8/1P1n2PP/4R1K1 w - - 1 0")
    run_ai_vs_stockfish(board, depth=4)

def test_mate_in_2_2():
    print("=== Mate in 2 Puzzle 2 ===")
    board = chess.Board("r2qr1k1/pp3pb1/2n3p1/1N4n1/1P2p2Q/P3p3/1B1P1PP1/R3K2R w KQ - 1 0")
    run_ai_vs_stockfish(board, depth=4)

def test_mate_in_3_1():
    print("=== Mate in 3 Puzzle 1 ===")
    board = chess.Board("2r1k3/ppp2RBp/1bn5/1N1N4/2B1p3/1P2P3/3q2PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=6)

def test_mate_in_3_2():
    print("=== Mate in 3 Puzzle 2 ===")
    board = chess.Board("1r3rk1/pp1n4/1q2pp1Q/3p4/5P2/1P3R1P/P1P1p1P1/b6K w - - 2 25")
    run_ai_vs_stockfish(board, depth=6)

def test_knight_fork():
    print("=== Knight Fork Tactic Test ===")
    board = chess.Board("6k1/8/8/8/8/8/3N4/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_complex_1():
    print("=== Complex Puzzle 1: Central Attack ===")
    board = chess.Board("r1bq1rk1/pp1n1ppp/2pbpn2/3p4/3P4/2NBPN2/PP3PPP/R1BQ1RK1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=4)

def test_complex_2():
    print("=== Complex Puzzle 2: Queenside Attack ===")
    board = chess.Board("2r2rk1/1bqn1ppp/p1np1n2/1p2p3/4P3/1NN1BP2/PPP2QPP/R1B2RK1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=4)

def test_complex_3():
    print("=== Complex Puzzle 3: Pin & Skewer ===")
    board = chess.Board("r3r1k1/1bp1qpp1/p1np1n1p/1p6/3P4/1BN1PN2/PPQ2PPP/3RR1K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=5)

def test_complex_4():
    print("=== Complex Puzzle 4: Rook & Bishop Coordination ===")
    board = chess.Board("r1bq1rk1/pp2ppbp/2n3p1/3p4/3P4/2N1PN2/PPP2PPP/R1BQ1RK1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=4)

def test_complex_5():
    print("=== Complex Puzzle 5: Endgame Coordination ===")
    board = chess.Board("8/4k3/2p1p3/1pP1P3/2P5/3K4/8/8 w - - 0 1")
    run_ai_vs_stockfish(board, depth=6)


# --- 20 Intermediate Puzzles ---
def test_intermediate_1():
    print("=== Intermediate Puzzle 1: Back-Rank Mate Threat ===")
    board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_2():
    print("=== Intermediate Puzzle 2: Knight Fork ===")
    board = chess.Board("6k1/8/8/3N4/8/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_3():
    print("=== Intermediate Puzzle 3: Skewer ===")
    board = chess.Board("6k1/8/8/8/4R3/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_4():
    print("=== Intermediate Puzzle 4: Double Attack ===")
    board = chess.Board("6k1/8/8/8/3Q4/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_5():
    print("=== Intermediate Puzzle 5: Rook Lift Attack ===")
    board = chess.Board("6k1/8/8/8/4R3/8/5PPP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_6():
    print("=== Intermediate Puzzle 6: Queen Pin ===")
    board = chess.Board("6k1/8/3B4/8/8/8/5PPP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_7():
    print("=== Intermediate Puzzle 7: Back Rank Mate Setup ===")
    board = chess.Board("6k1/5ppp/8/8/8/8/6PP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_8():
    print("=== Intermediate Puzzle 8: Knight Sacrifice ===")
    board = chess.Board("6k1/8/8/3N4/8/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_9():
    print("=== Intermediate Puzzle 9: Rook Pin ===")
    board = chess.Board("6k1/8/8/8/4R3/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_10():
    print("=== Intermediate Puzzle 10: Queen Sacrifice ===")
    board = chess.Board("6k1/8/8/8/3Q4/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_11():
    print("=== Intermediate Puzzle 11: Discovered Attack ===")
    board = chess.Board("6k1/8/3B4/8/8/8/5PPP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_12():
    print("=== Intermediate Puzzle 12: Overloaded Piece ===")
    board = chess.Board("6k1/8/8/3N4/8/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_13():
    print("=== Intermediate Puzzle 13: Pin and Skewer ===")
    board = chess.Board("6k1/8/8/8/4R3/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_14():
    print("=== Intermediate Puzzle 14: Bishop Sacrifice ===")
    board = chess.Board("6k1/8/8/8/3Q4/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_15():
    print("=== Intermediate Puzzle 15: Rook Lift with Threat ===")
    board = chess.Board("6k1/8/8/8/4R3/8/5PPP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_16():
    print("=== Intermediate Puzzle 16: Double Check ===")
    board = chess.Board("6k1/8/3B4/8/8/8/5PPP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_17():
    print("=== Intermediate Puzzle 17: Knight Fork Setup ===")
    board = chess.Board("6k1/8/8/3N4/8/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_18():
    print("=== Intermediate Puzzle 18: Pin Across File ===")
    board = chess.Board("6k1/8/8/8/4R3/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_19():
    print("=== Intermediate Puzzle 19: Queen Pressure ===")
    board = chess.Board("6k1/8/8/8/3Q4/8/6PP/6K1 w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)

def test_intermediate_20():
    print("=== Intermediate Puzzle 20: Bishop Fork ===")
    board = chess.Board("6k1/8/3B4/8/8/8/5PPP/5QRK w - - 0 1")
    run_ai_vs_stockfish(board, depth=3)


def run_tests():
    print("Running ALL scenario tests with Stockfish comparison...\n")
    # Original Tests
    test_checkmate_in_1()
    test_checkmate_in_2()
    test_mate_in_2_1()
    test_mate_in_2_2()
    test_mate_in_3_1()
    test_mate_in_3_2()
    test_knight_fork()
    test_complex_1()
    test_complex_2()
    test_complex_3()
    test_complex_4()
    test_complex_5()
    # Intermediate Puzzles
    for i in range(1, 21):
        globals()[f"test_intermediate_{i}"]()
    print("All tests completed!")


if __name__ == "__main__":
    run_tests()
