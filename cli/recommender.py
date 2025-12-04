import chess
from stockfish import Stockfish

def run_recommender():
    print("=== AI Chess Recommender ===")
    print("Type 'quit' to exit.")
    print()

    board = chess.Board()
    stockfish = Stockfish(path="/usr/games/stockfish")  # adjust path if needed

    while True:
        print(board)

        # Stockfish suggestion (temporary until we add our own AI)
        stockfish.set_fen_position(board.fen())
        best_move = stockfish.get_best_move()

        print(f"AI recommends (Stockfish): {best_move}")

        # Get user input
        user_input = input("Your move (SAN): ")

        if user_input.lower() in ["quit", "exit"]:
            break

        try:
            board.push_san(user_input)
        except Exception:
            print("Invalid move, please try again.\n")
            continue

        if board.is_game_over():
            print("Game over:", board.result())
            break
