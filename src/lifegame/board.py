"""GameBoard module.
"""

class GameBoard:
    """GameBoard class implements game logic.
    """
    SURROUNDING = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x or y]
    TOTAL = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]

    def __init__(self, board=None):
        self.board = board or {}

    def get_all_cells(self):
        all_cells = set()
        for row_idx in self.board:
            for col_idx in self.board[row_idx]:
                all_cells.add((row_idx, col_idx))
                for y, x in GameBoard.TOTAL:
                    all_cells.add((row_idx+y, col_idx+x))
        return all_cells

    def is_onboard(self, curr_y, curr_x):
        return None if curr_y not in self.board else curr_x in self.board[curr_y]

    def get_no_neighbours(self, all_cells, row_idx, col_idx):
        no_neighbours = 0
        for y, x in GameBoard.SURROUNDING:
            curr_y, curr_x = row_idx + y, col_idx + x
            if (curr_y, curr_x) in all_cells:
                if self.is_onboard(curr_y, curr_x):
                    no_neighbours += 1

        return no_neighbours

    def process(self):
        def add_to_board():
            if row_idx not in board2:
                board2[row_idx] = set()
            board2[row_idx].add(col_idx)

        all_cells = self.get_all_cells()
        board2 = {}
        for cell in all_cells:
            row_idx, col_idx = cell
            no_neighbours = self.get_no_neighbours(all_cells, row_idx, col_idx)
            is_onboard = self.is_onboard(row_idx, col_idx)
            if __debug__:
                print("Cell: %d,%d neighbours: %s exists: %s" % (row_idx, 
                                                                 col_idx, 
                                                                 no_neighbours, is_onboard))
            if is_onboard:  # life cell
                if 2 <= no_neighbours <= 3:
                    add_to_board()
            else:  # not life cell
                if no_neighbours == 3:
                    add_to_board()
        self.board = board2

