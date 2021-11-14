import copy
import random
import sys
import time
import tkinter
import threading
from aco import aco, Stack, Point
from maze import maze


class ui:
    def __init__(self, root, n=20):
        self.root = root
        self.width = n * 10 + 2
        self.height = n * 10 + 2
        self.n = n
        self.canvas = tkinter.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="#EBEBEB",
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.title("n:初始化 e:开始搜索 s:停止搜索 q:退出程序")
        self.__r = 5
        self.__lock = threading.RLock()

        self.__bindEvents()
        self.new()

    def __bindEvents(self):
        self.root.bind("q", self.quite)
        self.root.bind("n", self.new)
        self.root.bind("e", self.search_path)
        self.root.bind("s", self.stop)

    def title(self, s):
        self.root.title(s)

    def new(self, evt=None):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()
        self.map = maze(self.n+2)
        self.aco = aco(self.map, 1, 1, self.n, self.n)
        self.back_aco = aco(self.map, self.n, self.n, 1, 1)

        for i in range(len(self.aco.map.stone_x)):
            x = self.aco.map.stone_x[i] * 10
            y = self.aco.map.stone_y[i] * 10
            self.canvas.create_oval(
                x - self.__r, y - self.__r,
                x + self.__r, y + self.__r,
                fill="#ff0000",
                outline="#ffffff",
                tags="stone"
            )

        for i in range(len(self.aco.bfs_path)):
            x, y = self.aco.bfs_path[i][0]*10, self.aco.bfs_path[i][1]*10
            self.canvas.create_oval(
                x - self.__r, y - self.__r,
                x + self.__r, y + self.__r,
                fill="#00008B",
                outline="#ffffff",
                tags="bfs_path"
            )

    def line(self):
        self.canvas.delete("tmp_path")
        path = copy.deepcopy(self.aco.Beststackpath)
        while not path.empty():
            x, y = path.top().x * 10, path.top().y * 10
            path.pop()
            self.canvas.create_oval(
                x - self.__r, y - self.__r,
                x + self.__r, y + self.__r,
                fill="#48D1CC",
                outline="#ffffff",
                tags="tmp_path"
            )

            if not path.empty():
                x, y = path.bottum().x * 10, path.bottum().y * 10
                path.pop_b()
                self.canvas.create_oval(
                    x - self.__r, y - self.__r,
                    x + self.__r, y + self.__r,
                    fill="#7CFC00",
                    outline="#ffffff",
                    tags="tmp_path"
                )
            time.sleep(0.001)
            self.canvas.update()

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print(u"\n程序已退出...")
        sys.exit()

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    def stack2list(self, stack_path: Stack):
        res = []
        path = copy.deepcopy(stack_path)
        while not path.empty():
            top = path.top()
            path.pop()
            res.append((top.x, top.y))
        return res


    def merge_route(self):
        for i in range(self.aco.M):
            path = self.stack2list(copy.deepcopy(self.aco.stackpath[i]))
            back_path = self.stack2list(copy.deepcopy(self.back_aco.stackpath[i]))
            inter = tuple(set(path).intersection(set(back_path)))
            position = inter[random.randint(0, len(inter)-1)]
            p1 = path.index(position)
            p2 = back_path.index(position)
            merge_path = []
            for p in back_path[0:p2] + path[p1::-1]:
                merge_path.append(Point(p[0], p[1]))

            if len(merge_path) < self.aco.stackpath[i].size():
                self.aco.stackpath[i].stack = copy.deepcopy(merge_path)
            if len(merge_path) < self.back_aco.stackpath[i].size():
                self.back_aco.stackpath[i].stack = copy.deepcopy(merge_path)



    def search_path(self, evt=None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        print(f"BFS算法得到最优路径为: {self.aco.bfs_dis}")
        count = 1
        best = 0x7fffffff
        while self.__running:
            self.aco.search()
            self.back_aco.search()
            self.merge_route()
            self.__update_pheromone_gragh()
            self.line()
            self.canvas.update()

            if best > self.aco.bestSolution:
                best = self.aco.bestSolution
                print(f"第{count}次探索，当前最佳路径长度: {best}")
            count += 1

    def __update_pheromone_gragh(self):
        self.aco.update_phe()
        self.back_aco.update_phe()

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    ui(tkinter.Tk()).mainloop()
