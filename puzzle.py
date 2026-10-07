import random

TILE_SOURCE = {
    "w": (1, 0),   
    "s": (-1, 0),  
    "a": (0, 1),   
    "d": (0, -1),  
}
NEIGHBOURS = list(TILE_SOURCE.values())

class Puzzle:
    def __init__(self, size=4, board=None, rng=None):
        if size < 2:
            raise ValueError("size must be at least 2")
        self.size = size
        self.rng = rng or random.Random()
        if board is None:
            self.board, self.blank = self.make_board()
        else:
            self.board = [list(row) for row in board]
            self._validate()
            self.blank = self._find_blank()

    def goal(self):
            n = self.size
            return [list(range(r * n + 1, r * n + n + 1)) for r in range(n)][:-1] + \
                   [list(range((n - 1) * n + 1, n * n)) + [0]]

    def make_board(self):
        n = self.size
        steps = 10 * n ** 3
        while True:
            board = self.goal()
            br = bc = n - 1
            prev = None
            for _ in range(steps):
                options = [(br + dr, bc + dc) for dr, dc in NEIGHBOURS
                            if 0 <= br + dr < n and 0 <= bc + dc < n
                            and (br + dr, bc + dc) != prev]  
                nr, nc = self.rng.choice(options)
                board[br][bc], board[nr][nc] = board[nr][nc], 0
                prev, (br, bc) = (br, bc), (nr, nc)
                if board != self.goal():  
                    return board, (br, bc)
    def _validate(self):
            n = self.size
            flat = sorted(t for row in self.board for t in row)
            if len(self.board) != n or any(len(r) != n for r in self.board) \
                    or flat != list(range(n * n)):
                raise ValueError("board must be an n x n permutation of 0..n*n-1")
    
    def _find_blank(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c
        
    def blank_pos(self):
        return self.blank

    def move(self, key):
        if key not in TILE_SOURCE:
                    return None
        r, c = self.blank
        dr, dc = TILE_SOURCE[key]
        tr, tc = r + dr, c + dc
        if not (0 <= tr < self.size and 0 <= tc < self.size):
            return None
        tile = self.board[tr][tc]
        self.board[r][c], self.board[tr][tc] = tile, 0
        self.blank = (tr, tc)
        return tile

    def solved(self):
        return self.board == self.goal()