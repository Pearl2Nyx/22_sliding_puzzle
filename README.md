# Scenario 22 — Sliding Puzzle

A terminal sliding puzzle with configurable board size and legal blank-space moves.

## Provided files

- `main.py` — entry point.
- `game.py` — interaction, timer, and move tracking.
- `puzzle.py` — puzzle representation and movement rules.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

## Before changing the code

Start several puzzles and inspect the initial boards. Think about whether arbitrary
permutations can always be reached from the solved state using legal moves.

## Task 1 — Guarantee solvable starting states

Change puzzle initialisation so every generated board is reachable from the solved
arrangement. Prefer generating the solved board and applying legal blank moves to
scramble it.

**Done when:** repeated fresh puzzles are solvable in principle and the puzzle never
starts in an unreachable parity state.

## Task 2 — Complete puzzle lifecycle

Detect the solved arrangement and end the game cleanly. Prevent commands from changing
state after completion.

## Task 3 — Size, timer, and move modes

Add 3x3, 4x4, and 5x5 modes. Track moves and elapsed time consistently across all sizes.
Do not reset session values accidentally when only the board is recreated.

## Task 4 — Valid-action feedback

Only report a successful slide when a tile actually moved into the blank. Invalid moves
must not increment the move count or generate success feedback.

## Required testing

Generate many fresh boards, test all sizes, solve a small board, attempt impossible
moves, verify move counts, verify timer behaviour, test invalid commands, and quit.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [ ] Task 1 completed and the original defect was reproduced and fixed.
- [ ] Tasks 2–4 completed and tested.
- [ ] Boundary and invalid-input cases tested.
- [ ] No unnecessary external dependencies added.
- [ ] No persistent storage added.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-10-sliding-puzzle/
├── README.md
├── requirements.txt
├── main.py
├── game.py
└── puzzle.py
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history


## Implementation Notes

### Task 1 — Solvable Starting States

The original implementation generated the puzzle by randomly shuffling all tiles. 
This could produce unreachable board configurations due to the parity constraints 
of sliding puzzles.

The puzzle was changed to:

1. Create the solved board.
2. Locate the blank space.
3. Select a legal blank-space move.
4. Apply the move.
5. Repeat the process to scramble the board.

This guarantees that every generated starting state is reachable from the solved state.

### Task 2 — Puzzle Lifecycle

The puzzle now detects when the board reaches the solved arrangement.

Once the puzzle is solved:

- The final move count and elapsed time are displayed.
- The game ends cleanly.
- Further commands cannot modify the completed puzzle.

### Task 3 — Board Sizes, Timer, and Moves

The puzzle supports:

- 3 × 3
- 4 × 4
- 5 × 5

Move count and elapsed time are tracked by the game session and are not reset 
when the puzzle board is recreated unnecessarily.

### Task 4 — Valid-Action Feedback

A move is counted only when a tile actually moves into the blank space.

Invalid moves:

- Do not modify the board.
- Do not increment the move counter.
- Do not produce successful-move feedback.

## Testing

The implementation was tested for:

- 3 × 3, 4 × 4, and 5 × 5 boards.
- Multiple freshly generated puzzles.
- Reachability/solvability of generated boards.
- Solved-state detection.
- Valid blank-space moves.
- Impossible moves at board boundaries.
- Invalid commands.
- Correct move counting.
- Timer behaviour.
- Completion behaviour.
- Quit command.
- Prevention of moves after puzzle completion.

## BEFORE AND AFTER VIDEOS
 
 - BEFORE THE CHANGES
   https://github.com/user-attachments/assets/687fd113-9bd5-4e13-be2d-def4f1154a66

 - AFTER THE CHANGES
   https://github.com/user-attachments/assets/e60a9986-49c5-4d75-8261-2a10328aa271