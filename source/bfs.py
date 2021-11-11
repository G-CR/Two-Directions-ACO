import copy
import time

class point:
    def __init__(self, start):
        self.path = [start]
        self.current_pos = start
        self.tot_dis = 0.0


class bfs:
    def __init__(self, maps):
        self.map = maps
        self.map.print_map()
        self.start, self.end = (1, 1), (self.map.maze_size-2, self.map.maze_size-2)

    def solve(self):
        cur_point = point(self.start)
        self.map.visited[self.start[0]][self.start[1]] = 1
        all_point = [cur_point]

        while len(all_point):
            now_point = all_point[0]
            all_point.pop(0)
            (x, y) = now_point.current_pos
            for i in range(len(self.map.dir_x)):
                tx = x + self.map.dir_x[i]
                ty = y + self.map.dir_y[i]
                # print(self.start[0])
                if self.map.p[tx][ty] == 0 and not self.map.visited[tx][ty]:
                    self.map.visited[tx][ty] = 1
                    to_point = copy.deepcopy(now_point)
                    to_point.current_pos = (tx, ty)
                    to_point.path.append((tx, ty))
                    to_point.tot_dis += self.map.dis_straight if tx == x or ty == y else self.map.dis_slope
                    all_point.append(to_point)

                    if to_point.current_pos == self.end:
                        return to_point.path
            #             print("shortest distance = {}\npath = {}".format(to_point.tot_dis, to_point.path))
            #             for p in to_point.path:
            #                 (x, y) = p
            #                 self.map.p[x][y] = 2
            #             self.map.print_map()
            #             break
            # if found:
            #     break


if __name__ == '__main__':
    nt = time.time()
    bfs(10).solve()
    print(f"bfs cost {time.time()-nt}")
