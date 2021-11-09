import threading
import tkinter


class ui:
    def __init__(self, root, width=510, height=510, n=50):
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.stone = []
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
        print('new')

    def line(self):
        print('line')

    def clear(self):
        print('clear')

    def quite(self, evt):
        print('quite')

    def stop(self, evt):
        print("stop")

    def search_path(self, evt=None):
        print("search_path")

    def __update_pheromone_gragh(self):
        print("update")

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    ui(tkinter.Tk()).mainloop()
