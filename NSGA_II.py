#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 03:31:57 2021

@author: toanvd
"""

from Point import Point
import TSClass
import matplotlib.pyplot as plt
import random
import time
import numpy as np
import os
import pickle
from matplotlib.patches import Rectangle


class NSGA:
    def __init__(self, listTargets, listSensors):
        self.nTargets = len(listTargets)
        self.nSensors = len(listSensors)
        self.listTargets = listTargets
        self.listSensors = listSensors
        self.ratio_mutation = 0.2
        self.ratio_crossover = 0.8
        self.ratio_crossover_different = 0.5
        self.ratio_change = 0.8
        self.num_loop = 500
        self.num_gen = 200
        self.solution = []  # quan the kha thi
        self.solution_unfeasible = []  # quan the khong kha thi
        self.feasible_points = {}
        self.cost = {}
        self.ratio_heuristic_create = 0.02
        self.ratio_create_heuristic_unfeasible = 0.1
        self.cover_matrix = {}
        self.pareto_point = []
        # self.final_solution = int

    def get_all_feasible_points(self):
        intersection_points = []
        for i in range(self.nTargets):
            for j in range(i, self.nTargets):
                intersection_points.extend(
                    Point.get_intersection(self.listTargets[i], self.listTargets[j])
                )
        for i in self.listSensors:
            for j in self.listTargets:
                self.feasible_points[(i, j)] = []
        for i in intersection_points:
            for j in self.listTargets:
                if Point.is_cover(i, j):
                    for k in self.listSensors:
                        self.feasible_points[(k, j)].append(i)
        for i in self.listTargets:
            for j in self.listSensors:
                self.feasible_points[(j, i)].append(Point.insect_points(i, j))
        return 1

    def get_cost_move(self):
        for i in self.listSensors:
            for j in self.listTargets:
                for k in self.feasible_points[(i, j)]:
                    self.cost[i, k] = Point.get_distance(i, k)
        return 1

    def get_cover_matrix(self):
        cover_points = []
        for i in list(self.feasible_points.values()):
            cover_points.extend(i)
        for i in cover_points:
            self.cover_matrix[i] = []
        for i in cover_points:
            for j in self.listTargets:
                if Point.is_cover(i, j):
                    self.cover_matrix[i].append(j)
        return 1

    def heuristic_create_individual(self):
        a = [i for i in range(self.nTargets)]
        sensors = self.listSensors.copy()
        targets = self.listTargets.copy()
        np.random.shuffle(a)
        individual = [0 for i in range(self.nTargets)]
        for i in a:
            target = targets[i]
            sensor = Point.get_nearest_point(target, sensors)
            feasible_points = self.feasible_points[(sensor, self.listTargets[i])]
            feasible_point = Point.get_nearest_point(sensor, feasible_points)
            individual[i] = (sensor, feasible_point)
            sensors.remove(sensor)
        return individual

    def random_create_individual(self):
        individual = []
        sensors = self.listSensors.copy()
        for i in self.listTargets:
            sensor = random.choice(sensors)
            feasible_points = self.feasible_points[(sensor, i)]
            individual.append((sensor, random.choice(feasible_points)))
            sensors.remove(sensor)
        return individual

    def heuristic_create_unfeasible_individual(self):
        individual = []
        sensors = self.listSensors.copy()
        for i in self.listTargets:
            sensor = Point.get_nearest_point(i, sensors)
            feasible_points = self.feasible_points[(sensor, i)]
            # =============================================================================
            #             if len(feasible_points) > 1:
            #                 feasible_points = feasible_points
            #                 point = random.choice(feasible_points)
            #                 #sensor = Point.get_nearest_point(point, sensors)
            #             else:
            #                 point = random.choice(feasible_points)
            #             individual.append((sensor, point))
            # =============================================================================
            individual.append((sensor, random.choice(feasible_points)))
        return individual

    def random_create_unfeasible_individual(self):
        individual = []
        sensor = random.choice(self.listSensors)
        for i in self.listTargets:
            feasible_points = self.feasible_points[(sensor, i)]
            individual.append((sensor, random.choice(feasible_points)))
        return individual

    def initial(self):
        for i in range(self.num_gen):
            if random.random() < self.ratio_heuristic_create:
                self.solution.append(self.heuristic_create_individual())
            else:
                self.solution.append(self.random_create_individual())

        for i in range(self.num_gen):
            if random.random() < self.ratio_create_heuristic_unfeasible:
                self.solution_unfeasible.append(
                    self.heuristic_create_unfeasible_individual()
                )
            else:
                self.solution_unfeasible.append(
                    self.random_create_unfeasible_individual()
                )
        return 1

    def crossover(self, individual1, individual2, k):
        a = individual1[0:k] + individual2[k : self.nTargets]
        b = individual2[0:k] + individual1[k : self.nTargets]
        return [a, b]

    def run_crossover(self):
        datas = []
        for i in range(0, len(self.solution)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.nTargets)
                    a = random.choice(self.solution_unfeasible)
                    datas.extend(self.crossover(self.solution[i], a, k))
                else:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution[i], a, k))

        for i in range(0, len(self.solution_unfeasible)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution_unfeasible[i], a, k))
                else:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution_unfeasible)
                    datas.extend(self.crossover(self.solution_unfeasible[i], a, k))
        return datas

    def mutate(self, individual):
        k = random.randint(0, self.nTargets - 1)
        if random.random() < self.ratio_mutation:
            new_individual = individual[:]
            sensor = random.choice(self.listSensors)
            new_individual[k] = (
                sensor,
                random.choice(self.feasible_points[(sensor, self.listTargets[k])]),
            )
            return new_individual
        else:
            return individual

    def optimal_function(self, individual):
        # print(type(individual))
        individual_cp = list(set(individual))
        list_distance = [self.cost[(i[0], i[1])] for i in individual_cp]
        return [sum(list_distance) * (-1), max(list_distance) * (-1)]

    def caculator_optimal_function(self, solution):
        funtion1 = [self.optimal_function(i)[0] for i in solution]
        funtion2 = [self.optimal_function(i)[1] for i in solution]
        return [funtion1, funtion2]

    def selection(self):
        a = self.caculator_optimal_function(solution=self.solution)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        list_solution_sort = []
        # while len(list_solution_sort) <= self.num_gen:
        for i in front:
            list_solution_sort.extend(i)
        new_solution = [self.solution[i] for i in list_solution_sort[0 : self.num_gen]]
        # new_solution = new_solution[0:self.num_gen]
        self.solution = new_solution

        a = self.caculator_optimal_function(solution=self.solution_unfeasible)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        list_solution_sort = []
        # while len(list_solution_sort) <= self.num_gen:
        for i in front:
            list_solution_sort.extend(i)
        new_solution_unfeasible = [
            self.solution_unfeasible[i] for i in list_solution_sort[0 : self.num_gen]
        ]
        # new_solution_unfeasible = new_solution_unfeasible[0:self.num_gen]
        self.solution_unfeasible = new_solution_unfeasible
        return 1

    def fast_non_dominated_sort(self, values1, values2):
        S = [[] for i in range(0, len(values1))]
        front = [[]]
        n = [0 for i in range(0, len(values1))]
        rank = [0 for i in range(0, len(values1))]
        for p in range(0, len(values1)):
            S[p] = []
            n[p] = 0
            for q in range(0, len(values1)):
                if (
                    (values1[p] > values1[q] and values2[p] > values2[q])
                    or (values1[p] >= values1[q] and values2[p] > values2[q])
                    or (values1[p] > values1[q] and values2[p] >= values2[q])
                ):
                    if q not in S[p]:
                        S[p].append(q)
                elif (
                    (values1[q] > values1[p] and values2[q] > values2[p])
                    or (values1[q] >= values1[p] and values2[q] > values2[p])
                    or (values1[q] > values1[p] and values2[q] >= values2[p])
                ):
                    n[p] = n[p] + 1
            if n[p] == 0:
                rank[p] = 0
                if p not in front[0]:
                    front[0].append(p)

        i = 0
        while front[i] != []:
            Q = []
            for p in front[i]:
                for q in S[p]:
                    n[q] = n[q] - 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        if q not in Q:
                            Q.append(q)
            i = i + 1
            front.append(Q)

        del front[len(front) - 1]
        return front

    def check_sensor(self, individual):  # check dieu kien 1 sensor di toi 2 vi tri
        check = True
        flag = {i[0]: -1 for i in individual}
        # print(flag)
        for i in range(0, len(individual)):
            if flag[individual[i][0]] == -1:
                flag[individual[i][0]] = i
                # print(flag)
            elif individual[i][1] != individual[flag[individual[i][0]]][1]:
                check = False
            else:
                pass
        return check

    def print_final_solution(self, out_path):
        for i in self.solution_unfeasible:
            self.fix_sensor(i)
        self.solution.extend(self.solution_unfeasible)
        for i in self.solution:
            # self.check_contrain_2(i)
            self.check_final(i)
        a = self.caculator_optimal_function(self.solution)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        with open(out_path, "a") as f:
            for i in front[0]:
                self.pareto_point.append([opt1[i] * (-1), opt2[i] * (-1)])
                f.write(str(opt1[i] * (-1)))
                f.write("\t")
                f.write(str(opt2[i] * (-1)))
                f.write("\n")
            f.write("toanvd")
            f.write("\n")
            # test.draw_solution(self.solution[i],1000,1000)
        return -1

    def fix_sensor(
        self, individual
    ):  # sua ca the vi pham dieu kien 1 sensor di toi 2 vi tri
        flag = {i[0]: -1 for i in individual}
        sensors_not_used = []
        for i in self.listSensors:
            try:
                a = flag[i]
            except:
                sensors_not_used.append(i)
        for i in range(0, len(individual)):
            if flag[individual[i][0]] == -1:
                flag[individual[i][0]] = i
            elif individual[i][1] != individual[flag[individual[i][0]]][1]:
                sensor = random.choice(sensors_not_used)
                if (
                    individual[i][1]
                    not in self.feasible_points[(sensor, self.listTargets[i])]
                ):
                    individual[i] = (
                        sensor,
                        random.choice(
                            self.feasible_points[(sensor, self.listTargets[i])]
                        ),
                    )
                else:
                    individual[i] = (sensor, individual[i][1])
                sensors_not_used.remove(sensor)
                flag[sensor] = i
            else:
                pass
        return -1

    def check_contrain_2(self, individual):  # 2 cam bien khong di cung toi mot vi tri
        a = {}
        for i in range(0, self.nTargets):
            try:
                k = a[individual[i][1]]
                if (
                    self.cost[(individual[i][0], individual[i][1])]
                    > self.cost[(individual[k][0], individual[k], 1)]
                ):
                    individual[i] = individual[k]
                else:
                    individual[k] = individual[i]
            except:
                a[individual[i][1]] = i
        return individual

    def check_final(self, individual):
        cover = []
        for i in range(self.nTargets):
            cover_check = self.cover_matrix[individual[i][1]]
            flag = 0
            for j in cover_check:
                if j not in cover:
                    flag = 1
                    cover.append(j)
            if flag == 0:
                # a = (individual[i][0], individual[i][0])
                individual[i] = individual[i - 1]
        return individual, cover

    def local_search(self, list_data):
        datas = []
        for i in self.solution:
            if random.random() < self.ratio_mutation:
                individual = i.copy()
                individual = self.mutate(individual)
                datas.append(individual)
        for i in list_data:
            if random.random() < 2 * self.ratio_mutation:
                individual = i.copy()
                individual = self.mutate(individual)
                datas.append(individual)

        return datas

    def save_solution(self, path):
        import pickle

        with open(path, "wb") as fp:
            pickle.dump(self.solution[0], fp)

    def draw_solution(self, individual, w, h, path, h_lower):
        import matplotlib.font_manager as font_manager

        #        from matplotlib.patches import FancyArrowPatch
        font = font_manager.FontProperties(
            family="Times New Roman",
            # weight='bold',
            style="normal",
            size=15,
        )
        ax = TSClass.get_ax("", 100)
        # voronoi_plot_2d(vor, ax)
        ax.set_xlim(0, w)
        ax.set_ylim(h_lower, h)
        TSClass.draw_rs_list(self.listTargets, ax, c="lightslategray")
        TSClass.draw_list(self.listTargets, ax, c="r", m="*")
        TSClass.draw_list(self.listSensors, ax, c="g", m="o")
        ax.plot([], [], "*", c="r", label="Target".format("*"), linewidth=5)
        ax.plot([], [], "o", c="g", label="Sensor".format("o"), linewidth=5)

        for i in individual:
            # plt.quiver([i[0].x, i[1].x], [i[0].y, i[1].y], color='black')
            # ax.plot([i[0].x, i[1].x], [i[0].y, i[1].y], color='black',linestyle ='-|>')
            plt.annotate(
                "",
                xy=(i[1].x, i[1].y),
                xytext=(i[0].x, i[0].y),
                xycoords="data",
                arrowprops={
                    "arrowstyle": "->",
                    "linestyle": "-",
                    "linewidth": 2,
                    "shrinkA": 0,
                    "shrinkB": 0,
                },
            )
            # ar = FancyArrowPatch([i[0].x, i[1].x], [i[0].y, i[1].y], color='black',arrowstyle='->')
            # ax.add_patch(ar)
        ax.plot(
            [i[0].x, i[1].x],
            [i[0].y, i[1].y],
            color="black",
            marker=">",
            solid_joinstyle="miter",
            linewidth=3,
            label="Path",
        )
        # plt.show()
        #   fig.tight_layout()
        ax.legend(loc="lower center", prop=font, ncol=3)
        plt.savefig(path)

    def draw_data(self, w, h, path, ratio):
        import matplotlib.font_manager as font_manager

        #        from matplotlib.patches import FancyArrowPatch
        font = font_manager.FontProperties(
            family="Times New Roman", weight="normal", style="normal", size=20
        )
        ax = TSClass.get_ax("", 100)
        # voronoi_plot_2d(vor, ax)
        ax.set_xlim(0, w)
        ax.set_ylim(-700, h)
        # TSClass.draw_rs_list(self.listTargets, ax, c='lightslategray')
        TSClass.draw_list(self.listTargets, ax, c="r", m="*")
        TSClass.draw_list(self.listSensors, ax, c="g", m="o")
        ax.plot([], [], "*", c="r", label="Target".format("*"), markersize=12)
        ax.plot([], [], "o", c="g", label="Sensor".format("o"), markersize=12)
        # =============================================================================
        #         if ratio !=100:
        #             ax.plot([w/2 + ratio*w/200,w/2 + ratio*w/200], [0, h], color='black',linestyle ='--')
        #             ax.plot([w/2 - ratio*w/200,w/2 - ratio*w/200], [0, h], color='black',linestyle ='--', label = 'domain overlap')
        #         else:
        #             ax.plot([w/2 - ratio*w/200,w/2 - ratio*w/200], [0, h], color='black',linestyle ='-', label = 'domain overlap')
        # =============================================================================

        # rect = Rectangle((w/2 + ratio*w/,0),h,ratio*w/100,linewidth=1,edgecolor='r',facecolor='none')
        rect = Rectangle(
            (w / 2 - ratio * w / 200, 0),
            ratio * w / 100,
            h,
            linewidth=1,
            edgecolor="black",
            facecolor="lightslategray",
            linestyle="--",
            label="domain overlap",
            alpha=0.3,
        )

        ax.add_patch(rect)
        ax.legend(
            loc="lower center", prop=font, ncol=3, borderpad=0.3, labelspacing=0.05
        )
        plt.savefig(path)

    def run(self, out_path):
        self.get_all_feasible_points()
        self.get_cost_move()
        self.get_cover_matrix()
        self.initial()
        i = 0
        while i <= self.num_loop:
            datas = []
            datas = self.run_crossover()
            datas = [self.mutate(i) for i in datas]
            datas.extend(self.local_search(datas))
            datas.extend(self.local_search(datas))
            for data in datas:
                if self.check_sensor(data):
                    self.solution.append(data)
                else:
                    if random.random() < self.ratio_change:
                        self.fix_sensor(data)
                        self.solution.append(data)
                    else:
                        self.solution_unfeasible.append(data)
            self.selection()
            # print(self.caculator_optimal_function(self.solution[0:1]))
            # self.draw_pareto(i)
            # print(time.time()- start)
            i += 1
        # out_path = "1.txt"
        self.print_final_solution(out_path)

    def test_feasible_points(self):
        Point.rs = 20
        listSensors = []
        listX = [75, 40, 55, 65, 62.5, 15]
        listY = [75, 80, 70, 50, 6, 40]
        for i in range(len(listX)):
            x = listX[i]
            y = listY[i]
            listSensors.append(TSClass.Sensor(i, x, y))
        listX = [60, 30]
        listY = [40, 40]
        listTargets = []
        for i in range(len(listX)):
            x = listX[i]
            y = listY[i]
            listTargets.append(TSClass.Target(i, x, y))
        test = NSGA(listSensors=listSensors, listTargets=listTargets)
        test.get_all_feasible_points()
        test = NSGA(listSensors=listSensors, listTargets=listTargets)
        test.get_all_feasible_points()
        a = list(test.feasible_points.values())
        b = []
        for i in a:
            b.extend(a)

        ax = TSClass.get_ax("Check", 100)
        # voronoi_plot_2d(vor, ax)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        TSClass.draw_list(test.listTargets, ax, c="b")
        TSClass.draw_list(test.listSensors, ax, c="g")
        TSClass.draw_rs_list(test.listTargets, ax, c="b")
        TSClass.draw_list(b, ax, c="r")
        plt.show()


def test_draw():
    path = "data/cplex_data/50/"
    path_sensor = os.path.join(path, "50_sensor")
    path_target = os.path.join(path, "50_target")
    listSensors = []
    listTargets = []
    with open(path_sensor, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listSensors.append(Point(float(a[0]), float(a[1])))

    with open(path_target, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listTargets.append(Point(float(a[0]), float(a[1])))
    test = NSGA(listSensors=listSensors, listTargets=listTargets)
    test.get_all_feasible_points()
    test.get_cost_move()
    test.get_cover_matrix()
    a = test.heuristic_create_individual()
    test.draw_solution(a, 1000, 1000, "fig/heuristic_create_individual.png")
    a = test.heuristic_create_unfeasible_individual()
    test.draw_solution(a, 1000, 1000, "fig/heuristic_create_infeasible_individual.png")
    a = test.random_create_individual()
    test.draw_solution(a, 1000, 1000, "fig/random_create_individual.png")
    a = test.random_create_unfeasible_individual()
    test.draw_solution(a, 1000, 1000, "fig/random_create_infeasible_individual.png")


def draw_data():
    path = "/home/toanvd/Downloads/cluster"
    path = "data/data_overlap/"
    # for j in ['1','2','3_1','4','5']:
    for j in os.listdir(path):
        forder = os.path.join(path, j)
        path_sensor = os.path.join(forder, "sensor.txt")
        path_target = os.path.join(forder, "target.txt")
        listSensors = []
        listTargets = []
        with open(path_sensor, "r") as f:
            _data = f.read().split("\n")
        _data = [i for i in _data if len(i) > 1]
        for i in _data:
            a = i.split("\t")
            listSensors.append(Point(float(a[0]), float(a[1])))

        with open(path_target, "r") as f:
            _data = f.read().split("\n")
        _data = [i for i in _data if len(i) > 1]
        for i in _data:
            a = i.split("\t")
            listTargets.append(Point(float(a[0]), float(a[1])))
        test = NSGA(listSensors=listSensors, listTargets=listTargets)
        out_path = "fig/data1/data_overlap_" + j + ".png"
        test.draw_data(6000, 6000, out_path, int(j))


def run_overlap(path):
    Point.rs = 50
    out_path = os.path.join(path, "kq_nsga_ii.txt")
    path_sensor = os.path.join(path, "sensor.txt")
    path_target = os.path.join(path, "target.txt")
    listSensors = []
    listTargets = []
    with open(path_sensor, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listSensors.append(Point(float(a[0]), float(a[1])))

    with open(path_target, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listTargets.append(Point(float(a[0]), float(a[1])))
    for i in range(50):
        test = NSGA(listSensors=listSensors, listTargets=listTargets)
        test.run(out_path=out_path)


def draw_a_pareto():
    import matplotlib.font_manager as font_manager

    path = "data/cplex_data/50"
    Point.rs = 50
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    out_path = os.path.join(path, "kq_nsga_ii.txt")
    path_sensor = os.path.join(path, "50_sensor")
    path_target = os.path.join(path, "50_target")
    listSensors = []
    listTargets = []
    with open(path_sensor, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listSensors.append(Point(float(a[0]), float(a[1])))

    with open(path_target, "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listTargets.append(Point(float(a[0]), float(a[1])))
    test = NSGA(listSensors=listSensors, listTargets=listTargets)
    test.num_loop = 2
    test.num_gen = 200
    test.run(out_path="2.txt")
    a = test.caculator_optimal_function(solution=test.solution)
    opt1 = a[0]
    opt2 = a[1]
    front = test.fast_non_dominated_sort(opt1, opt2)
    opt1 = [i * -1 for i in opt1]
    opt2 = [i * -1 for i in opt2]
    clor = ["r", "b", "g", "orange", "m"]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    # ax.set_ylim(500, 1150)
    # ax.set_xlim(5800, 8700)
    X_list = []
    Y_list = []
    x1 = 6200
    for i in range(5):
        X = [opt1[j] for j in front[i]]
        Y = [opt2[j] for j in front[i]]
        X_list.extend(X)
        Y_list.extend(Y)
        tt2 = plt.scatter(X, Y, marker="o", c=clor[i], linewidths=3, facecolors="none")
        x_1 = [x for x, _ in sorted(zip(X, Y))]
        y_1 = [x for _, x in sorted(zip(X, Y))]
        plt.plot(x_1, y_1, c=clor[i], linestyle="--", label="Front" + str(i))
        # =============================================================================
        #         if i <5:
        #             ax.annotate('Front ' + str(i), xy=(x_1[2],y_1[2]), xytext=(x1,1100), fontsize=15,
        #                         fontproperties=font,
        #                     arrowprops=dict(facecolor='black', linewidth=2,arrowstyle="->"))
        #         else:
        #             #print(x_1[0],y_1[0])
        #             ax.annotate('Front ' + str(i), xy=(7180,800), xytext=(x1,1100), fontsize=15,
        #                 arrowprops=dict(facecolor='black',linewidth=2,arrowstyle="->"))
        # =============================================================================

        x1 += 500

    # plt.plot(x_1,y_1, c ='r', linestyle ='--',label='Pareto front')

    csfont = {"fontname": "Times New Roman"}
    plt.xlabel("Total move distance", fontsize=20, **csfont)
    plt.ylabel("Max move distance", fontsize=20, **csfont)
    plt.legend(loc="best", prop=font)
    plt.savefig("pareto_front.png", bbox_inches="tight")
    return X_list, Y_list


def draw_11():
    import matplotlib.font_manager as font_manager

    Point.rs = 50
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    opt1 = [i * -1 for i in a]
    opt2 = [i * -1 for i in b]
    clor = ["r", "b", "g", "orange", "m"]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    for i in range(4):
        X = [opt1[j] for j in data[i]]
        Y = [opt2[j] for j in data[i]]
        tt2 = plt.scatter(X, Y, marker="o", c=clor[i], linewidths=3, facecolors="none")
        x_1 = [x for x, _ in sorted(zip(X, Y))]
        y_1 = [x for _, x in sorted(zip(X, Y))]
        plt.plot(x_1, y_1, c=clor[i], linestyle="--", label="Level " + str(i))
    csfont = {"fontname": "Times New Roman"}
    plt.xlabel("Total move distance", fontsize=20, **csfont)
    plt.ylabel("Max move distance", fontsize=20, **csfont)
    plt.legend(loc="best", prop=font)
    plt.savefig("pareto_front_2.png", bbox_inches="tight")


def draw_test():
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    clor = ["r", "b", "g", "orange", "m"]
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.set_ylim(500, 1150)
    ax.set_xlim(5800, 8700)
    x1 = 6200
    for i in range(5):
        X = [opt1[j] for j in front[i]]
        Y = [opt2[j] for j in front[i]]
        tt2 = plt.scatter(X, Y, marker="o", c=clor[i], linewidths=3, facecolors="none")
        x_1 = [x for x, _ in sorted(zip(X, Y))]
        y_1 = [x for _, x in sorted(zip(X, Y))]
        plt.plot(x_1, y_1, c=clor[i], linestyle="--")
        if i != 2:
            ax.annotate(
                "Front " + str(i),
                xy=(x_1[2], y_1[2]),
                xytext=(x1, 1100),
                fontsize=15,
                fontproperties=font,
                arrowprops=dict(facecolor="black", linewidth=2, arrowstyle="->"),
            )
        else:
            # print(x_1[0],y_1[0])
            ax.annotate(
                "Front " + str(i),
                xy=(7180, 800),
                xytext=(x1, 1100),
                fontsize=15,
                arrowprops=dict(facecolor="black", linewidth=2, arrowstyle="->"),
            )

        x1 += 500

    # plt.plot(x_1,y_1, c ='r', linestyle ='--',label='Pareto front')
    csfont = {"fontname": "Times New Roman"}
    plt.xlabel("Total move distance", fontsize=20, **csfont)
    plt.ylabel("Max move distance", fontsize=20, **csfont)
    # plt.legend(loc='best',prop=font)
    plt.savefig("pareto_front.png", bbox_inches="tight")


def find_all_file_excel(path):
    # path = "/home/toanvd/Documents"
    all_forders = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isdir(os.path.join(path, f))
    ]
    all_files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
    ]
    while len(all_forders) > 0:
        path = all_forders.pop(0)
        foders = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isdir(os.path.join(path, f))
        ]
        files = [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        all_forders.extend(foders)
        all_files.extend(files)
    # file_excels = [i for i in all_files if '.xlsx' in i or '.xls' in i ]
    return all_files


if __name__ == "__main__":
    # draw_data()
    # while 1:
    #     try:
    #         X_list, Y_list = draw_a_pareto()
    #         break
    #     except:
    #         pass
# =============================================================================
#     path =  '/home/toanvd/Downloads/nsga_II_data/nsga_II/data'
#     files = find_all_file_excel(path)
#     files = [i for i in files if 'solution' in i and 'png' not in i]
#     for file in files:
#         if 'random' in file:
#             listSensors = []
#             listTargets = []
#             open_file = open(file, "rb")
#             loaded_list = pickle.load(open_file)
#             path_file = '/home/toanvd/Downloads/nsga_II_data/nsga_II/data/random_data/200'
#             Point.rs = int(file.split("_")[-1])
#             path_sensor = os.path.join(path_file, 'sensor.txt')
#             path_target = os.path.join(path_file, 'target.txt')
#             with open(path_sensor,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listSensors.append(Point(float(a[0]),float(a[1])))
#
#             with open(path_target,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listTargets.append(Point(float(a[0]),float(a[1])))
#             test = NSGA(listSensors=listSensors, listTargets=listTargets)
#             out_path = file + "_image.png"
#             test.draw_solution(loaded_list,6000,6000,out_path,-500)
#
#         elif 'cplex' not in file:
#             Point.rs=50
#     #file= files[0]
#             listSensors = []
#             listTargets = []
#             open_file = open(file, "rb")
#             loaded_list = pickle.load(open_file)
#             path_sensor = file.replace('solution', 'sensor.txt')
#             path_target = file.replace('solution', 'target.txt')
#             with open(path_sensor,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listSensors.append(Point(float(a[0]),float(a[1])))
#
#             with open(path_target,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listTargets.append(Point(float(a[0]),float(a[1])))
#             test = NSGA(listSensors=listSensors, listTargets=listTargets)
#             out_path = file + "_image.png"
#             test.draw_solution(loaded_list,6000,6000,out_path,-500)
#         else:
#             pass
#             Point.rs = 50
#             listSensors = []
#             listTargets = []
#             open_file = open(file, "rb")
#             loaded_list = pickle.load(open_file)
#             path_sensor = file.replace('solution', 'sensor.txt')
#             path_target = file.replace('solution', 'target.txt')
#             with open(path_sensor,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listSensors.append(Point(float(a[0]),float(a[1])))
#
#             with open(path_target,'r') as f:
#                 _data = f.read().split("\n")
#             _data = [i for i in _data if len(i)>1]
#             for i in _data:
#                 a = i.split("\t")
#                 listTargets.append(Point(float(a[0]),float(a[1])))
#             test = NSGA(listSensors=listSensors, listTargets=listTargets)
#             out_path = file + "_image.png"
#             test.draw_solution(loaded_list,6000,6000,out_path,-100)
# =============================================================================
# path = 'data/change_N/'
# =============================================================================
#     for i in os.listdir(path):
#         file_path = os.path.join(path, i)
#         print(file_path)
#         run_overlap(file_path)
# =============================================================================

# =============================================================================
    Point.rs = 5
    listSensors = []
    listTargets = []
    sensor = [(np.random.randint(0,20),np.random.randint(0,20)) for i in range(6)]
    target = [(np.random.randint(0,20),np.random.randint(0,20)) for i in range(6)]
    for i in sensor:
        listSensors.append(Point(float(i[0]),float(i[1])))
    for i in target:
        listTargets.append(Point(float(i[0]),float(i[1])))
# # =============================================================================
# #     with open("/home/toanvd/Documents/run_cplex/30/30_sensor",'r') as f:
# #         _data = f.read().split("\n")
# #     _data = [i for i in _data if len(i)>1]
# #     for i in sensor:
# #         a = i.split("\t")
# #         listSensors.append(Point(float(a[0]),float(a[1])))
# #
# #     with open("/home/toanvd/Documents/run_cplex/30/30_target",'r') as f:
# #         _data = f.read().split("\n")
# #     _data = [i for i in _data if len(i)>1]
# #     for i in target:
# #         a = i.split("\t")
# #         listTargets.append(Point(float(a[0]),float(a[1])))
# # =============================================================================
    for i in range(1):
        test = NSGA(listSensors=listSensors[0:6], listTargets=listTargets[0:6])
        test.get_all_feasible_points()
        test.get_cost_move()
        test.get_cover_matrix()
        a = test.heuristic_create_individual()
        b = test.random_create_individual()
# =============================================================================
test.run("1.txt")
# print(i)
