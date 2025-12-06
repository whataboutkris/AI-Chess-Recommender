import chess
from stockfish import Stockfish
import os 
from engine.algorithm import alphabeta  # <-- import your engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_recommender():
    print("=== AI Chess Recommender ===")
    print("Type 'quit' to exit.\n")

    board = chess.Board()

    # --- Path to Stockfish inside the repo ---
    stockfish_path = os.path.join(BASE_DIR, "stockfish", "stockfish.exe")

    # --- Create Stockfish engine instance ---
    stockfish = Stockfish(
        path=stockfish_path,
        depth=15,
        parameters={"Threads": 2, "Minimum Thinking Time": 30}
    )

    SEARCH_DEPTH = 3  # You can raise this later

    while True:
        print(board)
        print()

        # === Our AI's Recommendation ===
        score, ai_move = alphabeta(
            board,
            depth=SEARCH_DEPTH,
            alpha=-1e9,
            beta=1e9,
            maximizing=board.turn  # True = white to move
        )

        print(f"AI (Alpha-Beta, depth {SEARCH_DEPTH}) recommends: {ai_move}   | Eval: {score}")

        # === Stockfish's Recommendation ===
        stockfish.set_fen_position(board.fen())
        sf_move = stockfish.get_best_move()
        print(f"Stockfish recommends: {sf_move}")
        print()

        # === User Move Input ===
        user_input = input("Your move (SAN): ")

        if user_input.lower() in ["quit", "exit"]:
            break

        try:
            board.push_san(user_input)
        except Exception:
            print("Invalid move, try again.\n")
            continue

        print("\n--- Move accepted ---\n")

        # === Check for game end ===
        if board.is_game_over():
            print(board)
            print("Game over:", board.result())
            break
