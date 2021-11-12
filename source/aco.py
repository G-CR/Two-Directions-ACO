import copy
import math
import random
import time
from maze import maze
from bfs import bfs


class Stack(object):
    def __init__(self):
        self.stack = []

    def push(self, value):  # 进栈
        self.stack.append(value)

    def pop(self):  # 出栈
        return self.stack.pop()

    def empty(self):  # 如果栈为空
        if len(self.stack) == 0:
            return True
        else:
            return False

    def top(self):
        # 取出目前stack中最新的元素
        return self.stack[-1]

    def size(self):
        return len(self.stack)


# 坐标类
class Point:
    x = 0
    y = 0


class aco:
    def __init__(self, n):
        self.map = maze(n + 2)
        # self.map.print_map()
        self.start, self.end = Point(), Point()
        self.start.x, self.start.y = 1, 1
        self.end.x, self.end.y = n, n

        self.N = self.map.maze_size
        self.M = 10  # 每一轮中蚂蚁的个数
        self.RcMax = 10  # 迭代次数
        self.IN = 1.0  # 信息素的初始量

        self.add = [[0.0 for j in range(self.N)] for i in range(self.N)]
        self.phe = [[self.IN for j in range(self.N)] for i in range(self.N)]
        self.MAX = 0x7fffffff

        self.bestSolution = self.MAX  # 最短距离
        self.Beststackpath = Stack()  # 最优路线

        # alphe信息素的影响因子，betra路线距离的影响因子，rout信息素的保持度，Q用于计算每只蚂蚁在其路迹留下的信息素增量
        # 初始化变量参数和信息数组
        self.alphe, self.betra, self.rout, self.Q = 0.0001, 14.0, 0.35, 10.0
        self.offset = [Point() for i in range(8)]
        self.offset[0].x = 0
        self.offset[0].y = 1  # 向右
        self.offset[1].x = 1
        self.offset[1].y = 1  # 向右下
        self.offset[2].x = 1
        self.offset[2].y = 0  # 向下
        self.offset[3].x = 1
        self.offset[3].y = -1  # 向左下
        self.offset[4].x = 0
        self.offset[4].y = -1  # 向左
        self.offset[5].x = -1
        self.offset[5].y = -1  # 向左上
        self.offset[6].x = -1
        self.offset[6].y = 0  # 向上
        self.offset[7].x = -1
        self.offset[7].y = 1  # 向右上

        # 每轮M只蚂蚁，每一轮结束后才进行全局信息素更新
        self.stackpath = [Stack() for i in range(self.M)]
        # 拷贝障碍地图
        self.Ini_map = [copy.deepcopy(self.map) for i in range(self.M)]
        # 记录每一只蚂蚁的当前位置
        self.Allposition = [Point() for i in range(self.M)]

        [self.bfs_path, self.bfs_dis] = bfs(self.map).solve()

    def search(self):
        # 先清空每一只蚂蚁的路线存储栈
        for i in range(self.M):
            while not self.stackpath[i].empty():
                self.stackpath[i].pop()

        for i in range(self.M):
            self.Ini_map[i] = copy.deepcopy(self.map)
            # 将起点初始化为障碍点
            self.Ini_map[i].p[self.start.x][self.start.y] = 1
            # 起点入栈
            self.stackpath[i].push(self.start)
            # 初始化每一只蚂蚁的当前位置
            self.Allposition[i] = copy.deepcopy(self.start)

        # 开启M只蚂蚁循环
        for j in range(self.M):
            # print("第" + str(j) + "只蚂蚁")
            while (self.Allposition[j].x) != (self.end.x) or (self.Allposition[j].y) != (self.end.y):
                # print("<" + (str)(Allposition[j].x) + "," + (str)(Allposition[j].y) + ">")
                # 选择下一步
                psum = 0.0
                for op in range(4):
                    # 计算下一个可能的坐标
                    x = self.Allposition[j].x + self.offset[op].x
                    y = self.Allposition[j].y + self.offset[op].y
                    if (self.Ini_map[j].around[self.Allposition[j].x][self.Allposition[j].y])[op] == 0 and \
                            self.Ini_map[j].p[x][y] != 1:
                        psum += math.pow(self.phe[x][y], self.alphe) * math.pow((10.0 / self.stackpath[j].size()),
                                                                                self.betra)
                # 判断是否有选择
                # 如找到了下一点
                if psum != 0.0:
                    drand = random.uniform(0, 1)
                    pro = 0.0
                    x, y = 0, 0
                    for re in range(4):
                        # 计算下一个可能的坐标
                        x = self.Allposition[j].x + self.offset[re].x
                        y = self.Allposition[j].y + self.offset[re].y
                        if (self.Ini_map[j].around[self.Allposition[j].x][self.Allposition[j].y])[re] == 0 and \
                                self.Ini_map[j].p[x][y] != 1:
                            pro += (pow(self.phe[x][y], self.alphe) * pow((10.0 / self.stackpath[j].size()),
                                                                          self.betra)) / psum
                            if pro >= drand:
                                break
                    # 入栈
                    self.Allposition[j].x = x
                    self.Allposition[j].y = y
                    temp_Point = copy.deepcopy(self.Allposition[j])
                    self.stackpath[j].push(temp_Point)
                    # 设置障碍
                    self.Ini_map[j].p[self.Allposition[j].x][self.Allposition[j].y] = 1
                else:  # 没找到了下一点
                    # 向后退一步，出栈
                    p = self.stackpath[j].pop()
                    # 消除入栈时设置的障碍
                    self.Ini_map[j].p[self.Allposition[j].x][self.Allposition[j].y] = 0
                    if self.stackpath[j].empty() == True:
                        return False
                    # 设置回溯后的Allposition
                    if self.Allposition[j].x == self.stackpath[j].top().x:
                        if (self.Allposition[j].y - self.stackpath[j].top().y) == 1:  # 向右
                            (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[
                                0] = 1  # 标记该方向已访问
                        if (self.Allposition[j].y - self.stackpath[j].top().y) == -1:  # 向左
                            (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[
                                4] = 1  # 标记该方向已访问
                    elif self.Allposition[j].y == self.stackpath[j].top().y:
                        if (self.Allposition[j].x - self.stackpath[j].top().x) == 1:  # 向下
                            (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[
                                2] = 1  # 标记该方向已访问
                        if (self.Allposition[j].x - self.stackpath[j].top().x) == -1:  # 向上
                            (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[
                                6] = 1  # 标记该方向已访问
                    else:
                        if (self.Allposition[j].y - self.stackpath[j].top().y) == 1:
                            if (self.Allposition[j].x - self.stackpath[j].top().x) == 1:  # 向右下
                                (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[1] = 1
                            else:  # 向右上
                                (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[7] = 1
                        else:
                            if (self.Allposition[j].x - self.stackpath[j].top().x) == 1:  # 向左下
                                (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[3] = 1
                            else:  # 向左上
                                (self.Ini_map[j].around[self.stackpath[j].top().x][self.stackpath[j].top().y])[5] = 1

                    self.Allposition[j].x = self.stackpath[j].top().x
                    self.Allposition[j].y = self.stackpath[j].top().y
        # 保存最优路线
        for i in range(self.M):
            solution = 0
            tmp_path = copy.deepcopy(self.stackpath[i])
            top = tmp_path.top()
            tmp_path.pop()
            while not tmp_path.empty():
                if abs(top.x-tmp_path.top().x) + abs(top.y-tmp_path.top().y) == 2:
                    solution += math.sqrt(2)
                else:
                    solution += 1
                top = tmp_path.top()
                tmp_path.pop()

            if solution < self.bestSolution:
                self.Beststackpath = copy.deepcopy(self.stackpath[i])
                self.bestSolution = solution

        # 计算每一只蚂蚁在其每一段路径上留下的信息素增量
        # 初始化信息素增量数组
        for i in range(self.N):
            for j in range(self.N):
                self.add[i][j] = 0

        for i in range(self.M):
            # 先算出每只蚂蚁的路线的总距离solu
            solu = self.stackpath[i].size()
            d = self.Q / solu
            while self.stackpath[i].empty() == False:
                self.add[self.stackpath[i].top().x][self.stackpath[i].top().y] += d
                self.stackpath[i].pop()

    def update_phe(self):  # 更新信息素
        for i in range(self.N):
            for j in range(self.N):
                self.phe[i][j] = self.phe[i][j] * self.rout + self.add[i][j]
                # 为信息素设置一个下限值和上限值
                if self.phe[i][j] < 0.0001:
                    self.phe[i][j] = 0.0001
                if self.phe[i][j] > 20:
                    self.phe[i][j] = 20