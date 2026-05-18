import time
from board import HUMAN, AI
from evaluate import evaluate_board, quick_move_score

class SearchStats:
    def __init__(self):
        self.nodes = 0

def order_moves(board, moves, player):
    return sorted(moves, key=lambda m: quick_move_score(board, m, player), reverse=(player == AI))

def minimax(board, depth, maximizing, stats):
    stats.nodes += 1
    result = board.terminal_result()
    if result == AI:
        return 10000000 + depth, None
    if result == HUMAN:
        return -10000000 - depth, None
    if result == 0:
        return 0, None
    if depth == 0:
        return evaluate_board(board), None
    player = AI if maximizing else HUMAN
    moves = order_moves(board, board.get_valid_moves(), player)
    if maximizing:
        best_score = -10**18
        best_move = None
        for r, c in moves:
            board.make_move(r, c, AI)
            score, _ = minimax(board, depth - 1, False, stats)
            board.undo_move(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_score, best_move
    else:
        best_score = 10**18
        best_move = None
        for r, c in moves:
            board.make_move(r, c, HUMAN)
            score, _ = minimax(board, depth - 1, True, stats)
            board.undo_move(r, c)
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return best_score, best_move

def alphabeta(board, depth, alpha, beta, maximizing, stats):
    stats.nodes += 1
    result = board.terminal_result()
    if result == AI:
        return 10000000 + depth, None
    if result == HUMAN:
        return -10000000 - depth, None
    if result == 0:
        return 0, None
    if depth == 0:
        return evaluate_board(board), None
    player = AI if maximizing else HUMAN
    moves = order_moves(board, board.get_valid_moves(), player)
    if maximizing:
        best_score = -10**18
        best_move = None
        for r, c in moves:
            board.make_move(r, c, AI)
            score, _ = alphabeta(board, depth - 1, alpha, beta, False, stats)
            board.undo_move(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = 10**18
        best_move = None
        for r, c in moves:
            board.make_move(r, c, HUMAN)
            score, _ = alphabeta(board, depth - 1, alpha, beta, True, stats)
            board.undo_move(r, c)
            if score < best_score:
                best_score = score
                best_move = (r, c)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

def choose_move(board, depth=3, algorithm='alphabeta'):
    stats = SearchStats()
    start = time.perf_counter()
    algorithm = algorithm.lower().strip()
    if algorithm == 'minimax':
        score, move = minimax(board, depth, True, stats)
    else:
        score, move = alphabeta(board, depth, -10**18, 10**18, True, stats)
    elapsed = time.perf_counter() - start
    return {'algorithm': algorithm, 'depth': depth, 'move': move, 'score': score, 'nodes': stats.nodes, 'time': elapsed, 'time_ms': elapsed * 1000}
