import heapq
from typing import List, Iterable
from Board import Board
class Solver:
    class Node:
        def __init__(self, board: Board, moves: int, previous: 'Solver.Node' = None):
            self.board = board
            self.moves = moves
            self.previous = previous
            # Manhattan priority optimization
            self.priority = moves + board.manhattan()

        def __lt__(self, other):
            return self.priority < other.priority

    def __init__(self, initial: Board):
        self._initial = initial
        self._solution_node = None
        self._solvable = False
        self._solve()

    def _solve(self):
        # A* loop with unsolvable detection using initial and twin boards
        pq_orig = [self.Node(self._initial, 0)]
        pq_twin = [self.Node(self._initial.twin(), 0)]
        
        while True:
            # Step for original board
            node = heapq.heappop(pq_orig)
            if node.board.is_goal():
                self._solvable, self._solution_node = True, node
                return
            for neighbor in node.board.neighbors():
                if node.previous is None or neighbor != node.previous.board:
                    heapq.heappush(pq_orig, self.Node(neighbor, node.moves + 1, node))
            
            # Step for twin board
            node_twin = heapq.heappop(pq_twin)
            if node_twin.board.is_goal():
                self._solvable = False
                return
            for neighbor in node_twin.board.neighbors():
                if node_twin.previous is None or neighbor != node_twin.previous.board:
                    heapq.heappush(pq_twin, self.Node(neighbor, node_twin.moves + 1, node_twin))

    def is_solvable(self) -> bool:
        return self._solvable

    def moves(self) -> int:
        return self._solution_node.moves if self._solvable else -1

    def solution(self) -> Iterable[Board]:
        if not self._solvable: return None
        path = []
        curr = self._solution_node
        while curr:
            path.append(curr.board)
            curr = curr.previous
        return reversed(path)