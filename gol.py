import curses
from collections import defaultdict


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.h, self.w = self.screen.getmaxyx()
        self.h -= 1  # -1 accounts for the border column/row
        self.w -= 1
        self.state = defaultdict(int)

    def render(self):
        for y in range(1, self.h - 1):
            for x in range(1, self.w - 1):
                self.screen.addch(y, x, "o" if (x, y) in self.state else ".")

    def iterate(self):
        updated = defaultdict(int)  # holds the updated game state for next iteration

        for xy, state in self.state.items():
            n = self.count_neighbors(xy[0], xy[1])

            # any live cell with two or three live neighbors lives on to the next generation
            if n == 2 or n == 3:
                updated[(xy[0], xy[1])] = 1

            # count the neighbors of this cell's dead neighbors - bring to life if it has exactly 3 live neighbors
            for n1 in self.find_neighbors(xy[0], xy[1]):
                for n2 in self.find_neighbors(n1[0], n1[1]):
                    if self.state[(n2[0], n2[1])] == 0:
                        if self.count_neighbors(n2[0], n2[1]) == 3:
                            updated[(n2[0], n2[1])] = 1

        self.state = updated  # cell death is implicit in the new game state

    def count_neighbors(self, x, y):
        count = 0
        for xy in self.find_neighbors(x, y):
            count += self.state[xy]
        return count

    def find_neighbors(self, x, y):
        neighbors = []
        for xy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            xx = x + xy[0]
            yy = y + xy[1]
            neighbors.append((xx, yy))
        return neighbors


def main():
    from time import sleep
    from argparse import ArgumentParser
    from demos import setup_ship, setup_blinker, setup_random
    parser = ArgumentParser(description="Runs a Conway Game of Life simulation")
    parser.add_argument("--blink", action="store_true",
                        help="set up the initial game state with a blinking pattern. (default setup is random.)")
    parser.add_argument("--ship", action="store_true",
                        help="set up the initial game state with a ship pattern. (default setup is random.)")
    parser.add_argument('--step', action="store_true",
                        help="optionally wait for a keypress in between each iteration")
    args = parser.parse_args()

    screen = curses.initscr()
    screen.border(0)

    gol = Game(screen)
    if args.blink:
        setup_blinker(gol)
    elif args.ship:
        setup_ship(gol)
    else:
        setup_random(gol)

    iterations = 100000
    ch = None
    i = 0
    try:
        while ch != 27 and i < iterations:  # loop until ESC or max iterations reached
            gol.render()
            screen.refresh()
            if args.step:
                ch = screen.getch()
            else:
                sleep(0.5)
            gol.iterate()
            i += 1
    except:
        pass

    curses.endwin()
    print "Game of Life finished in", i, "iterations"

if __name__ == "__main__":
    main()
