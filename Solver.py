"""
VIVA VOCE PREPARATION GUIDE (CONT.)
===================================
1. VIVA PHASE 2: Code Walkthrough
   - Student A must explain the SearchNode comparison: "We implemented __lt__ because heapq requires it for objects pushed into the Min-Heap. The priority is defined as (Manhattan Distance + moves). Ties are broken by prioritizing nodes with a strictly smaller Manhattan distance, which pushes nodes closer to the goal."
   - Student B must explain the while loop: "We use the exact step-by-step logic from A*. In each iteration, we pop the SearchNode with the lowest priority from both the main puzzle queue and the twin puzzle queue. If the main queue hits the goal, it is solvable. If the twin queue hits the goal, the original puzzle was fundamentally unsolvable."
   - Avoiding redundant nodes optimization: "When enqueuing neighbors, we compare the neighbor against current.prev_node.board. This simple check prevents the algorithm from uselessly bouncing back and forth between two states."

Remember: DO NOT just copy-paste this blindly. Follow the GitHub Workflow. Branch out, Commit with tags, PR, merge.
"""

import heapq
from board import Board

class SearchNode:
    # Encapsulating the search tree logic
    def __init__(self, board, moves, prev_node):
        self.board = board
        self.moves = moves
        self.prev_node = prev_node
        # Cash the priority
        self.priority = board.manhattan() + moves

    def __lt__(self, other):
        # Tie-breaking logic: if two nodes have the same priority (moves + manhattan)
        # prefer the one that is closer to the goal (lower manhattan distance)
        # Explain this exactly in your Viva!
        if self.priority == other.priority:
            return self.board.manhattan() < other.board.manhattan()
        return self.priority < other.priority


class Solver:
    def __init__(self, initial):
        """
        Initialize Solver with edge case handling.
        
        Edge Cases Handled:
        - Null/None initial board
        - Unsolvable puzzles (detected via twin algorithm)
        """
        # Edge Case 1: Null/None initial board
        if initial is None:
            raise ValueError("Initial board cannot be None")
        
        # Edge Case 2: Validate board dimension (should be square)
        if initial.dimension() <= 0:
            raise ValueError(f"Invalid board dimension: {initial.dimension()}")
            
        self._is_solvable = False
        self._solution_boards = []
        
        # Priority Queues (Min-Heaps) for simultaneous A* search
        pq_main = []
        pq_twin = []
        
        # Push start nodes. Moves = 0.
        heapq.heappush(pq_main, SearchNode(initial, 0, None))
        heapq.heappush(pq_twin, SearchNode(initial.twin(), 0, None))
        
        # Edge Case 3: Ensure priority queues are not empty
        if len(pq_main) == 0 or len(pq_twin) == 0:
            raise ValueError("Failed to initialize search queues")
        
        # Run A* Search side by side
        while len(pq_main) > 0 and len(pq_twin) > 0:
            
            # 1: Pop the node with the minimum priority
            current_main = heapq.heappop(pq_main)
            
            # Check if this node is the goal
            if current_main.board.is_goal():
                self._is_solvable = True
                self._build_solution(current_main)
                break
                
            current_twin = heapq.heappop(pq_twin)
            # If twin reaches the goal, the initial is mathematically unsolvable
            if current_twin.board.is_goal():
                self._is_solvable = False
                break
                
            # 2: Insert neighboring boards back into priority queue (Main)
            for neighbor in current_main.board.neighbors():
                # Critical Optimization: Do not enqueue a neighbor if its board 
                # is the same as the board of the previous search node.
                if current_main.prev_node is None or not (neighbor == current_main.prev_node.board):
                    next_node = SearchNode(neighbor, current_main.moves + 1, current_main)
                    heapq.heappush(pq_main, next_node)
                    
            # 2: Insert neighboring boards back into priority queue (Twin)
            for neighbor in current_twin.board.neighbors():
                if current_twin.prev_node is None or not (neighbor == current_twin.prev_node.board):
                    next_node = SearchNode(neighbor, current_twin.moves + 1, current_twin)
                    heapq.heappush(pq_twin, next_node)

    def _build_solution(self, goal_node):
        # Follow the prev_node pointers back to the start
        current = goal_node
        path = []
        while current is not None:
            path.append(current.board)
            current = current.prev_node
            
        # Reverse the array since we traversed backwards
        for i in range(len(path) - 1, -1, -1):
            self._solution_boards.append(path[i])

    def is_solvable(self):
        return self._is_solvable

    def moves(self):
        if not self._is_solvable:
            return -1
        # Number of moves is the count of boards in the solution sequence minus the initial board
        return len(self._solution_boards) - 1

    def solution(self):
        if not self._is_solvable:
            return None
        return self._solution_boards
