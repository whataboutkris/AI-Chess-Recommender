import chess
import numpy as np
import math

class EvaluationFunction:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 0
        }

        self.pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
           50, 50, 50, 50, 50, 50, 50, 50,
           10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        
        self.knight_table = [
           -50,-40,-30,-30,-30,-30,-40,-50,
           -40,-20,  0,  0,  0,  0,-20,-40,
           -30,  0, 10, 15, 15, 10,  0,-30,
           -30,  5, 15, 20, 20, 15,  5,-30,
           -30,  0, 15, 20, 20, 15,  0,-30,
           -30,  5, 10, 15, 15, 10,  5,-30,
           -40,-20,  0,  5,  5,  0,-20,-40,
           -50,-40,-30,-30,-30,-30,-40,-50
        ]
        
        self.bishop_table = [
           -20,-10,-10,-10,-10,-10,-10,-20,
           -10,  0,  0,  0,  0,  0,  0,-10,
           -10,  0,  5, 10, 10,  5,  0,-10,
           -10,  5,  5, 10, 10,  5,  5,-10,
           -10,  0, 10, 10, 10, 10,  0,-10,
           -10, 10, 10, 10, 10, 10, 10,-10,
           -10,  5,  0,  0,  0,  0,  5,-10,
           -20,-10,-10,-10,-10,-10,-10,-20
        ]
        
        self.rook_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
           -5,  0,  0,  0,  0,  0,  0, -5,
           -5,  0,  0,  0,  0,  0,  0, -5,
           -5,  0,  0,  0,  0,  0,  0, -5,
           -5,  0,  0,  0,  0,  0,  0, -5,
           -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ]
        
        self.queen_table = [
           -20,-10,-10, -5, -5,-10,-10,-20,
           -10,  0,  0,  0,  0,  0,  0,-10,
           -10,  0,  5,  5,  5,  5,  0,-10,
            -5,  0,  5,  5,  5,  5,  0, -5,
             0,  0,  5,  5,  5,  5,  0, -5,
           -10,  5,  5,  5,  5,  5,  0,-10,
           -10,  0,  5,  0,  0,  0,  0,-10,
           -20,-10,-10, -5, -5,-10,-10,-20
        ]
        
        self.king_middle_table = [
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -30,-40,-40,-50,-50,-40,-40,-30,
           -20,-30,-30,-40,-40,-30,-30,-20,
           -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]
        
        self.king_endgame_table = [
           -50,-40,-30,-20,-20,-30,-40,-50,
           -30,-20,-10,  0,  0,-10,-20,-30,
           -30,-10, 20, 30, 30, 20,-10,-30,
           -30,-10, 30, 40, 40, 30,-10,-30,
           -30,-10, 30, 40, 40, 30,-10,-30,
           -30,-10, 20, 30, 30, 20,-10,-30,
           -30,-30,  0,  0,  0,  0,-30,-30,
           -50,-30,-30,-20,-20,-30,-30,-50
        ]

    def evaluate_board(self, board):
        """ Heuristic evaluation function that scores the board position """
        if board.is_checkmate():
            return -9999 if board.turn else 9999
        
        if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
            return 0

        score = 0

        piece_count = len(board.piece_map())
        is_endgame = piece_count <= 6

        white_material = 0
        black_material = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece is not None:
                piece_value = self.piece_values[piece.piece_type]
                
                if piece.color == chess.WHITE:
                    white_material += piece_value
                else:
                    black_material += piece_value

                flipped_square = chess.square(chess.square_file(square), 7 - chess.square_rank(square))
                
                if piece.piece_type == chess.PAWN:
                    pos_value = self.pawn_table[flipped_square]
                elif piece.piece_type == chess.KNIGHT:
                    pos_value = self.knight_table[flipped_square]
                elif piece.piece_type == chess.BISHOP:
                    pos_value = self.bishop_table[flipped_square]
                elif piece.piece_type == chess.ROOK:
                    pos_value = self.rook_table[flipped_square]
                elif piece.piece_type == chess.QUEEN:
                    pos_value = self.queen_table[flipped_square]
                elif piece.piece_type == chess.KING:
                    pos_value = self.king_endgame_table[flipped_square] if is_endgame else self.king_middle_table[flipped_square]
                else:
                    pos_value = 0
                
                score += pos_value if piece.color == chess.WHITE else -pos_value

        score += white_material - black_material

        white_mobility = len([move for move in board.legal_moves if board.color_at(move.from_square) == chess.WHITE])
        black_mobility = len([move for move in board.legal_moves if board.color_at(move.from_square) == chess.BLACK])
        mobility_bonus = (white_mobility - black_mobility) * 5
        score += mobility_bonus

        king_safety_score = self._evaluate_king_safety(board)
        score += king_safety_score

        pawn_structure_score = self._evaluate_pawn_structure(board)
        score += pawn_structure_score

        tempo_bonus = 10 if board.turn == chess.WHITE else -10
        score += tempo_bonus
        
        return score

    def _evaluate_king_safety(self, board):
        """ Evaluate king safety """
        score = 0

        white_king = board.king(chess.WHITE)
        black_king = board.king(chess.BLACK)

        white_king_safety = self._evaluate_one_king_safety(board, white_king, chess.WHITE)
        black_king_safety = self._evaluate_one_king_safety(board, black_king, chess.BLACK)

        score += white_king_safety - black_king_safety
        
        return score

    def _evaluate_one_king_safety(self, board, king_square, color):
        """ Evaluate safety of a one king """
        safety_score = 0
  
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)

        for file_offset in [-1, 0, 1]:
            for rank_offset in [1, 2] if color == chess.WHITE else [-1, -2]:
                target_file = king_file + file_offset
                target_rank = king_rank + rank_offset
                
                if 0 <= target_file <= 7 and 0 <= target_rank <= 7:
                    target_square = chess.square(target_file, target_rank)
                    piece = board.piece_at(target_square)

                    if piece and piece.piece_type == chess.PAWN and piece.color == color:
                        safety_score += 15

        king_file = chess.square_file(king_square)
        for file_offset in [-1, 0, 1]:
            check_file = king_file + file_offset
            if 0 <= check_file <= 7:
                file_has_our_pawn = False
                file_has_opponent_major = False
                
                for rank in range(8):
                    square = chess.square(check_file, rank)
                    piece = board.piece_at(square)
                    if piece:
                        if piece.piece_type in [chess.PAWN] and piece.color == color:
                            file_has_our_pawn = True
                        elif piece.piece_type in [chess.ROOK, chess.QUEEN] and piece.color != color:
                            if abs(rank - chess.square_rank(king_square)) <= 2:
                                file_has_opponent_major = True
                
                if not file_has_our_pawn and file_has_opponent_major:
                    safety_score -= 20

        if not (king_file in [2, 3, 4, 5] and king_rank in [0, 1, 6, 7]):
            if king_file in [2, 3, 4, 5] and king_rank in [2, 3, 4, 5]:
                safety_score -= 10

        return safety_score

    def _evaluate_pawn_structure(self, board):
        """ Evaluate pawn structure """
        score = 0

        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)

        white_pawn_score = self._evaluate_one_color_pawns(board, white_pawns, chess.WHITE)
        black_pawn_score = self._evaluate_one_color_pawns(board, black_pawns, chess.BLACK)
        
        score += white_pawn_score - black_pawn_score
        
        return score

    def _evaluate_one_color_pawns(self, board, pawns, color):
        """ Evaluate pawn structure for a one color """

        pawn_score = 0
        pawn_files = set()

        for pawn_square in pawns:
            file = chess.square_file(pawn_square)
            pawn_files.add(file)

        for pawn_square in pawns:
            file = chess.square_file(pawn_square)
            rank = chess.square_rank(pawn_square)

            pawns_on_file = 0
            for other_pawn in pawns:
                if chess.square_file(other_pawn) == file:
                    pawns_on_file += 1
            
            if pawns_on_file > 1:
                pawn_score -= 10

            has_adjacent_pawns = False
            for adj_file in [file-1, file+1]:
                if 0 <= adj_file <= 7:
                    for other_pawn in pawns:
                        if chess.square_file(other_pawn) == adj_file:
                            has_adjacent_pawns = True
                            break
                if has_adjacent_pawns:
                    break
            
            if not has_adjacent_pawns:
                pawn_score -= 15

            is_passed = True
            direction = 1 if color == chess.WHITE else -1
            
            for check_file in [file-1, file, file+1]:
                if 0 <= check_file <= 7:
                    for check_rank in range(rank + direction, 8) if color == chess.WHITE else range(rank + direction, -1, -1):
                        check_square = chess.square(check_file, check_rank)
                        piece = board.piece_at(check_square)
                        if piece and piece.piece_type == chess.PAWN and piece.color != color:
                            is_passed = False
                            break
                    if not is_passed:
                        break
            
            if is_passed:
                advancement_bonus = (rank if color == chess.WHITE else 7-rank) * 10
                pawn_score += 30 + advancement_bonus

        return pawn_score


class ChessAlgorithms:
    def __init__(self, depth=3, time_limit=1.0):
        self.depth = depth
        self.time_limit = time_limit
        self.evaluator = EvaluationFunction()
        self.nodes_searched = 0
        self.killer_moves = {}
        self.history_table = {}

    def iterative_deepening_search(self, board):
        """ Perform iterative deepening search to find best move """
        best_move = None
        best_score = 0
        
        for d in range(1, self.depth + 1):
            self.nodes_searched = 0
            score, move = self.minimax_root(board.copy(), d)
            if move:
                best_move = move
                best_score = score
        
        return best_move, best_score, self.nodes_searched

    def minimax_root(self, board, depth):
        """ Root call for minimax with move ordering """
        best_move = None
        best_value = -math.inf if board.turn == chess.WHITE else math.inf
        
        legal_moves = list(board.legal_moves)
        ordered_moves = self.order_moves(board, legal_moves, depth)
        
        for move in ordered_moves:
            board.push(move)
            if board.turn == chess.BLACK:
                value = self.minimax(board, depth - 1, -math.inf, math.inf, False)
            else:
                value = self.minimax(board, depth - 1, -math.inf, math.inf, True)
            board.pop()
            
            if board.turn == chess.WHITE:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
        
        return best_value, best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """ Minimax with alpha-beta pruning """
        self.nodes_searched += 1
        
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate_board(board)

        legal_moves = list(board.legal_moves)
        ordered_moves = self.order_moves(board, legal_moves, depth)
        
        if maximizing_player:
            max_eval = -math.inf
            for move in ordered_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()

                if eval_score >= beta:
                    self.record_killer_move(move, depth)
                    self.update_history(move, depth, depth * depth)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in ordered_moves:
                board.push(move)
                eval_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()

                if eval_score <= alpha:
                    self.record_killer_move(move, depth)
                    self.update_history(move, depth, depth * depth)
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def order_moves(self, board, legal_moves, depth):
        """ Order moves to maximize alpha-beta pruning efficiency """
        ordered_moves = []
        
        for move in legal_moves:
            score = self.score_move(board, move, depth)
            ordered_moves.append((score, move))

        ordered_moves.sort(key=lambda x: x[0], reverse=True)
        return [move for score, move in ordered_moves]
    
    def score_move(self, board, move, depth):
        """ Score a move for ordering purposes """
        score = 0

        if depth in self.killer_moves and move == self.killer_moves[depth]:
            score += 9000

        if (board.turn, move.from_square, move.to_square) in self.history_table:
            score += self.history_table[(board.turn, move.from_square, move.to_square)]

        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                attacker_value = self.evaluator.piece_values[board.piece_at(move.from_square).piece_type]
                victim_value = self.evaluator.piece_values[captured_piece.piece_type]
                score += 8000 + victim_value - attacker_value

        if move.promotion:
            score += 7000

        temp_board = board.copy()
        temp_board.push(move)
        if temp_board.is_check():
            score += 6000

        if board.is_castling(move):
            score += 5000
        
        return score
    
    def record_killer_move(self, move, depth):
        """ Record killer move for future ordering """
        self.killer_moves[depth] = move
    
    def update_history(self, move, depth, improvement):
        """ Update history table with move performance """
        key = (chess.WHITE, move.from_square, move.to_square)
        if key in self.history_table:
            self.history_table[key] += improvement
        else:
            self.history_table[key] = improvement
