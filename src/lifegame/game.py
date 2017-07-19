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
        self.options = options
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.pattern_width = options.width / self.patterns_horizontal
        self.pattern_height = options.height / self.patterns_vertical
        self.game_board = game_board

    @property
    def patterns_horizontal(self):
        return self.options.horizontal

    @property
    def patterns_vertical(self):
        return self.options.vertical

    def draw(self):
        pw, ph = self.pattern_width, self.pattern_height
        screen = self.screen
        for x in range(0, self.patterns_horizontal):
            for y in range(0, self.patterns_vertical):
                is_onboard = self.game_board.is_onboard(y, x)
                color = Game.PATT_COLOR if is_onboard else Game.BACK_COLOR
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
        self.clock.tick(self.options.clock)
        pygame.time.wait(self.options.wait)

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
