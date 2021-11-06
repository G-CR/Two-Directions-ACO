import random
import math


class maze:
    maze_size = 20
    stone_num = maze_size * maze_size // 2
    stone_x = []
    stone_y = []
    dir_x = [0, 1, 1, 1, 0, -1, -1, -1]
    dir_y = [-1, -1, 0, 1, 1, 1, 0, -1]
    dis_straight = 1
    dis_slope = math.sqrt(2)

    def print_map(self):
        for i in self.maps:
            print(i)

    def random_point(self):
        x = random.randint(1, self.maze_size)
        y = random.randint(1, self.maze_size)
        return x, y

    def random_stone(self):
        for i in range(self.stone_num):
            x, y = self.random_point()
            self.stone_x.append(x)
            self.stone_y.append(y)
            self.visited[x][y] = 0
            self.maps[x][y] = 0

    def __init__(self):
        self.maps = [[1 for y in range(self.maze_size + 1)] for x in range(self.maze_size + 1)]
        self.visited = [[0 for y in range(self.maze_size + 1)] for x in range(self.maze_size + 1)]
        self.random_stone()
