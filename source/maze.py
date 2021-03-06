import random
import math


class maze:
    dir_x = [0, 1, 1, 1, 0, -1, -1, -1]
    dir_y = [-1, -1, 0, 1, 1, 1, 0, -1]
    dis_straight = 1
    dis_slope = math.sqrt(2)


    def random_point(self):
        x = random.randint(1, self.maze_size - 1)
        y = random.randint(1, self.maze_size - 1)
        return x, y

    def random_stone(self):
        for i in range(self.stone_num):
            while True:
                x, y = self.random_point()
                if (x, y) != (1, 1) and (x, y) != (self.maze_size-2, self.maze_size-2):
                    break
            self.stone_x.append(x)
            self.stone_y.append(y)
            self.p[x][y] = 1

        # print(f"num_stone = {len(self.stone_x)}")

    def __init__(self, maze_size):
        self.stone_x = []
        self.stone_y = []
        self.maze_size = maze_size
        self.stone_num = maze_size * maze_size // 3
        self.p = [[0 for y in range(self.maze_size)] for x in range(self.maze_size)]
        self.around = [[[0 for z in range(8)] for y in range(self.maze_size)] for x in range(self.maze_size)]
        self.visited = [[0 for y in range(self.maze_size + 2)] for x in range(self.maze_size + 2)]
        self.random_stone()
        for i in range(self.maze_size):
            self.p[0][i] = self.p[i][0] = 1
        for i in range(self.maze_size):
            self.p[self.maze_size-1][i] = self.p[i][self.maze_size-1] = 1
        self.start, self.end = (1, 1), (self.maze_size, self.maze_size)
