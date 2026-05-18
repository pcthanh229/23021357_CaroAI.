EMPTY = 0
HUMAN = 1   # X
AI = 2      # O
WIN_LEN = 4

class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.last_move = None

    def clone(self):
        b = Board(self.size)
        b.grid = [row[:] for row in self.grid]
        b.last_move = self.last_move
        return b

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def is_empty(self, r, c):
        return self.in_bounds(r, c) and self.grid[r][c] == EMPTY

    def make_move(self, r, c, player):
        if not self.is_empty(r, c):
            return False
        self.grid[r][c] = player
        self.last_move = (r, c)
        return True

    def undo_move(self, r, c):
        self.grid[r][c] = EMPTY
        self.last_move = None

    def is_full(self):
        return all(self.grid[r][c] != EMPTY for r in range(self.size) for c in range(self.size))

    def has_any_piece(self):
        return any(self.grid[r][c] != EMPTY for r in range(self.size) for c in range(self.size))

    def print_board(self):
        print('   ' + ' '.join(str(i) for i in range(self.size)))
        for r in range(self.size):
            row = []
            for c in range(self.size):
                if self.grid[r][c] == HUMAN:
                    row.append('X')
                elif self.grid[r][c] == AI:
                    row.append('O')
                else:
                    row.append('.')
            print(f'{r:2d} ' + ' '.join(row))

    def check_winner(self, player):
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != player:
                    continue
                for dr, dc in directions:
                    count = 1
                    nr, nc = r + dr, c + dc
                    while self.in_bounds(nr, nc) and self.grid[nr][nc] == player:
                        count += 1
                        if count >= WIN_LEN:
                            return True
                        nr += dr
                        nc += dc
        return False

    def terminal_result(self):
        if self.check_winner(AI):
            return AI
        if self.check_winner(HUMAN):
            return HUMAN
        if self.is_full():
            return 0
        return None

    def get_valid_moves(self, radius=2):
        if not self.has_any_piece():
            mid = self.size // 2
            return [(mid, mid)]
        moves = set()
        pieces = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] != EMPTY]
        for r, c in pieces:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if self.in_bounds(nr, nc) and self.grid[nr][nc] == EMPTY:
                        moves.add((nr, nc))
        return list(moves)
