import random
import unittest
from game import SlidingPuzzle
from puzzle import Puzzle
from solvability_check import is_solvable


class FakeClock:
    def __init__(self):
        self.t = 100.0
    def __call__(self):
        return self.t
    def tick(self, s):
        self.t += s


def near_solved_3x3():
    return Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 0, 8]])


class PuzzleTests(unittest.TestCase):
    def test_fresh_boards_always_solvable_unsolved_valid(self):
        for size in (3, 4, 5):
            for _ in range(500):
                p = Puzzle(size)
                self.assertEqual(sorted(sum(p.board, [])), list(range(size * size)))
                self.assertTrue(is_solvable(p.board))
                self.assertFalse(p.solved())

    def test_parity_checker_rejects_known_unsolvable(self):
        self.assertFalse(is_solvable([[2, 1, 3], [4, 5, 6], [7, 8, 0]]))  # swapped pair

    def test_cached_blank_matches_board(self):
        p = Puzzle(4)
        for key in "wasd" * 50:
            p.move(key)
            r, c = p.blank
            self.assertEqual(p.board[r][c], 0)

    def test_edge_moves_rejected_and_board_unchanged(self):
        p = Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])  # blank bottom-right
        for key in ("w", "a"):  # no tile below / right of blank
            self.assertIsNone(p.move(key))
        self.assertTrue(p.solved())

    def test_move_returns_tile_and_swaps(self):
        p = near_solved_3x3()
        self.assertEqual(p.move("a"), 8)
        self.assertTrue(p.solved())

    def test_bad_board_rejected(self):
        with self.assertRaises(ValueError):
            Puzzle(3, board=[[1, 1, 3], [4, 5, 6], [7, 8, 0]])


class GameTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.g = SlidingPuzzle(3, clock=self.clock)

    def test_all_sizes(self):
        for s in (3, 4, 5):
            self.g.new_game(s)
            self.assertEqual(len(self.g.puzzle.board), s)
        with self.assertRaises(ValueError):
            self.g.new_game(6)

    def test_invalid_move_no_count_no_success_message(self):
        self.g.puzzle = Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        for key in ("w", "a"):
            ok, msg = self.g.apply_move(key)
            self.assertFalse(ok)
            self.assertNotIn("Slid", msg)
        self.assertEqual(self.g.moves, 0)

    def test_valid_move_counts_once(self):
        self.g.puzzle = Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        ok, msg = self.g.apply_move("s")
        self.assertTrue(ok)
        self.assertIn("Slid tile 6 down", msg)
        self.assertEqual(self.g.moves, 1)

    def test_solve_small_board_by_reversing_moves(self):
        self.g.puzzle = Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        for key in "sd":                       # scramble: 2 legal moves
            self.assertTrue(self.g.apply_move(key)[0])
        self.assertFalse(self.g.finished)
        for key in "aw":                       # undo them in reverse order
            self.assertTrue(self.g.apply_move(key)[0])
        self.assertTrue(self.g.finished)
        self.assertEqual(self.g.moves, 4)
        self.assertEqual(self.g.session["solved"], 1)

    def test_commands_ignored_after_completion_and_timer_frozen(self):
        self.g.puzzle = near_solved_3x3()
        self.clock.tick(7)
        ok, msg = self.g.apply_move("a")
        self.assertTrue(ok)
        self.assertIn("Solved", msg)
        board_after = [r[:] for r in self.g.puzzle.board]
        self.clock.tick(50)
        for key in "wasd":
            ok, msg = self.g.apply_move(key)
            self.assertFalse(ok)
            self.assertIn("already solved", msg)
        self.assertEqual(self.g.moves, 1)
        self.assertEqual(self.g.puzzle.board, board_after)
        self.assertEqual(self.g.elapsed(), 7)

    def test_timer_runs_while_playing(self):
        self.clock.tick(12)
        self.assertEqual(self.g.elapsed(), 12)

    def test_new_game_resets_game_values_keeps_session(self):
        self.g.puzzle = near_solved_3x3()
        self.g.apply_move("a")
        self.clock.tick(5)
        self.g.handle_command("4")
        self.assertEqual((self.g.size, self.g.moves, self.g.elapsed()), (4, 0, 0))
        self.assertFalse(self.g.finished)
        self.assertEqual(self.g.session["solved"], 1)
        self.assertEqual(self.g.session["best"][3]["moves"], 1)

    def test_invalid_commands_change_nothing(self):
        before = ([r[:] for r in self.g.puzzle.board], self.g.moves, self.g.size)
        for cmd in ("", "  ", "wa", "wasd", "x", "9", "12", "quit", "6"):
            msg, keep = self.g.handle_command(cmd)
            self.assertTrue(keep)
            self.assertIn("Unknown command", msg)
        self.assertEqual(before, ([r[:] for r in self.g.puzzle.board], self.g.moves, self.g.size))

    def test_quit(self):
        self.assertEqual(self.g.handle_command("Q"), ("Bye.", False))

    def test_move_keys_case_and_whitespace_insensitive(self):
        self.g.puzzle = Puzzle(3, board=[[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.assertIn("Slid", self.g.handle_command(" S ")[0])


if __name__ == "__main__":
    unittest.main()