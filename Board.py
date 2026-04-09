import heapq
from typing import List, Iterable
class Board:
    def __init__(self, tiles: List[List[int]]):
        self._tiles = tuple(tuple(row) for row in tiles)
        self._n = len(tiles)

    def __str__(self) -> str:
        return f"{self._n}\n" + "\n".join(" ".join(f"{val:2}" for val in row) for row in self._tiles)

    def dimension(self) -> int:
        return self._n

    def hamming(self) -> int:
        count = 0
        for r in range(self._n):
            for c in range(self._n):
                val = self._tiles[r][c]
                if val != 0 and val != r * self._n + c + 1:
                    count += 1
        return count

    def manhattan(self) -> int:
        # Manhattan calculation: sum of vertical and horizontal distances to goal positions
        dist = 0
        for r in range(self._n):
            for c in range(self._n):
                val = self._tiles[r][c]
                if val != 0:
                    target_r = (val - 1) // self._n
                    target_c = (val - 1) % self._n
                    dist += abs(r - target_r) + abs(c - target_c)
        return dist

    def is_goal(self) -> bool:
        for r in range(self._n):
            for c in range(self._n):
                val = self._tiles[r][c]
                expected = r * self._n + c + 1
                if val == 0:
                    if r != self._n - 1 or c != self._n - 1: return False
                elif val != expected:
                    return False
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board): return False
        return self._tiles == other._tiles

    def __hash__(self) -> int:
        return hash(self._tiles)

    def neighbors(self) -> Iterable['Board']:
        # Neighbors logic: find 0 and generate all valid boards by sliding
        r0, c0 = next((r, c) for r in range(self._n) for c in range(self._n) if self._tiles[r][c] == 0)
        results = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r0 + dr, c0 + dc
            if 0 <= nr < self._n and 0 <= nc < self._n:
                tiles_copy = [list(row) for row in self._tiles]
                tiles_copy[r0][c0], tiles_copy[nr][nc] = tiles_copy[nr][nc], tiles_copy[r0][c0]
                results.append(Board(tiles_copy))
        return results

    def twin(self) -> 'Board':
        tiles_copy = [list(row) for row in self._tiles]
        if tiles_copy[0][0] != 0 and tiles_copy[0][1] != 0:
            tiles_copy[0][0], tiles_copy[0][1] = tiles_copy[0][1], tiles_copy[0][0]
        else:
            tiles_copy[1][0], tiles_copy[1][1] = tiles_copy[1][1], tiles_copy[1][0]
        return Board(tiles_copy)
