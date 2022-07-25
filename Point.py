# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt

NUM_FOR_COMPARE = 10**-5


def compare_leq(a, b):
    return a - b < NUM_FOR_COMPARE


# ------------------------------------------------------------
class Point:
    rs = 50

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, ax, c, m):
        ax.scatter(self.x, self.y, marker=m, color=c, linewidth=3)

    def draw_rs(self, ax, c):
        # ax.add_patch(plt.Circle((self.x, self.y), radius=Point.rs, color=c, linewidth = 2, fill=False, alpha=0.3))
        ax.add_patch(plt.Circle((self.x, self.y), radius=Point.rs, color=c, alpha=0.3))

    def is_cover(self, t):
        return compare_leq(self.get_distance(t), Point.rs)

    def get_nearest_point(self, listP):
        if len(listP) == 0:
            return None
        pMin = listP[0]
        dMin = self.get_distance(pMin)
        for p in listP[1:]:
            d = self.get_distance(p)
            if d < dMin:
                pMin, dMin = p, d
        return pMin

    def get_covered_id(self, listP):
        listCoveredIds = []
        for i in range(len(listP)):
            if self.is_cover(listP[i]):
                listCoveredIds.append(i)
        return listCoveredIds

    def get_covered_points(self, listP):
        listCoveredPoint = []
        for p in listP:
            if self.is_cover(p):
                listCoveredPoint.append(p)
        return listCoveredPoint

    def get_distance(self, b):
        return math.sqrt((self.x - b.x) ** 2 + (self.y - b.y) ** 2)

    def is_intersection(self, t1):
        return compare_leq(self.get_distance(t1), 2 * Point.rs)

    def get_intersection(self, t1):
        if not self.is_intersection(t1):
            return []
        r = Point.rs
        d = self.get_distance(t1)

        if compare_leq(d, 0):
            return []

        a = (d**2) / (2 * d)
        h = math.sqrt(r**2 - a**2)
        x2 = self.x + a * (t1.x - self.x) / d
        y2 = self.y + a * (t1.y - self.y) / d

        x3 = x2 + h * (t1.y - self.y) / d
        y3 = y2 - h * (t1.x - self.x) / d
        x4 = x2 - h * (t1.y - self.y) / d
        y4 = y2 + h * (t1.x - self.x) / d
        return [Point(x3, y3), Point(x4, y4)]

    def insect_points(self, cir):
        d = self.get_distance(cir)
        if d > self.rs:
            return Point(
                self.x + self.rs / d * (cir.x - self.x),
                self.y + self.rs / d * (cir.y - self.y),
            )
        else:
            return Point(cir.x, cir.y)

    def acceptable_point(self, sensor, listP):
        points = []
        for i in listP:
            points.extend(self.get_intersection(i))
        points.append(self.insect_points(sensor))
        return points

    def to_string(self):
        return [str(self.x), str(self.y)]


# =============================================================================
# if __name__ == '__main__':
#     a = Point(4,2)
#     b = Point(1,2)
#     Point.rs = 2
#     b = Point.insect_points(a,b)
# =============================================================================
