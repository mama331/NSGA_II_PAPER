# -*- coding: utf-8 -*-
from Point import Point
import TSClass
import matplotlib.pyplot as plt
import random
import time
import numpy as np

# import sys
class NSGA:
    def __init__(self, listTargets, listSensors):
        self.nTargets = len(listTargets)
        self.nSensors = len(listSensors)
        self.listTargets = listTargets
        self.listSensors = listSensors
        self.ratio_mutation = 0.3
        self.ratio_crossover = 0.8
        self.ratio_crossover_different = 0.7
        self.ratio_change = 0.8
        self.num_loop = 500
        self.num_gen = 200
        self.solution = []  # quan the kha thi
        self.solution_unfeasible = []  # quan the khong kha thi
        self.feasible_points = {}
        self.cost = {}
        self.ratio_heuristic_create = 0
        self.ratio_create_heuristic_unfeasible = 0
        self.cover_matrix = {}
        self.pareto_point = []
        self.final_solution = []

    def get_all_feasible_points(self):
        for i in self.listSensors:
            for j in self.listTargets:
                self.feasible_points[(i, j)] = []
                self.feasible_points[(i, j)].extend(
                    Point.acceptable_point(j, i, self.listTargets)
                )
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
        individual = []
        sensors = self.listSensors.copy()
        for i in self.listTargets:
            sensor = Point.get_nearest_point(i, sensors)
            feasible_points = self.feasible_points[(sensor, i)]
            feasible_point = Point.get_nearest_point(sensor, feasible_points)
            individual.append((sensor, feasible_point))
            # individual.append((sensor, random.choice(feasible_points)))
            sensors.remove(sensor)
        return individual

    def heuristic_create_individual_1(self):
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
                self.solution.append(self.heuristic_create_individual_1())
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
        # return -1

    def crossover(self, individual1, individual2, k):
        a = individual1[0:k] + individual2[k : self.nTargets]
        b = individual2[0:k] + individual1[k : self.nTargets]
        return [a, b]

    def run_crossover(self):
        datas = []
        for l in range(0, len(self.solution)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution_unfeasible)
                    # print(l)
                    datas.extend(self.crossover(self.solution[l], a, k))
                else:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution[l], a, k))
        for l in range(0, len(self.solution_unfeasible)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution_unfeasible[l], a, k))
                else:
                    k = random.randint(0, self.nTargets - 1)
                    a = random.choice(self.solution_unfeasible)
                    datas.extend(self.crossover(self.solution_unfeasible[l], a, k))
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
            test.draw_solution(self.solution[i], 1000, 1000)
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

    def local_search(self):
        datas = []
        for i in self.solution:
            if random.random() < 2 * self.ratio_mutation:
                individual = i.copy()
                individual = self.mutate(individual)
                datas.append(individual)
        return datas

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

    def draw_solution(self, individual, w, h):
        ax = TSClass.get_ax("Check", 100)
        # voronoi_plot_2d(vor, ax)
        ax.set_xlim(0, w)
        ax.set_ylim(0, h)
        TSClass.draw_list(self.listTargets, ax, c="b")
        TSClass.draw_list(self.listSensors, ax, c="g")
        TSClass.draw_rs_list(self.listTargets, ax, c="b")
        for i in individual:
            ax.plot([i[0].x, i[1].x], [i[0].y, i[1].y], color="r")
        plt.show()

    def draw_pareto(self, count):
        for i in self.solution:
            self.check_contrain_2(i)
            self.check_final(i)
        a = self.caculator_optimal_function(self.solution)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        for i in front[0]:
            self.pareto_point.append([opt1[i] * (-1), opt2[i] * (-1)])
        fig = plt.figure()
        # ax = plt.gca()
        sum_move = [i[0] for i in self.pareto_point]
        max_move = [i[1] for i in self.pareto_point]
        sum_move = [x for x, _ in sorted(zip(sum_move, max_move))]
        max_move = [x for _, x in sorted(zip(sum_move, max_move))]
        plt.scatter(sum_move, max_move, marker=8, c="r", label="NSGA")
        plt.plot(sum_move, max_move, c="g")
        plt.xlabel("Tổng khoảng cách di chuyển")
        plt.ylabel("Khoảng cách cảm biến động di chuyển xa nhất")
        # plt.legend(handles=[tt2, tt3], loc='best')
        path = "test_" + str(count) + ".png"
        fig.savefig(path)
        self.pareto_point = []
        # plt.show()

    def run(self):
        self.get_all_feasible_points()
        self.get_cost_move()
        self.get_cover_matrix()
        self.initial()
        i = 0
        while i <= self.num_loop:
            # start = time.time()
            datas = []
            datas = self.run_crossover()
            datas = [self.mutate(i) for i in datas]
            datas.extend(self.local_search())
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
            print(self.caculator_optimal_function(self.solution[0:1]))
            # self.draw_pareto(i)
            # print(time.time()- start)
            i += 1
        out_path = "1.txt"
        self.print_final_solution(out_path)
        # self.draw_pareto(1)


def test_fix_sensor():
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
    test.get_cost_move()
    indi = test.random_create_unfeasible_individual()
    a = test.optimal_function(indi)
    test.solution.append(indi)
    test.solution.append(indi)
    # test.fix_sensor(test.solution[1])
    return test


def run_1():
    import pandas as pd

    sensor = []
    target = []
    df = pd.ExcelFile("/home/toanvd/Documents/run_100/Thaydoisonode.xlsx")
    dfs = df.parse("200")
    for i in dfs.sensor:
        sensor.append(eval(i))
    for j in dfs.target:
        target.append(eval(j))
    listX = [i[0] for i in target]
    listY = [i[1] for i in target]
    listTargets = []
    for i in range(len(listX)):
        x = listX[i]
        y = listY[i]
        listTargets.append(TSClass.Target(i, x, y))
    listX = [i[0] for i in sensor]
    listY = [i[1] for i in sensor]
    listSensors = []
    for i in range(len(listX)):
        x = listX[i]
        y = listY[i]
        listSensors.append(TSClass.Sensor(i, x, y))
    test = NSGA(listSensors=listSensors, listTargets=listTargets)
    test.run()
    return test


def check_solution(individual):
    test = NSGA()
    flag = 1
    for i in range(test.nTargets):
        if not Point.is_cover(individual[i][1], test.listTargets[i]):
            flag = 0
    print(flag)


if __name__ == "__main__":
    # test = NSGA(listSensors=listSensors, listTargets=listTargets)
    # test.run()
    # a = test.cover_matrix
    # test = run_1()

    Point.rs = 50
    listSensors = []
    listTargets = []
    with open("/home/toanvd/Documents/run_cplex/30/30_sensor", "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listSensors.append(Point(float(a[0]), float(a[1])))

    with open("/home/toanvd/Documents/run_cplex/30/30_target", "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        listTargets.append(Point(float(a[0]), float(a[1])))
    for i in range(1):
        test = NSGA(listSensors=listSensors, listTargets=listTargets)
        test.run()
        # print(i)
# =============================================================================
#     import pandas as pd
#     sensor = []
#     target = []
#     df = pd.ExcelFile('/home/toanvd/Documents/run_100/Thaydoisonode.xlsx')
#     dfs = df.parse("200")
#     for i in dfs.sensor:
#         sensor.append(eval(i))
#     for j in dfs.target:
#         target.append(eval(j))
#     listX = [i[0] for i in target]
#     listY = [i[1] for i in target]
#     listTargets = []
#     for i in range(len(listX)):
#         x = listX[i]
#         y = listY[i]
#         listTargets.append(TSClass.Target(i, x, y))
#     listX = [i[0] for i in sensor]
#     listY = [i[1] for i in sensor]
#     listSensors = []
#     for i in range(len(listX)):
#         x = listX[i]
#         y = listY[i]
#         listSensors.append(TSClass.Sensor(i, x, y))
#     test = NSGA(listSensors=listSensors, listTargets=listTargets)
#     test.get_all_feasible_points()
#     test.get_cost_move()
#     test.get_cover_matrix()
#     a = test.feasible_points
#     test.initial()
#     solution = test.solution
#     solution_unfeasible = test.solution_unfeasible
#     i =0
#     while i < 5:
#         datas = test.run_crossover()
#         datas = [test.mutate(i) for i in datas]
#         for data in datas:
#             if test.check_sensor(data):
#                 test.solution.append(data)
#             else:
#                 if random.random() < test.ratio_change:
#                     test.fix_sensor(data)
#                     test.solution.append(data)
#                 else:
#                     test.solution_unfeasible.append(data)
#         test.selection()
#         i+=1
# =============================================================================
# =============================================================================
#     ax = TSClass.get_ax("Check", 100)
#     ax.set_xlim(-100, 200)
#     ax.set_ylim(-100, 200)
#     TSClass.draw_list(listTargets, ax, c='b')
#     TSClass.draw_list(listSensors, ax, c='g')
#     TSClass.draw_rs_list(listTargets, ax, c='b')
#     TSClass.draw_id(listSensors, ax, 'g', 's')
#     TSClass.draw_id(listTargets, ax, 'b', 't')
# =============================================================================
# =============================================================================
#     test = NSGA(listSensors=listSensors, listTargets=listTargets)
#     test.get_all_feasible_points()
#     test.get_cost_move()
#     a = test.feasible_points
#     b = test.cost
#     indi = test.heuristic_create_individual()
#     test.draw_solution(indi)
# =============================================================================
# TSClass.draw_list(a[(listSensors[0],listTargets[0])], ax, c='r')
# plt.show()
