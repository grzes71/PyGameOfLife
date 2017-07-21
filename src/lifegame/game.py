"""Game of Life main module.
"""

import argparse
import pygame

from lifegame.board import GameBoard

BOARD = {
    0: {4, 5},
    1: {3, 4},
    2: {4},
    6: {10},
    7: {8, 10},
    8: {9, 10},
    20: {6, 11},
    21: {4, 5, 7, 8, 9, 10, 12, 13},
    22: {6, 11},
}

def parse_args():
    parser = argparse.ArgumentParser(description='Game of Life')
    parser.add_argument('--width', default=600, type=int, help='game display width')
    parser.add_argument('--height', default=400, type=int, help='game display height')
    parser.add_argument('--fullscreen', action='store_true', help='switch fullscreen on')
    parser.add_argument('--wait', default=500, type=int, help='wait time between iterations')
    parser.add_argument('--clock', default=50, type=int, help='clock tick')
    parser.add_argument('--horizontal', default=20, type=int, help='number of horizontal cells')
    parser.add_argument('--vertical', default=25, type=int, help='number of vertical cells')
    return parser.parse_args()


class Game(object):
    """Game class responsible for drawing the game board.
    """
    PATT_COLOR = (255, 100, 0)
    BACK_COLOR = (0, 0, 0)

    def __init__(self, options, screen, game_board):
        self.screen = screen
        self.game_board = game_board
        self.offset_x = self.offset_y = 0

        self._width, self._height = options.width, options.height
        self._horizontal, self._vertical = options.horizontal, options.vertical

        self.clock_tick = options.clock
        self.wait_time = options.wait

        self.clock = pygame.time.Clock()
        self._calculate_pattern_size()

    def _calculate_pattern_size(self):
        self._pattern_width = self.width / self.patterns_horizontal
        self._pattern_height = self.height / self.patterns_vertical

    @property
    def pattern_width(self):
        return self._pattern_width

    @property
    def pattern_height(self):
        return self._pattern_height

    @property
    def patterns_horizontal(self):
        return self._horizontal

    @property
    def patterns_vertical(self):
        return self._vertical

    @patterns_horizontal.setter
    def patterns_horizontal(self, value):
        self._horizontal = value
        self._calculate_pattern_size()

    @patterns_vertical.setter
    def patterns_vertical(self, value):
        self._vertical = value
        self._calculate_pattern_size()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw(self):
        pw, ph = self.pattern_width, self.pattern_height
        screen = self.screen
        screen.fill(Game.BACK_COLOR)
        for x in range(0, self.patterns_horizontal):
            for y in range(0, self.patterns_vertical):
                is_onboard = self.game_board.is_onboard(y+self.offset_y, x+self.offset_x)
                if is_onboard:
                    pygame.draw.rect(screen, Game.PATT_COLOR, pygame.Rect(x * pw, y * ph, pw - 1, ph - 1))

    def logic(self):
        self.game_board.process()

    def in_progress(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    self.offset_x -= 1
                    print("x=", self.offset_x)
                elif event.key == pygame.K_RIGHT:
                    self.offset_x += 1
                    print("x=", self.offset_x)
                elif event.key == pygame.K_UP:
                    self.offset_y -= 1
                    print("y=", self.offset_y)
                elif event.key == pygame.K_DOWN:
                    self.offset_y += 1
                    print("y=", self.offset_y)
                elif event.key == pygame.K_KP_PLUS:
                    self.patterns_vertical += 1
                    self.patterns_horizontal += 1
                    print("plus")
                elif event.key == pygame.K_KP_MINUS:
                    self.patterns_vertical -= 1
                    self.patterns_horizontal -= 1
                    print("minus")
            elif event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        pygame.display.update()
        self.clock.tick(self.clock_tick)
        pygame.time.wait(self.wait_time)

    def loop(self):
        """"Main game loop.
        """
        in_progress = True

        while in_progress:
            self.logic()
            self.draw()
            self.update()
            in_progress = self.in_progress()


def main():
    options = parse_args()
    video_size = (options.width, options.height)
    if options.fullscreen:
        screen = pygame.display.set_mode(video_size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(video_size)
    pygame.init()
    game_board = GameBoard(BOARD)
    game = Game(options, screen, game_board)
    game.loop()
    pygame.display.quit()
    pygame.quit()
