import matplotlib.pyplot as plt
import numpy as np
from random import randint
from matplotlib import colors


class MineSweeper:

    def __init__(self, dim, mine_count, test):
        """Set up global variables and create an empty MineSweeper grid"""
        self.fig, self.ax = plt.subplots(figsize=(7, 7))
        self.dim = dim
        self.total_mines = mine_count
        self.testing_mode = test
        self.grid = np.zeros((self.dim, self.dim), dtype=int)
        self.visited = np.zeros((self.dim, self.dim), dtype=bool)
        self.markers = np.zeros((self.dim, self.dim), dtype=bool)
        self.success_state = False
        self.gg = False
        self.mines_found = 0

        """Randomly populate the grid with how many mines the user chose"""
        """Fix overlap issue"""
        mine_tracker = 0
        while mine_tracker < self.total_mines:
            x, y = randint(0, len(self.grid) - 1), randint(0, len(self.grid[0]) - 1)
            self.grid[x][y] = 1
            # print("Created mine at: ", x, ",", y)
            mine_tracker += 1

        # print(self.grid)
        self.display_minesweeper_grid()

    def display_minesweeper_grid(self):
        colormap = colors.ListedColormap(["grey"])
        self.ax.imshow(self.grid, cmap=colormap)

        # ax.scatter(0, 0, marker=">", color="cyan", s=200)
        # self.ax.set_xticks(np.arange(0, self.dim, 1))
        # self.ax.set_yticks(np.arange(0, self.dim, 1))
        # self.ax.grid()

        def onclick(event):
            self.is_success_state()
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            x, y = int(round(event.xdata)), int(round(event.ydata))
            if event.button == 3:
                """Set flag"""
                self.draw_flag(x, y)
            else:
                """reveal mine count"""
                if not self.grid[x][y] == 1:
                    self.reveal_mine_count(x, y)
                else:
                    self.reveal_mine(x, y)
            print("Clicked: ", x, ",", y)

            self.fig.canvas.draw_idle()
            print(self.get_neighbors(x, y))
            if self.mines_found >= self.total_mines:
                print("Game Over:All Mines Found -> Rerun program")
                self.success_state = False
                self.gg = True
                self.fig.canvas.mpl_disconnect(cid)

        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)

        # ani = animation.FuncAnimation(fig, animate, interval=1000)
        # self.reveal_all_mines()
        plt.show()

    def get_neighbors(self, x, y):
        adjacent_mines = hidden_squares = 0
        revealed_safe = revealed_mine = 0
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        """Check if the child node is indeed an empty space"""
        """Traverse the neighbors"""
        for i, j in neighbors:
            """Check that the neighbors are inbounds"""
            if x + i < self.dim and y + j < self.dim:
                """Check if the neighbors are a mine, if they are count the neighboring mines"""
                if self.grid[x + i][y + j] == 1:
                    adjacent_mines += 1
                    # print("Found mine at: ", x + i, ",", y + j)
                if not self.visited[x + i][y + j]:
                    hidden_squares += 1
                # print("Found hidden square at: ", x + i, ",", y + j)
                if self.visited[x + i][y + j] and self.grid[x + i][y + j] == 0:
                    revealed_safe += 1
                if self.visited[x + i][y + j] and self.grid[x + i][y + j] == 1:
                    revealed_mine += 1
        """Return total mine near neighbor"""
        return adjacent_mines, hidden_squares, revealed_safe, revealed_mine

    def draw_flag(self, x, y):
        self.ax.scatter(x, y, marker=">", color="red")
        self.markers[x][y] = True
        self.visited[x][y] = True

    def reveal_mine_count(self, x, y):
        adjacent_mines, _, _, _ = self.get_neighbors(x, y)
        (count) = str(adjacent_mines)
        self.ax.text(x, y, count)
        self.ax.scatter(x, y, marker="s", color="silver")
        self.visited[x][y] = True
        self.gg = True

    def reveal_mine(self, x, y):
        self.ax.scatter(x, y, marker="o", color="cyan")
        self.markers[x][y] = True
        self.visited[x][y] = True
        self.success_state = False
        self.mines_found += 1
        print("Bomb Detonated")

    """For testing purposes -> see all bombs"""

    def reveal_all_mines(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == 1:
                    self.ax.scatter(x, y, marker="o", color="black")
                    self.markers[x][y] = True
                    self.visited[x][y] = True

    def is_success_state(self):
        """check if the entire visited board is TRUE AND no bombs are hit"""

        if self.visited.all():
            for x in range(self.dim):
                for y in range(self.dim):
                    """check if the bombs are flagged"""
                    if self.markers[x][y] and self.grid[x][y] == 1:
                        self.success_state = True

    def basic_agent(self):

        """Start at a random point in the grid -> first move"""
        x, y = randint(0, len(self.grid) - 1), randint(0, len(self.grid[0]) - 1)

        """The first cell is checked to be safe"""

        if self.grid[x][y] != 1:
            clue, hidden_squares, revealed_safe, revealed_mine = self.get_neighbors(x, y)
            self.visited[x][y] = True
            """also the mine count"""
            safe_squares = 8 - clue

            """8 total spaces, 3 is the clue meaning 3 mines. meaning 5 empty. 8 - 3 = 5"""

        for x in range(self.dim):
            for y in range(self.dim):
                pass
        pass


if __name__ == '__main__':
    dimension = int(input("Enter Dimension of the the minesweeper grid:\n"))
    total_mines = int(input("Enter how many mines should be in the game:\n"))
    human_or_ai = str(input("Testing mode?[y/n]\n"))
    if human_or_ai == "y":
        minesweep = MineSweeper(dimension, total_mines, True)
    else:
        minesweep = MineSweeper(dimension, total_mines, False)
