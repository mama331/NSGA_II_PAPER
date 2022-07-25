# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import os
import Point
from Point import Point


# ------------------------------------------------------------
class Target(Point):
    def __init__(self, i, x, y):
        Point.__init__(self, x, y)
        self.i = i
        self.lifeTime = 0

    def get_copy(self):
        tCopy = Target(self.i, self.x, self.y)
        tCopy.lifeTime = self.lifeTime
        return tCopy

    def draw(self, ax, c):
        ax.scatter(self.x, self.y, marker="*", color=c)

    def get_nearest_location(self, s):
        d = self.get_distance(s)
        if Point.compare_leq(d, Point.rs):
            return Point(s.x, s.y)
        x = self.x - Point.rs * (self.x - s.x) / d
        y = self.y - Point.rs * (self.y - s.y) / d
        return Point(x, y)


# ------------------------------------------------------------
class Sensor(Point):
    def __init__(self, j, x, y):
        Point.__init__(self, x, y)
        self.j = j
        self.free = True

    def draw(self, ax, c):
        ax.scatter(self.x, self.y, marker="^", color=c)

    def update_move(self, Dj):
        self.free = False
        self.x, self.y = Dj.x, Dj.y


# ------------------------------------------
def get_ax(title, WH):
    fig = plt.figure(figsize=(8, 8))
    # fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, WH)
    ax.set_ylim(0, WH)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)
    fig.tight_layout()
    return ax


def draw_list(listP, ax, c, m):
    for p in listP:
        p.draw(ax, c, m)


def draw_rs_list(listP, ax, c):
    for p in listP:
        p.draw_rs(ax, c)


def draw_id(listP, ax, c, ch):
    for i in range(len(listP)):
        t = listP[i]
        ax.annotate(ch + str(i), (t.x, t.y), color=c, size=15)


def draw_ax(listT, listS, title):
    ax = get_ax(title, 100)
    draw_list(listT, ax, c="b")
    draw_rs_list(listT, ax, c="b")
    draw_list(listS, ax, c="g")
    # draw_rs_list(listS, ax, c='g')
    draw_id(listT, ax, "b", "t")
    draw_id(listS, ax, "g", "s")

    ax.plot([], [], "^", c="b", label="Target".format("^"))
    ax.plot([], [], "o", c="g", label="Sensor".format("o"))
    ax.legend()

    folder = "Fig/test"
    if not os.path.exists(folder):
        os.mkdir(folder)
    plt.savefig(folder + "/" + title + ".png")

    plt.show()
