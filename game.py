import time
from puzzle import Puzzle

SIZES = (3, 4, 5)
DIRECTION_NAMES = {"w": "up", "s": "down", "a": "left", "d": "right"}
HELP = ("W/A/S/D slides a tile up/left/down/right into the blank. "
        "3/4/5 = new game of that size, N = new game (same size), Q = quit.")

class SlidingPuzzle:
    def __init__(self, size=4, clock=time.monotonic, rng=None):
            self.clock = clock
            self.rng = rng
            self.session = {"solved": 0, "best": {}} 
            self.new_game(size)


    def new_game(self, size):
            if size not in SIZES:
                raise ValueError(f"size must be one of {SIZES}")
            self.size = size
            self.puzzle = Puzzle(size, rng=self.rng)
            self.moves = 0
            self.started = self.clock()
            self.finished_at = None

    @property
    def finished(self):
        return self.finished_at is not None
    
    def elapsed(self):
        end = self.finished_at if self.finished else self.clock()
        return end - self.started
    
    def _record_solve(self):
        self.finished_at = self.clock()
        self.session["solved"] += 1
        best = self.session["best"].setdefault(
            self.size, {"moves": self.moves, "time": self.elapsed()})
        best["moves"] = min(best["moves"], self.moves)
        best["time"] = min(best["time"], self.elapsed())

    def apply_move(self, key):
            if self.finished:
                return False, "Puzzle already solved. N = new game, 3/4/5 = change size, Q = quit."
            tile = self.puzzle.move(key)
            if tile is None:
                return False, "That move is not possible."
            self.moves += 1
            if self.puzzle.solved():
                self._record_solve()
                return True, f"Slid tile {tile} {DIRECTION_NAMES[key]}. Solved!"
            return True, f"Slid tile {tile} {DIRECTION_NAMES[key]}."
    def handle_command(self, cmd):

            cmd = cmd.strip().lower()
            if cmd == "q":
                return "Bye.", False
            if cmd == "n":
                self.new_game(self.size)
                return f"New {self.size}x{self.size} game.", True
            if cmd in {str(s) for s in SIZES}:
                self.new_game(int(cmd))
                return f"New {self.size}x{self.size} game.", True
            if cmd in DIRECTION_NAMES:
                return self.apply_move(cmd)[1], True
            return f"Unknown command {cmd!r}. {HELP}", True

    
    def display(self):
        width = len(str(self.size * self.size - 1))
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or '.':>{width}}" for x in row))
        status = "SOLVED" if self.finished else "playing"
        line = (f"{self.size}x{self.size} [{status}]  Moves: {self.moves}  " f"Time: {int(self.elapsed())}s  Solved this session: {self.session['solved']}")
        best = self.session["best"].get(self.size)
        if best:
            line += f"  Best: {best['moves']} moves / {int(best['time'])}s"
        print(line)

    def run(self):
        print("Sliding Puzzle —", HELP)
        while True:
            self.display()
            try:
                cmd = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                return
            message, keep_running = self.handle_command(cmd)
            print(message)
            if not keep_running:
                return
