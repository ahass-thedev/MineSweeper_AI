from matplotlib import pyplot as plt
import numpy as np
from matplotlib import colors
import random
import pandas as pd


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
        self.flags = []
        self.neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.zero_queue = []
        """Randomly populate the grid with how many mines the user chose"""
        """Fix overlap issue"""
        mine_tracker = 0
        while mine_tracker < self.total_mines:
            x, y = random.randint(0, len(self.grid) - 1), random.randint(0, len(self.grid[0]) - 1)
            self.grid[x][y] = 1
            # print("Created mine at: ", x, ",", y)
            mine_tracker += 1

        # self.grid[4][4] = 1
        # print(self.grid)
        # self.basic_agent()

        self.display_minesweeper_grid()

    def display_minesweeper_grid(self):
        colormap = colors.ListedColormap(["grey"])
        self.ax.imshow(self.grid, cmap=colormap)

        # ax.scatter(0, 0, marker=">", color="cyan", s=200)
        # self.ax.set_xticks(np.arange(0, self.dim, 1))
        # self.ax.set_yticks(np.arange(0, self.dim, 1))
        # self.ax.grid()
        # self.visited[7][5] = False
        # self.visited[5][7] = True
        # print("Value of 7 5 ", self.visited[7][5])
        # zero_queue = []

        def onclick(event):

            self.is_success_state()
            """ print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))"""
            x, y = int(round(event.xdata)), int(round(event.ydata))
            # print("Clicked: ", x, ",", y)

            if event.button == 3:
                """Set flag"""
                if self.testing_mode:
                    self.basic_agent()
                else:
                    self.draw_flag(x, y)

                """Human interaction with AI"""
                """The first cell is checked to be safe ie not a mine"""

            else:
                """reveal mine count"""
                if not self.grid[x][y] == 1:
                    self.visited[x][y] = True
                    self.reveal_mine_count(x, y)
                    # self.draw_flag(x, y)
                    # print(self.visited[9][0])

                else:
                    # self.reveal_mine(x, y)
                    self.draw_flag(x, y)
                    self.visited[x][y] = True
                    self.markers[x][y] = True
                    self.flags.append((x, y))
            # print("Clicked: ", x, ",", y)

            self.fig.canvas.draw_idle()
            # print("After the update:", self.get_neighbors(x, y))
            # print(self.visited)
            if self.mines_found >= self.total_mines:
                print("Game Over:All Mines Found -> Rerun program")
                self.success_state = False
                self.gg = True
                self.fig.canvas.mpl_disconnect(cid)
            # print(self.visited)
            # print("-------")
            # print(self.markers)

        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)

        # ani = animation.FuncAnimation(fig, animate, interval=1000)

        self.reveal_all_mines()

        plt.show()

    def get_neighbors(self, x, y):
        adjacent_mines = hidden_squares = 0
        revealed_safe = revealed_mine = 0
        hidden_squares_list = []
        open_zero_neighbors = []
        """Check if the child node is indeed an empty space"""
        """Traverse the neighbors"""
        if self.grid[x][y] == 1:
            return -99, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, open_zero_neighbors
        for i, j in self.neighbors:
            """Check that the neighbors are inbounds"""
            if x + i in range(0, self.dim) and y + j in range(0, self.dim):
                """Check if the neighbors are a mine, if they are count the neighboring mines"""
                if self.grid[x + i][y + j] == 1:
                    adjacent_mines += 1
                    # print("Found mine at: ", x + i, ",", y + j)
                    """Empty and unvisited list of cells"""
                if self.grid[x + i][y + j] == 0 and not self.visited[x + i][y + j]:
                    coords_tuple = x + i, y + j
                    open_zero_neighbors.append(coords_tuple)
                    """list of hidden squares -> unvisited"""
                if not self.visited[x + i][y + j]:
                    hidden_squares += 1
                    coords_tuple = x + i, y + j
                    hidden_squares_list.append(coords_tuple)
                # print("Found hidden square at: ", x + i, ",", y + j)
                """open safe spaces around"""
                if self.visited[x + i][y + j] and self.grid[x + i][y + j] == 0:
                    revealed_safe += 1
                    """mines discovered"""
                if self.markers[x + i][y + j]:
                    revealed_mine += 1
                    # self.draw_flag(x + i, y + j)
                    # print("Revealed mine found", x + i, y + j)
                    # print("The neighbor is ", i, j)
                    # self.draw_flag(x + i, y + j)
        """Return total mine near neighbor"""
        return adjacent_mines, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, open_zero_neighbors

    def draw_flag(self, x, y):
        self.ax.scatter(x, y, marker=">", color="red")
        # self.markers[x][y] = True
        # self.visited[x][y] = True

    def reveal_mine_count(self, x, y):
        if x in range(0, self.dim) and y in range(0, self.dim):

            adjacent_mines, _, _, _, _, _ = self.get_neighbors(x, y)
            if self.grid[x][y] == 1:
                adjacent_mines = -10
            (count) = str(adjacent_mines)
            self.ax.text(x, y, count)
            self.ax.scatter(x, y, marker="s", color="silver")
            # self.visited[x][y] = True
            self.gg = True

    def reveal_mine(self, x, y):
        if x in range(0, self.dim) and y in range(0, self.dim):
            if self.grid[x][y] == 1:
                self.ax.scatter(x, y, marker="o", color="cyan")
                # self.markers[x][y] = True
                # self.visited[x][y] = True
                self.success_state = False
                self.mines_found += 1
                print("Bomb Detonated")

    """For testing purposes -> see all bombs"""

    def reveal_all_mines(self):
        for x in range(self.dim):
            for y in range(self.dim):
                if self.grid[x][y] == 1:
                    self.ax.scatter(x, y, marker="o", color="black")
                    # self.markers[x][y] = True
                    # self.visited[x][y] = True

    def is_success_state(self):
        """check if the entire visited board is TRUE AND no bombs are hit"""

        if self.visited.all():
            for x in range(self.dim):
                for y in range(self.dim):
                    """check if the bombs are flagged"""
                    if self.markers[x][y] and self.grid[x][y] == 1:
                        self.success_state = True

    def basic_agent(self):
        """Create empty open queue to add 0 coords to"""

        """Generate random coordinates"""
        # open_tuple = self.random_cords()
        # self.revised_random()
        # x, y = open_tuple[0], open_tuple[1]
        self.zero_queue.append(self.random_cords())
        # self.visited[x][y] = True

        """if self.grid[x][y] == 1:
            print(x, y)
            print("RANDOM DETONATED THE BOMB")
            # quit()"""
        # print("The random coord is: ", zero_queue)

        while self.zero_queue:
            """if self.reveal_mine_count(x, y) == 1:
            open_tuple = self.random_cords()
            x, y = open_tuple[0], open_tuple[1]
            continue"""
            visited_chunk_cells = []
            # print(x, y)
            print("The queue", self.zero_queue)
            current_tuple = self.zero_queue.pop()
            visited_chunk_cells.append(current_tuple)
            x, y = current_tuple[0], current_tuple[1]
            self.visited[x][y] = True
            self.reveal_mine_count(x, y)
            # self.mark_all_neighbors_safe(x, y)
            """no bounds check made here - fix"""
            # random_neighbor = self.get_random_neighbor()
            direction_tuple = self.get_direction(x, y)
            # x += random_neighbor[0]
            # y += random_neighbor[1]
            if direction_tuple is not None:
                scalex, scaley = direction_tuple[0], direction_tuple[1]
            else:
                continue
            cell_data = (clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, zero_neighbors) \
                = self.get_neighbors(x, y)

            count = 0  # ghetto animation variable
            while True:
                if clue == 0:
                    self.mark_all_neighbors_safe(x, y)
                    # self.check_grid(x, y, cell_data)
                    if x + scalex in range(self.dim) and y + scaley in range(self.dim):
                        # print("Stuck here")
                        clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, \
                        zero_neighbors = self.get_neighbors(x + scalex, y + scaley)
                        if clue != 0:
                            # print("This should be the last entry")
                            pass
                        x += scalex
                        y += scaley
                        if clue == 0:
                            open_tuple = x, y
                            self.zero_queue.append(open_tuple)
                            # self.mark_all_neighbors_safe(x, y)

                        self.reveal_mine_count(x, y)
                        self.visited[x][y] = True
                        # self.fig.canvas.draw_idle()
                        """if clue != 0:
                            self.ax.imshow(self.grid, cmap=colormap)
                            plt.pause(.005)
                        if count % 50 == 0:
                            self.ax.imshow(self.grid, cmap=colormap)
                            plt.pause(.005)"""
                        count += 1
                        # time.sleep(3)
                        # self.check_grid()
                        # clue = new_clue
                        print("This do be busted lol")
                        if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                            print("Does this run")
                            self.zero_queue.append(self.random_cords())
                    else:
                        print("From the first")
                        if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                            print("Does this run")
                            self.zero_queue.append(self.random_cords())
                        break
                else:
                    print("From the second")
                    if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                        print("Does this run")
                        self.zero_queue.append(self.random_cords())
                    break
            # print(zero_queue)
            self.check_grid(visited_chunk_cells)
            visited_chunk_cells.clear()
            print("The queue before the bottom", self.zero_queue)

            # continue
        """ mines_found = np.where(self.markers is True)
        mines_found_list = list(zip(mines_found[0], mines_found[1]))
        print(mines_found_list)"""

    def random_cords(self):
        result = np.where((self.visited == 0))
        open_list = list(zip(result[0], result[1]))
        random_choice = random.choice(open_list)
        return random_choice
        # return random.randint(0, len(self.grid) - 1), random.randint(0, len(self.grid[0]) - 1)

    def improved_random_cords(self, old_location):
        result = np.where(self.visited == 0)
        open_list = list(zip(result[0], result[1]))
        random_choice = random.choice(open_list)
        if self.is_neighbor(old_location=old_location, new_location=random_choice) and len(open_list) > 8:
            return self.improved_random_cords(old_location=old_location)
        return random_choice

    def is_neighbor(self, old_location, new_location):

        for i, j in self.neighbors:
            if old_location[0] + i in range(0, self.dim) and old_location[1] + j in range(0, self.dim):
                if new_location[0] == old_location + i and new_location[1] == old_location[1] + j:
                    return True
        return False

    def get_direction(self, x, y):
        viable_direction_list = []

        for i, j in self.neighbors:
            if x + i in range(0, self.dim) and y + j in range(0, self.dim):
                if not self.visited[x + i][y + j] and not self.markers[x + i][y + j]:
                    viable_tuple = i, j
                    viable_direction_list.append(viable_tuple)
        if len(viable_direction_list) != 0:
            return random.choice(viable_direction_list)

    def check_grid(self, visited_chunk_cells):
        global_mines_revealed = len(np.where(self.markers == 1))
        while visited_chunk_cells:
            check_tuple = visited_chunk_cells.pop()
            x, y = check_tuple[0], check_tuple[1]
            clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, open_zero_neighbors \
                = self.get_neighbors(x, y)
            """All hidden squares surrounding the current cell is a mine"""
            if clue - revealed_mine == hidden_squares:
                print("Issued from all mines")
                for index, coords_tuple in enumerate(hidden_squares_list):
                    self.markers[coords_tuple[0]][coords_tuple[1]] = True
                    self.visited[coords_tuple[0]][coords_tuple[1]] = True
                    self.draw_flag(coords_tuple[0], coords_tuple[1])

            """All hidden squares surrounding the current cell is safe"""
            if 8 - clue - revealed_safe == hidden_squares:
                print("Issued from all safe")
                # self.mark_all_neighbors_safe(x=x, y=y)
                # for index, coords_tuple in enumerate(hidden_squares_list):

    def mark_all_neighbors_safe(self, x, y):
        for i, j in self.neighbors:
            if x + i in range(0, self.dim) and y + j in range(0, self.dim):
                self.visited[x + i][y + j] = True
                self.reveal_mine_count(x + i, y + j)
                if not np.any(self.zero_queue == (x, y)):
                    self.zero_queue.append((x + i, y + j))
                    # self.check_grid()
                else:
                    continue

    def get_random_neighbor(self):
        return random.choice(self.neighbors)

    def test_agent(self):
        density_vs_safe_mines_flagged = pd.DataFrame(columns=('Density', 'Safe_Mines_Flagged_Rate'))

        for density_percentage in np.arange(0.0, 1, .05):
            current_density_attempts = 0
            while current_density_attempts < 10:
                """set up the board for testing"""
                self.grid = np.zeros((self.dim, self.dim), dtype=int)
                self.visited = np.zeros((self.dim, self.dim), dtype=bool)
                self.markers = np.zeros((self.dim, self.dim), dtype=bool)
                self.total_mines = np.floor((self.dim * self.dim) * density_percentage)
                """create mines on the board"""
                mine_tracker = 0
                while mine_tracker < self.total_mines:
                    x, y = random.randint(0, len(self.grid) - 1), random.randint(0, len(self.grid[0]) - 1)
                    self.grid[x][y] = 1
                    # print("Created mine at: ", x, ",", y)
                    mine_tracker += 1
                """Run the test"""
                self.basic_agent()

                successful_mine = 0
                for x in range(0, self.dim):
                    for y in range(0, self.dim):
                        if self.markers[x][y] and self.grid[x][y] == 1:
                            successful_mine += 1
        density_vs_safe_mines_flagged.to_csv("basic_agent_density_vs_safe_mines_flagged.csv", mode='a', index=False)

    def improved_agent(self):

        """Create empty open queue to add 0 coords to"""

        """Generate random coordinates"""
        # open_tuple = self.random_cords()
        # self.revised_random()
        # x, y = open_tuple[0], open_tuple[1]
        self.zero_queue.append(self.random_cords())
        # self.visited[x][y] = True

        """if self.grid[x][y] == 1:
            print(x, y)
            print("RANDOM DETONATED THE BOMB")
            # quit()"""
        # print("The random coord is: ", zero_queue)

        while self.zero_queue:
            """if self.reveal_mine_count(x, y) == 1:
            open_tuple = self.random_cords()
            x, y = open_tuple[0], open_tuple[1]
            continue"""
            visited_chunk_cells = []
            # print(x, y)
            print("The queue", self.zero_queue)
            current_tuple = self.zero_queue.pop()
            visited_chunk_cells.append(current_tuple)
            x, y = current_tuple[0], current_tuple[1]
            self.visited[x][y] = True
            self.reveal_mine_count(x, y)
            # self.mark_all_neighbors_safe(x, y)
            """no bounds check made here - fix"""
            # random_neighbor = self.get_random_neighbor()
            direction_tuple = self.get_direction(x, y)
            # x += random_neighbor[0]
            # y += random_neighbor[1]
            if direction_tuple is not None:
                scalex, scaley = direction_tuple[0], direction_tuple[1]
            else:
                continue
            cell_data = (clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, zero_neighbors) \
                = self.get_neighbors(x, y)

            count = 0  # ghetto animation variable
            while True:
                if clue == 0:
                    self.mark_all_neighbors_safe(x, y)
                    # self.check_grid(x, y, cell_data)
                    if x + scalex in range(self.dim) and y + scaley in range(self.dim):
                        # print("Stuck here")
                        clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, \
                        zero_neighbors = self.get_neighbors(x + scalex, y + scaley)
                        if clue != 0:
                            # print("This should be the last entry")
                            pass
                        x += scalex
                        y += scaley
                        if clue == 0:
                            open_tuple = x, y
                            self.zero_queue.append(open_tuple)
                            # self.mark_all_neighbors_safe(x, y)

                        self.reveal_mine_count(x, y)
                        self.visited[x][y] = True
                        # self.fig.canvas.draw_idle()
                        """if clue != 0:
                            self.ax.imshow(self.grid, cmap=colormap)
                            plt.pause(.005)
                        if count % 50 == 0:
                            self.ax.imshow(self.grid, cmap=colormap)
                            plt.pause(.005)"""
                        count += 1
                        # time.sleep(3)
                        # self.check_grid()
                        # clue = new_clue
                        print("This do be busted lol")
                        if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                            print("Does this run")
                            self.zero_queue.append(self.random_cords())
                    else:
                        print("From the first")
                        if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                            print("Does this run")
                            self.zero_queue.append(self.random_cords())
                        break
                else:
                    print("From the second")
                    if len(self.zero_queue) == 0 and len(np.where((self.visited == 0))) != 0:
                        print("Does this run")
                        self.zero_queue.append(self.random_cords())
                    break
            # print(zero_queue)
            self.improved_check_grid(visited_chunk_cells)
            visited_chunk_cells.clear()
            print("The queue before the bottom", self.zero_queue)

    def improved_check_grid(self, visited_chunk_cells):
        while visited_chunk_cells:
            check_tuple = visited_chunk_cells.pop()
            x, y = check_tuple[0], check_tuple[1]
            clue, hidden_squares, revealed_safe, revealed_mine, hidden_squares_list, open_zero_neighbors \
                = self.get_neighbors(x, y)
            """All hidden squares surrounding the current cell is a mine"""
            if clue - revealed_mine == hidden_squares:
                print("Issued from all mines")
                for index, coords_tuple in enumerate(hidden_squares_list):
                    self.markers[coords_tuple[0]][coords_tuple[1]] = True
                    self.visited[coords_tuple[0]][coords_tuple[1]] = True
                    self.draw_flag(coords_tuple[0], coords_tuple[1])

            """If a space has as many revealed mines as the clue, the neighbors of the clue cell are safe"""
            """if clue - revealed_mine == 0:
                self.reveal_mine_count(x,y)
                self.visited

                if clue - revealed_mine == hidden_squares:
                    print("Issued from all mines")
                    for index, coords_tuple in enumerate(hidden_squares_list):
                        self.markers[coords_tuple[0]][coords_tuple[1]] = True
                        self.visited[coords_tuple[0]][coords_tuple[1]] = True
                        self.draw_flag(coords_tuple[0], coords_tuple[1])"""

            """All hidden squares surrounding the current cell is safe"""
            if 8 - clue - revealed_safe == hidden_squares:
                print("Issued from all safe")
                # self.mark_all_neighbors_safe(x=x, y=y)
                # for index, coords_tuple in enumerate(hidden_squares_list):


if __name__ == '__main__':
    dimension = int(input("Enter Dimension of the the minesweeper grid:\n"))
    total_mines = int(input("Enter how many mines should be in the game:\n"))
    human_or_ai = str(input("Play with the agent assistance[y/n]\n"))
    if human_or_ai == "y":
        minesweep = MineSweeper(dimension, total_mines, True)
    else:
        minesweep = MineSweeper(dimension, total_mines, False)
