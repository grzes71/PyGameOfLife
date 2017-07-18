import pygame
from pygame.locals import *

CLOCK_TICK = 50
TIME_WAIT = 500
SIZE = (30, 25)

BOARD = {
    1: {1, 2, 3},
    4: {10},
    5: {3, 4, 5, 8, 10},
    6: {4, 5, 6, 9, 10},
    18: {6, 11},
    19: {4, 5, 7, 8, 9, 10, 12, 13},
    20: {6, 11},
}


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
                print("Cell: %d,%d neighbours: %s exists: %s" % (row_idx, col_idx, no_neighbours, is_onboard))
            if is_onboard:  # life cell
                if 2 <= no_neighbours <= 3:
                    add_to_board()
            else:  # not life cell
                if no_neighbours == 3:
                    add_to_board()
        self.board = board2


class Game(object):
    """Game class responsible for drawing the game board.
    """
    PATT_COLOR = (255, 100, 0)
    BACK_COLOR = (0, 0, 0)

    def __init__(self):
        vi = pygame.display.Info()
        width, height = vi.current_w, vi.current_h
        self.video_size = (width, height)
        self.screen = pygame.display.set_mode(self.video_size, FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.patterns_horizontal, self.patterns_vertical = SIZE
        self.pattern_width = width / self.patterns_horizontal
        self.pattern_height = height / self.patterns_vertical
        self.game_board = GameBoard(BOARD)

    def get_cell(self, y, x):
        return self.game_board.is_onboard(y, x)

    def draw(self):
        pw, ph = self.pattern_width, self.pattern_height
        screen = self.screen
        for x in range(0, self.patterns_horizontal):
            for y in range(0, self.patterns_vertical):
                color = Game.PATT_COLOR if self.get_cell(y, x) else Game.BACK_COLOR
                pygame.draw.rect(screen, color, pygame.Rect(x * pw, y * ph, pw - 1, ph - 1))

    def logic(self):
        self.game_board.process()

    def in_progress(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        pygame.display.update()
        self.clock.tick(CLOCK_TICK)
        pygame.time.wait(TIME_WAIT)

    def loop(self):
        """"Main game loop.
        """
        pygame.event.pump()
        in_progress = True

        while in_progress:
            self.logic()
            self.draw()
            self.update()
            in_progress = self.in_progress()


def main():
    pygame.init()
    Game().loop()
    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    main()

