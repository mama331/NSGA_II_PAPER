import math
import matplotlib.pyplot as plt

NUM_FOR_COMPARE = 10**-10


def compare_leq(a, b):
    return a - b < NUM_FOR_COMPARE


# ------------------------------------------------------------
class Point:
    rs = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, ax, c):
        ax.scatter(self.x, self.y, marker=".", color=c)

    def draw_rs(self, ax, c):
        ax.add_patch(plt.Circle((self.x, self.y), radius=Point.rs, color=c, fill=False))

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
