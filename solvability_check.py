

import sys
from puzzle import Puzzle


def is_solvable(board):
    n = len(board)
    flat = [t for row in board for t in row if t != 0]
    inversions = sum(1 for i in range(len(flat)) for j in range(i + 1, len(flat))
                     if flat[i] > flat[j])
    if n % 2 == 1:
        return inversions % 2 == 0
    blank_row_from_bottom = n - next(r for r, row in enumerate(board) if 0 in row)
    return (inversions + blank_row_from_bottom) % 2 == 1


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    for size in (3, 4, 5):
        bad = sum(not is_solvable(Puzzle(size).board) for _ in range(count))
        print(f"{size}x{size}: {bad}/{count} unsolvable ({100 * bad / count:.1f}%)")