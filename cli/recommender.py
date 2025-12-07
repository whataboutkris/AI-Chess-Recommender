import chess
from stockfish import Stockfish
import os 
from engine.algorithm import alphabeta  # <-- import your engine
from rich.console import Console
from rich.style import Style

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

console = Console()

# --- Square colors ---
LIGHT_SQUARE = "#EEEED2"  # light square color
DARK_SQUARE  = "#769656"  # dark square color

# --- Piece colors ---
WHITE_PIECE = "white"  # capital letters
BLACK_PIECE = "black"  # lowercase letters

def piece_color(piece):
    if piece == ".":
        return "black"
    elif piece.isupper():
        return WHITE_PIECE
    else:
        return BLACK_PIECE

def print_rich_board(board, square_width=7, square_height=3):
    # --- Split board into rows ---
    rows = str(board).split("\n")
    files = "a b c d e f g h".split()

    # --- Top file coordinates ---
    coord_line = " " * 2  # offset for left rank numbers
    for f in files:
        coord_line += f"{f.center(square_width)}"
    console.print(coord_line)

    # --- Iterate over ranks ---
    for r_idx, row in enumerate(rows):
        rank = 8 - r_idx
        squares = row.split(" ")

        lines = [["" for _ in range(len(squares))] for _ in range(square_height)]

        for c_idx, sq in enumerate(squares):
            is_dark = (r_idx + c_idx) % 2 == 1
            bg = DARK_SQUARE if is_dark else LIGHT_SQUARE

            color = piece_color(sq)

            style = Style(bgcolor=bg, color=color, bold=True)

            piece_char = sq if sq != "." else " "

            for h in range(square_height):
                if h == square_height // 2:
                    lines[h][c_idx] = f"[{style}]{piece_char.center(square_width)}[/{style}]"
                else:
                    lines[h][c_idx] = f"[{style}]{' ' * square_width}[/{style}]"

        for h in range(square_height):
            left_rank = f"{rank}" if h == square_height // 2 else " "
            right_rank = f"{rank}" if h == square_height // 2 else " "
            console.print(left_rank + " " + "".join(lines[h]) + " " + right_rank)

    # --- Bottom file coordinates ---
    console.print(coord_line)

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
        print_rich_board(board)
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
            print_rich_board(board)
            print("Game over:", board.result())
            break
