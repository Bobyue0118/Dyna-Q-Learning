import numpy as np
import tkinter as tk
import time


UNIT = 40
MAZE_H = 6     # 迷宫高6
MAZE_W = 6     # 迷宫宽6

# 在python3中，类定义默认继承object，所以写不写都没有区别
# 在python2中，并不是这样
# 在python2中，如果不继承object对象，只拥有__doc__ , module 和自己定义的name变量
# 继承了object对象，就拥有了好多可操作对象，这些都是类中的高级特性。
# 不继承object的类叫经典类，继承了object的类叫新式类
class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()                # 用Maze父类的方法初始化对象self
        self.action_space = ['u', 'd', 'l', 'r']    # 行为空间：up，down，left & right
        self.n_actions = len(self.action_space)     # 行为空间中行为的个数，即有几个可供选择的行为
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))  # 可视化窗口
        self._build_maze()                          # 调用下文定义的函数
        self.bonusFlag = False
        self.eating = True

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # 绘制grid
        for c in range(0, MAZE_W * UNIT, UNIT):    # 从0开始，以UNIT为步长，到MAZE_W * UNIT（不包括）
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        origin = np.array([20, 20])                # (0, 0)方格的中心

        # hell1
        hell1_center = origin + np.array([UNIT * 4, UNIT * 3])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - 15, hell1_center[1] - 15,
            hell1_center[0] + 15, hell1_center[1] + 15,
            fill='black')
        # hell2
        hell2_center = origin + np.array([UNIT * 3, UNIT * 4])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - 15, hell2_center[1] - 15,
            hell2_center[0] + 15, hell2_center[1] + 15,
            fill='black')
        # hell3
        hell3_center = origin + np.array([UNIT * 1, UNIT * 0])
        self.hell3 = self.canvas.create_rectangle(
            hell3_center[0] - 15, hell3_center[1] - 15,
            hell3_center[0] + 15, hell3_center[1] + 15,
            fill='black')
        # hell4
        hell4_center = origin + np.array([UNIT * 4, UNIT * 1])
        self.hell4 = self.canvas.create_rectangle(
            hell4_center[0] - 15, hell4_center[1] - 15,
            hell4_center[0] + 15, hell4_center[1] + 15,
            fill='black')
        # hell5
        hell5_center = origin + np.array([UNIT * 5, UNIT * 1])
        self.hell5 = self.canvas.create_rectangle(
            hell5_center[0] - 15, hell5_center[1] - 15,
            hell5_center[0] + 15, hell5_center[1] + 15,
            fill='black')

        # oval：椭圆形的
        # equivalent to oval_center = origin + np.array([UNIT * 4, UNIT * 4])
        oval_center = origin + UNIT * 4
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='green')

        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # create bonus
        bonus_center = origin + np.array([UNIT * 5, UNIT * 0])
        self.bonus = self.canvas.create_polygon(
            [bonus_center[0]+15, bonus_center[1],
            bonus_center[0], bonus_center[1]-15,
            bonus_center[0]-15, bonus_center[1],
            bonus_center[0], bonus_center[1]+15],
            fill='#CDCD00')
        self.bonus_location = self.canvas.create_polygon(
            bonus_center[0] - 15, bonus_center[1] - 15,
            bonus_center[0] + 15, bonus_center[1] + 15,
            fill='white')

        self.canvas.pack()

    def reset(self):
        self.canvas.delete(self.rect)
        self.canvas.delete(self.bonus)
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
        bonus_center = origin + np.array([UNIT * 5, UNIT * 0])
        self.bonus = self.canvas.create_polygon(
            [bonus_center[0]+15, bonus_center[1],
            bonus_center[0], bonus_center[1]-15,
            bonus_center[0]-15, bonus_center[1],
            bonus_center[0], bonus_center[1]+15],
            fill='#CDCD00')
        self.bonusFlag = False
        self.eating = True
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])

        s_ = self.canvas.coords(self.rect) # next state

        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
        elif (s_ == self.canvas.coords(self.bonus_location)) and (self.bonusFlag == False):
            self.bonusFlag = True
            reward = 3
            done = False
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2), self.canvas.coords(self.hell3), self.canvas.coords(self.hell4), 
        self.canvas.coords(self.hell5)]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False
        s_.append(self.bonusFlag)

        return s_, reward, done

    def render(self):
        self.update()
        time.sleep(0.1)
        if self.bonusFlag and self.eating:
            self.eating = False
            time.sleep(0.5)
            self.canvas.delete(self.bonus)


