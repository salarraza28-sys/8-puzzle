import heapq
from typing import List, Iterable
from Solver import Solver
from Board import Board

def run_test(puzzle):
    initial = Board(puzzle)
    solver = Solver(initial)

    print("Initial Board:")
    print(initial)
    print()

    if not solver.is_solvable():
        print("No solution possible")
    else:
        print(f"Minimum number of moves = {solver.moves()}")
        for board in solver.solution():
            print(board)
            print("---")
    print("=================================\n")


if __name__ == "__main__":
    
    # Test case 1: Solvable 3x3 puzzle
    puzzle1 = [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
    
    # Test case 2: Another solvable puzzle
    puzzle2 = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
    
    # Test case 3: Unsolvable puzzle
    puzzle3 = [[1, 2, 3], [4, 5, 6], [8, 7, 0]]

    run_test(puzzle1)
    run_test(puzzle2)
    run_test(puzzle3)
