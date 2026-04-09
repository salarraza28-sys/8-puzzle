import heapq
from typing import List, Iterable
from Solver import Solver
from Board import Board


if __name__ == "__main__":
    # Test case: Solvable 3x3 puzzle
    puzzle = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
    initial = Board(puzzle)
    solver = Solver(initial)

    if not solver.is_solvable():
        print("No solution possible")
    else:
        print(f"Minimum number of moves = {solver.moves()}")
        for board in solver.solution():
            print(board)
            print("---")
