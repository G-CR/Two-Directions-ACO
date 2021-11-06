import random


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class maze:
    maze_size = 20
    stone_num = maze_size * 3

    def __init__(self):
        self.maps = [[1 for y in range(self.maze_size)] for y in range(self.maze_size)]


if __name__ == '__main__':
    maze()
