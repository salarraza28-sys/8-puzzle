class Board:
    def __init__(self, tiles):
        """
        Initialize a Board with edge case validation.
        
        Edge Cases Handled:
        - Null/None input
        - Non-rectangular dimensions
        - Invalid tile values
        - Missing or duplicate tiles
        - Negative dimensions
        """
        # Edge Case 1: Null input
        if tiles is None:
            raise ValueError("Tiles cannot be None")
        
        # Edge Case 2: Empty tiles
        if len(tiles) == 0:
            raise ValueError("Tiles cannot be empty")
        
        # Edge Case 3: Get dimension and validate
        self._n = len(tiles)
        
        # Edge Case 4: Negative or zero dimension
        if self._n <= 0:
            raise ValueError(f"Dimension must be positive, got {self._n}")
        
        # Edge Case 5: Non-rectangular (jagged array)
        for i, row in enumerate(tiles):
            if row is None:
                raise ValueError(f"Row {i} is None")
            if len(row) != self._n:
                raise ValueError(f"Row {i} has {len(row)} elements, expected {self._n}")
        
        # Copy tiles and collect all values for validation
        self._tiles = []
        all_values = []
        
        for i in range(self._n):
            row = []
            for j in range(self._n):
                val = tiles[i][j]
                
                # Edge Case 6: Non-integer values
                if not isinstance(val, int):
                    raise ValueError(f"Tile at ({i},{j}) is not an integer: {val}")
                
                # Edge Case 7: Negative values
                if val < 0:
                    raise ValueError(f"Negative tile value {val} at ({i},{j})")
                
                # Edge Case 8: Value out of range (must be 0 to n²-1)
                if val >= self._n * self._n:
                    raise ValueError(f"Tile value {val} at ({i},{j}) exceeds maximum {self._n * self._n - 1}")
                
                row.append(val)
                all_values.append(val)
            
            self._tiles.append(row)
        
        # Edge Case 9: Duplicate values
        if len(set(all_values)) != len(all_values):
            duplicates = [v for v in set(all_values) if all_values.count(v) > 1]
            raise ValueError(f"Duplicate tile values found: {duplicates}")
        
        # Edge Case 10: Missing values (not a permutation of 0 to n²-1)
        expected_values = set(range(self._n * self._n))
        actual_values = set(all_values)
        if actual_values != expected_values:
            missing = expected_values - actual_values
            extra = actual_values - expected_values
            msg = ""
            if missing:
                msg += f"Missing values: {missing}. "
            if extra:
                msg += f"Extra values: {extra}."
            raise ValueError(f"Invalid permutation. {msg}")
        
        # Cache heuristic distances during construction
        self._manhattan = 0
        self._hamming = 0
        
        for i in range(self._n):
            for j in range(self._n):
                val = self._tiles[i][j]
                if val != 0:
                    # Calculate correct goal position
                    goal_row = (val - 1) // self._n
                    goal_col = (val - 1) % self._n
                    
                    # Manhattan distance is the sum of horizontal and vertical offsets
                    self._manhattan += abs(i - goal_row) + abs(j - goal_col)
                    
                    # Hamming checks if it's strictly in the wrong place
                    if val != (i * self._n + j + 1):
                        self._hamming += 1


    def __str__(self):
        res = str(self._n) + "\n"
        for i in range(self._n):
            for j in range(self._n):
                res += str(self._tiles[i][j]) + " "
            res += "\n"
        return res

    def dimension(self):
        return self._n

    def hamming(self):
        return self._hamming

    def manhattan(self):
        return self._manhattan

    def is_goal(self):
        # We are at the goal if the Hamming distance is 0
        return self._hamming == 0

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Board):
            return False
        if self._n != other.dimension():
            return False
        
        # Check every tile manually (no zip or enumerate allowed)
        for i in range(self._n):
            for j in range(self._n):
                if self._tiles[i][j] != other._tiles[i][j]:
                    return False
        return True

    def _copy_tiles(self):
        # Helper method to generate a deepcopy for immutability during neighbor creation
        new_tiles = []
        for i in range(self._n):
            row = []
            for j in range(self._n):
                row.append(self._tiles[i][j])
            new_tiles.append(row)
        return new_tiles

    def neighbors(self):
        # Find the blank square (0)
        blank_r = -1
        blank_c = -1
        for i in range(self._n):
            for j in range(self._n):
                if self._tiles[i][j] == 0:
                    blank_r = i
                    blank_c = j
                    
        neighbors_list = []
        
        # Move up
        if blank_r > 0:
            copy1 = self._copy_tiles()
            # Swap
            copy1[blank_r][blank_c], copy1[blank_r - 1][blank_c] = copy1[blank_r - 1][blank_c], copy1[blank_r][blank_c]
            neighbors_list.append(Board(copy1))
            
        # Move down
        if blank_r < (self._n - 1):
            copy2 = self._copy_tiles()
            copy2[blank_r][blank_c], copy2[blank_r + 1][blank_c] = copy2[blank_r + 1][blank_c], copy2[blank_r][blank_c]
            neighbors_list.append(Board(copy2))
            
        # Move left
        if blank_c > 0:
            copy3 = self._copy_tiles()
            copy3[blank_r][blank_c], copy3[blank_r][blank_c - 1] = copy3[blank_r][blank_c - 1], copy3[blank_r][blank_c]
            neighbors_list.append(Board(copy3))
            
        # Move right
        if blank_c < (self._n - 1):
            copy4 = self._copy_tiles()
            copy4[blank_r][blank_c], copy4[blank_r][blank_c + 1] = copy4[blank_r][blank_c + 1], copy4[blank_r][blank_c]
            neighbors_list.append(Board(copy4))
            
        return neighbors_list

    def twin(self):
        # The twin board allows us to detect unsolvable puzzles. 
        # We simply swap the first two adjacent, non-blank tiles we find.
        copy_tiles = self._copy_tiles()
        
        # Try horizontal swap
        for i in range(self._n):
            for j in range(self._n - 1):
                if copy_tiles[i][j] != 0 and copy_tiles[i][j+1] != 0:
                    copy_tiles[i][j], copy_tiles[i][j+1] = copy_tiles[i][j+1], copy_tiles[i][j]
                    return Board(copy_tiles)
                    
        # Try vertical swap if horizontal wasn't possible
        for i in range(self._n - 1):
            for j in range(self._n):
                if copy_tiles[i][j] != 0 and copy_tiles[i+1][j] != 0:
                    copy_tiles[i][j], copy_tiles[i+1][j] = copy_tiles[i+1][j], copy_tiles[i][j]
                    return Board(copy_tiles)
                    
        return Board(copy_tiles)
