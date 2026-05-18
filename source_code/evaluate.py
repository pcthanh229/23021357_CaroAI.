from board import EMPTY, HUMAN, AI, WIN_LEN

SCORES = {4: 1000000, 3: 20000, 2: 1000, 1: 10}

def opponent(player):
    return HUMAN if player == AI else AI

def evaluate_line(cells, player):
    other = opponent(player)
    p_count = cells.count(player)
    o_count = cells.count(other)
    if p_count > 0 and o_count > 0:
        return 0
    if p_count == 4:
        return SCORES[4]
    if o_count == 4:
        return -SCORES[4]
    if p_count > 0:
        return SCORES.get(p_count, 0)
    if o_count > 0:
        return -int(SCORES.get(o_count, 0) * 1.2)
    return 0

def evaluate_board(board):
    if board.check_winner(AI):
        return 10000000
    if board.check_winner(HUMAN):
        return -10000000
    total = 0
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for r in range(board.size):
        for c in range(board.size):
            for dr, dc in directions:
                cells = []
                for k in range(WIN_LEN):
                    nr, nc = r + dr*k, c + dc*k
                    if not board.in_bounds(nr, nc):
                        cells = []
                        break
                    cells.append(board.grid[nr][nc])
                if cells:
                    total += evaluate_line(cells, AI)
    mid = board.size // 2
    for r in range(board.size):
        for c in range(board.size):
            dist = abs(r - mid) + abs(c - mid)
            if board.grid[r][c] == AI:
                total += max(0, 8 - dist)
            elif board.grid[r][c] == HUMAN:
                total -= max(0, 8 - dist)
    return total

def quick_move_score(board, move, player):
    r, c = move
    board.make_move(r, c, player)
    score = evaluate_board(board)
    board.undo_move(r, c)
    return score
