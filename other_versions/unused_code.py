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
				
				


    def sort_mask_elements(self):
        def masking(item):
            return bool(isinstance(item, (set, list)) and len(item) > 1)

        for i, row in enumerate(self.mask):
            for numbers in filter(masking, row):
                x_pos = row.index(numbers)
                self.mask[i][x_pos] = [x for y, x in sorted(zip(self.mc_cues, numbers))]



    def solve(self):
        self.iterations += 1

        pick = self.find_min_empty()
        if not pick:
            return True
        else:
            row, col = pick

        for i in self.mask[row][col]:
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False
        
        
        def solve(self):
        self.iterations += 1

        pick = self.find_min_empty()
        if not pick:
            return True
        else:
            row, col = pick

        for i in [x for _, x in sorted(zip(self.mc_cues, self.mask[row][col]))]:
            # ^ Only check for numbers in mask in the order of most common cues
            if self.valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False
        
        
        
        
        
        
    def update_mask(self):
        def masking(item):
            return bool(isinstance(item, (set, list)) and len(item) > 1)

        self.cues = self.set_cues()
        self.mc_cues = self.set_mc_cues()
        for i, row in enumerate(self.mask):
            for numbers in filter(masking, row):
                x_pos = row.index(numbers)
                to_mask = list()
                to_remove = set()
                #fillable = self.check_neighbors(numbers, (i, x_pos))
                #if fillable:
                #    self.mask[i][x_pos] = fillable
                #else:
                for number in numbers:
                    if not self.valid(number, (i, x_pos)):
                        to_remove.add(number)
                for num in to_remove:
                    self.mask[i][x_pos].remove(num)
                for num in self.mc_cues:
                    if num in self.mask[i][x_pos]:
                        to_mask.append(num)
                self.mask[i][x_pos] = to_mask
                
                
    def check_neighbors(self, valid_choices, pos):
        def masking(item):
            return bool(isinstance(item, set) and len(item) > 1)

        def to_set(item):
            if isinstance(item, int):
                return {item}
            else:
                return item

        # Check row
        def chk_row(pos):
            rows = list(map(to_set, self.mask[pos[0]]))
            print(f"R: {rows}")
            fillable = valid_choices.difference(*rows)
            if len(fillable) == 1:
                print(f"OK_Row: {fillable}")
                return fillable

        # Check column
        def chk_col(pos):
            columns = list(map(to_set, [item[pos[1]] for item in self.mask]))
            print(f"C: {columns}")
            fillable = valid_choices.difference(*columns)
            if len(fillable) == 1:
                print(f"OK_Column: {fillable}")
                return fillable

        # Check box
        def chk_box(pos):
            box_x = pos[1] // self.box_size
            box_y = pos[0] // self.box_size
            sets = []
            for i in range(box_y * self.box_size, box_y * self.box_size + self.box_size):
                sets += list(map(to_set, self.mask[i][box_x * self.box_size: box_x * self.box_size + self.box_size]))
            print(f"B: {sets}")
            fillable = valid_choices.difference(*sets)
            if len(fillable) == 1:
                print(f"OK_Box: {fillable}")
                return fillable

        row = chk_row(pos)
        if row:
            return row
        col = chk_col(pos)
        if col:
            return col
        box = chk_box(pos)
        if box:
            return box

        return False
        
        
logging.info(f'{strftime("%d %b %Y %H:%M:%S", localtime())}: '
             f'Iterations: {challenge.iterations}, Preprocessing passes: {preprocess_passes} '
             f'Cues: {challenge.cues} '
             f'Time Taken: {execution_time}, File: {FILENAME}, Interpreter: {INTERPRETER}')
             
