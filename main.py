from board import Board
from solver import Solver
import sys

def get_valid_puzzle_input():
    """
    Get and validate user input for the 8-puzzle.
    Handles edge cases: empty input, invalid characters, wrong count, duplicates, out of range.
    """
    while True:
        try:
            print("\n" + "="*60)
            print("8-PUZZLE SOLVER ")
            print("="*60)
            # print("\nEnter 9 numbers (0-8) with no spaces or commas.")
            # print("Example: 013425786")
            # print("Note: 0 represents the blank tile")
            # print("-"*60)
            
            user_input = input("\nEnter the numbers from 0-8: ").strip()
            
            # Edge Case 1: Empty input
            if not user_input:
                print("❌ ERROR: Input cannot be empty!")
                continue
            
            # Edge Case 2: Wrong length
            if len(user_input) != 9:
                print(f"❌ ERROR: Expected 9 digits, got {len(user_input)}!")
                continue
            
            # Edge Case 3: Non-numeric characters
            if not user_input.isdigit():
                print("❌ ERROR: Input contains non-numeric characters!")
                continue
            
            # Convert to list of integers
            digits = [int(char) for char in user_input]
            
            # Edge Case 4: Out of range values
            invalid_digits = [d for d in digits if d < 0 or d > 8]
            if invalid_digits:
                print(f"❌ ERROR: Digits must be 0-8. Found: {invalid_digits}")
                continue
            
            # Edge Case 5: Duplicate numbers
            if len(set(digits)) != 9:
                duplicates = [d for d in set(digits) if digits.count(d) > 1]
                print(f"❌ ERROR: Duplicate digits found: {duplicates}")
                print("   Each digit 0-8 must appear exactly once!")
                continue
            
            # Edge Case 6: Missing 0 (blank tile)
            if 0 not in digits:
                print("❌ ERROR: Missing blank tile (0)! All puzzles must have exactly one blank.")
                continue
            
            # Convert flat list to 3x3 board
            board_tiles = []
            for row_idx in range(3):
                row = []
                for col_idx in range(3):
                    row.append(digits[row_idx * 3 + col_idx])
                board_tiles.append(row)
            
            print("\n✓ Input validation passed!")
            return board_tiles
            
        except ValueError as e:
            print(f"❌ ERROR: Invalid input - {e}")
            continue
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            continue

def display_board(tiles, title=""):
    """Display the puzzle board in a formatted way."""
    if title:
        print(f"\n{title}")
    for row in tiles:
        print("  " + " ".join(str(tile) for tile in row))

def main():
    """Main program with edge case handling."""
    try:
        # Get validated input
        board_tiles = get_valid_puzzle_input()
        
        # Display input
        display_board(board_tiles, "Initial Board:")
        
        # print("\nCreating Board object...")
        initial = Board(board_tiles)
        
        # print("Running A* Solver...")
        print("-"*60)
        
        solver = Solver(initial)
        
        if not solver.is_solvable():
            print("\n❌ No solution possible!")
            print("This puzzle configuration cannot be solved.")
            print("   (This can be verified using the solvability algorithm)")
        else:
            solution = solver.solution()
            moves = solver.moves()
            
            print(f"\n✓ Solution found!")
            print(f"Minimum number of moves: {moves}")
            print("-"*60)
            
            count = 0
            for board in solution:
                print(f"\nMove {count}:")
                print(board)
                count += 1
            
            print("="*60)
            print(f"Total moves: {moves}")
            print("="*60)
            
    except ValueError as e:
        print(f"\n❌ Board Creation Error: {e}")
        print("Failed to create valid board. Please check your input.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
