import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


# --------------------------------------------------------
# class for manage sensor in a region
import TSClass


class MoreTarget:
    def __init__(self):
        self.neighborId = []
        self.osgId = []
        self.chiefId = -1


# ---------------------------------------------------------
class TVGreedyWSNs:
    def __init__(self, listTargets, listSensors):
        self.nTargets = len(listTargets)
        self.nSensors = len(listSensors)
        self.listTargets = listTargets
        self.listSensors = listSensors
        self.listMore = [MoreTarget() for _ in range(self.nTargets)]
        self.chiefOf = [False for _ in range(self.nSensors)]

    # make voronoi diagram with targets
    def add_neighborId(self, x, y):
        self.listMore[x].neighborId.append(y)
        self.listMore[y].neighborId.append(x)

    def make_vor(self):
        if len(self.listTargets) == 2:
            self.add_neighborId(0, 1)
        if len(self.listTargets) < 3:
            return

        points = []
        for t in self.listTargets:
            points.append([t.x, t.y])

        vor = Voronoi(points)
        for i in vor.ridge_dict:
            x = i[0]
            y = i[1]
            if x < self.nTargets and y < self.nTargets:
                self.add_neighborId(x, y)
        return vor

    # find osg of each target's voronoi
    def find_osg(self):
        for i in range(self.nSensors):
            s = self.listSensors[i]
            idMin = 0
            dMin = s.get_distance(self.listTargets[0])
            for j in range(1, self.nTargets):
                d = s.get_distance(self.listTargets[j])
                if d < dMin:
                    dMin = d
                    idMin = j
            self.listMore[idMin].osgId.append(i)
        return

    # find chief of each target's voronoi
    # other sensor in osg of target's voronoi can be aid server
    def find_chief(self, i):
        t = self.listTargets[i]
        tMore = self.listMore[i]
        if len(tMore.osgId) != 0:
            dMin = -1
            for j in self.listMore[i].osgId:
                d = t.get_distance(self.listSensors[j])
                if dMin == -1 or d < dMin:
                    dMin, tMore.chiefId = d, j
            self.chiefOf[tMore.chiefId] = True
        return

    # find chief, sensor can be aid server
    # don't find what sensor is aid server because it not necessary
    # to find the nearest sensor
    def find_csg(self, chiefId, nowNeighborId):
        csg = []
        if chiefId != -1:
            csg.append(self.listSensors[chiefId])

        for i in nowNeighborId:
            t2More = self.listMore[i]
            for j in t2More.osgId:
                if (not self.chiefOf[j]) and self.listSensors[j].free is True:
                    csg.append(self.listSensors[j])
        return csg

    # check if exit neighbors’ chief could be shared

    def neighbor_chief(self, t, nowNeighborId):
        dMin = -1
        s = Dj = None
        for i in nowNeighborId:
            t2 = self.listTargets[i]
            chiefId = self.listMore[i].chiefId
            if t2.lifeTime == 0 and chiefId != -1 and t.is_intersection(t2):
                chief = self.listSensors[chiefId]
                listS = t.get_intersection(t2)
                for j in listS:
                    d = chief.get_distance(j)
                    if dMin == -1 or d < dMin:
                        s = chief
                        Dj = j
        return s, Dj


# main process
def main(WSNs):
    vor = WSNs.make_vor()
    WSNs.find_osg()
    for i in range(WSNs.n_targets):
        WSNs.find_chief(i)

    ax = TSClass.get_ax("Check", 100)
    # voronoi_plot_2d(vor, ax)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    TSClass.draw_list(WSNs.list_targets, ax, c="b")
    # TSClass.draw_rs_list(WSNs.listTargets, ax, c='b')
    TSClass.draw_list(WSNs.list_sensors, ax, c="g")
    # TSClass.draw_id(WSNs.listTargets, ax, 'b', 't')
    # TSClass.draw_id(WSNs.listSensors, ax, 'g', 's')

    # total movement
    total = 0
    max_dis = 0
    for i in range(WSNs.n_targets):
        t = WSNs.list_targets[i]
        tMore = WSNs.listMore[i]
        if t.lifeTime == 0:
            csg = WSNs.find_csg(tMore.chiefId, tMore.neighborId)
            if len(csg) != 0:
                s = t.get_nearest_point(csg)
                Dj = t.get_nearest_location(s)
            else:
                s, Dj = WSNs.neighbor_chief(t, tMore.neighborId)
                if s is None:
                    # control 2nd order neighbor or higher neighbor
                    nowNeighborId = tMore.neighborId
                    passNeighbor = [False for _ in range(WSNs.n_targets)]
                    for i2 in nowNeighborId:
                        passNeighbor[i2] = True
                    passNeighbor[i] = True
                    while True:
                        nextNeighborId = []
                        for i2 in nowNeighborId:
                            for i3 in WSNs.listMore[i2].neighborId:
                                if not passNeighbor[i3]:
                                    nextNeighborId.append(i3)
                                    passNeighbor[i3] = True
                        if len(nextNeighborId) == 0:
                            return False
                        nowNeighborId = nextNeighborId
                        csg = WSNs.find_csg(tMore.chiefId, nowNeighborId)
                        if len(csg) != 0:
                            s = t.get_nearest_point(csg)
                            Dj = t.get_nearest_location(s)
                            break

            total = total + s.get_distance(Dj)
            max_dis = max(max_dis, s.get_distance(Dj))
            ax.plot([s.x, Dj.x], [s.y, Dj.y], color="r")
            listCoveredPoints = Dj.get_covered_points(WSNs.list_targets)
            s.update_move(Dj)
            for t in listCoveredPoints:
                t.lifeTime = 1

        if t.lifeTime == 0:
            return -1
        if tMore.chiefId != -1:
            WSNs.chiefOf[tMore.chiefId] = False
    plt.show()
    return [total, max_dis]
