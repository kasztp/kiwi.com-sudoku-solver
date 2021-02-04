    def solve(self):
        self.iterations += 1

        if not self.find_min_empty():
            return True
        else:
            row, col = self.find_min_empty()
        temp_mask = []
        if row == 99 and col == 99:
            temp_mask = deepcopy(self.mask)
            self.update_mask()
            row, col = self.find_min_empty()
            if row == 99 and col == 99:
                row, col = self.find_empty()

        if len(self.mask[row][col]) > 0:
            for i in self.mask[row][col].copy():
                if self.valid(i, (row, col)):
                    self.board[row][col] = i

                    if self.solve():
                        return True

                    self.board[row][col] = 0
        if temp_mask:
            self.mask = temp_mask
        return False
		
		
		
		
	def find_min_empty(self):
        def is_set(item):
            return bool(isinstance(item, set))

        min_len_set = [0, {1, 2, 3, 4, 5, 6, 7, 8, 9}]
        for i, row in enumerate(self.mask):
            if len(list(filter(is_set, row))) >= 1:
                smallest_set_in_row = min(filter(is_set, row), key=len)
                if len(min_len_set[1]) > len(smallest_set_in_row) and self.board[i][row.index(smallest_set_in_row)] == 0:
                    min_len_set[0] = i
                    min_len_set[1] = smallest_set_in_row

        if min_len_set != [0, {1, 2, 3, 4, 5, 6, 7, 8, 9}]:
            return min_len_set[0], self.mask[min_len_set[0]].index(min_len_set[1])  # row, col
        elif not self.find_empty():
            return None
        else:
            return 99, 99
			
			
			
			



    def is_solved(self):
        while self.find_empty():
            if not self.find_empty():
                return True
            else:
                row, col = self.find_min_empty()

            fillable = self.check_neighbors(self.mask[row][col], (row, col))
            if fillable:
                self.board[row][col] = int(fillable)
                self.mask[row][col] = fillable
            else:
                return row, col
				
				
