import random
import math


class maze:
    stone_x = []
    stone_y = []
    dir_x = [0, 1, 1, 1, 0, -1, -1, -1]
    dir_y = [-1, -1, 0, 1, 1, 1, 0, -1]
    dis_straight = 1
    dis_slope = math.sqrt(2)

    def print_map(self):
        for i in self.p:
            print(i)

    def random_point(self):
        x = random.randint(1, self.maze_size - 1)
        y = random.randint(1, self.maze_size - 1)
        return x, y

    def random_stone(self):
        for i in range(self.stone_num):
            x, y = self.random_point()
            self.stone_x.append(x)
            self.stone_y.append(y)
            self.p[x][y] = 1

    def __init__(self, maze_size):
        self.maze_size = maze_size
        self.stone_num = maze_size * maze_size // 3
        self.p = [[0 for y in range(self.maze_size)] for x in range(self.maze_size)]
        self.around = [[[0 for z in range(8)] for y in range(self.maze_size)] for x in range(self.maze_size)]
        self.visited = [[0 for y in range(self.maze_size + 2)] for x in range(self.maze_size + 2)]
        self.random_stone()
        for i in range(self.maze_size + 1):
            self.p[0][i - 1] = self.p[i - 1][0] = 1
        for i in range(self.maze_size + 1):
            self.p[self.maze_size - 1][i - 1] = self.p[i - 1][self.maze_size - 1] = 1

        self.start, self.end = (1, 1), (self.maze_size, self.maze_size)
