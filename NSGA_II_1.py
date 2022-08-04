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
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.font_manager as font_manager


class NSGA:
    def __init__(
        self,
        list_targets,
        list_sensors,
        ratio_mutation=0.2,
        ratio_crossover=0.8,
        ratio_crossover_different=0.5,
        ratio_change=0.8,
        num_loop=500,
        num_gen=200,
        ratio_heuristic_create=0.02,
        ratio_create_heuristic_unfeasible=0.1,
    ):
        self.n_targets = len(list_targets)
        self.n_sensors = len(list_sensors)
        self.list_targets = list_targets
        self.list_sensors = list_sensors
        self.ratio_mutation = ratio_mutation
        self.ratio_crossover = ratio_crossover
        self.ratio_crossover_different = ratio_crossover_different
        self.ratio_change = ratio_change
        self.num_loop = num_loop
        self.num_gen = num_gen
        self.solution = []  # Feasible Population:
        self.solution_infeasible = []  # Infeasible Population
        self.feasible_points = {}
        self.cost = {}
        self.ratio_heuristic_create = ratio_heuristic_create
        self.ratio_create_heuristic_unfeasible = ratio_create_heuristic_unfeasible
        self.cover_matrix = {}
        self.pareto_point = []

    def get_all_feasible_points(self):
        intersection_points = []
        for i in range(self.n_targets):
            for j in range(i, self.n_targets):
                intersection_points.extend(
                    Point.get_intersection(self.list_targets[i], self.list_targets[j])
                )
        for i in self.list_sensors:
            for j in self.list_targets:
                self.feasible_points[(i, j)] = []
        for i in intersection_points:
            for j in self.list_targets:
                if Point.is_cover(i, j):
                    for k in self.list_sensors:
                        self.feasible_points[(k, j)].append(i)
        for i in self.list_targets:
            for j in self.list_sensors:
                self.feasible_points[(j, i)].append(Point.insect_points(i, j))
        return 1

    def get_cost_move(self):
        for i in self.list_sensors:
            for j in self.list_targets:
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
            for j in self.list_targets:
                if Point.is_cover(i, j):
                    self.cover_matrix[i].append(j)
        return 1

    def heuristic_create_individual(self):
        a = [i for i in range(self.n_targets)]
        sensors = self.list_sensors.copy()
        targets = self.list_targets.copy()
        np.random.shuffle(a)
        individual = [0 for i in range(self.n_targets)]
        for i in a:
            target = targets[i]
            sensor = Point.get_nearest_point(target, sensors)
            feasible_points = self.feasible_points[(sensor, self.list_targets[i])]
            feasible_point = Point.get_nearest_point(sensor, feasible_points)
            individual[i] = (sensor, feasible_point)
            sensors.remove(sensor)
        return individual

    def random_create_individual(self):
        individual = []
        sensors = self.list_sensors.copy()
        for i in self.list_targets:
            sensor = random.choice(sensors)
            feasible_points = self.feasible_points[(sensor, i)]
            individual.append((sensor, random.choice(feasible_points)))
            sensors.remove(sensor)
        return individual

    def heuristic_create_unfeasible_individual(self):
        individual = []
        sensors = self.list_sensors.copy()
        for i in self.list_targets:
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
        sensor = random.choice(self.list_sensors)
        for i in self.list_targets:
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
                self.solution_infeasible.append(
                    self.heuristic_create_unfeasible_individual()
                )
            else:
                self.solution_infeasible.append(
                    self.random_create_unfeasible_individual()
                )
        return 1

    def crossover(self, individual1, individual2, k):
        a = individual1[0:k] + individual2[k: self.n_targets]
        b = individual2[0:k] + individual1[k: self.n_targets]
        return [a, b]

    def run_crossover(self):
        datas = []
        for i in range(0, len(self.solution)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.n_targets)
                    a = random.choice(self.solution_infeasible)
                    datas.extend(self.crossover(self.solution[i], a, k))
                else:
                    k = random.randint(0, self.n_targets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution[i], a, k))

        for i in range(0, len(self.solution_infeasible)):
            if random.random() < self.ratio_crossover:
                if random.random() < self.ratio_crossover_different:
                    k = random.randint(0, self.n_targets - 1)
                    a = random.choice(self.solution)
                    datas.extend(self.crossover(self.solution_infeasible[i], a, k))
                else:
                    k = random.randint(0, self.n_targets - 1)
                    a = random.choice(self.solution_infeasible)
                    datas.extend(self.crossover(self.solution_infeasible[i], a, k))
        return datas

    def mutate(self, individual):
        k = random.randint(0, self.n_targets - 1)
        if random.random() < self.ratio_mutation:
            new_individual = individual[:]
            sensor = random.choice(self.list_sensors)
            new_individual[k] = (
                sensor,
                random.choice(self.feasible_points[(sensor, self.list_targets[k])]),
            )
            return new_individual
        else:
            return individual

    def optimal_function(self, individual):
        # print(type(individual))
        individual_cp = list(set(individual))
        list_distance = [self.cost[(i[0], i[1])] for i in individual_cp]
        return [sum(list_distance) * (-1), max(list_distance) * (-1)]

    def calculate_optimal_function(self, solution):
        function_1 = [self.optimal_function(i)[0] for i in solution]
        function_2 = [self.optimal_function(i)[1] for i in solution]
        return [function_1, function_2]

    def selection(self):
        a = self.calculate_optimal_function(solution=self.solution)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        list_solution_sort = []
        # while len(list_solution_sort) <= self.num_gen:
        for i in front:
            list_solution_sort.extend(i)
        new_solution = [self.solution[i] for i in list_solution_sort[0: self.num_gen]]
        # new_solution = new_solution[0:self.num_gen]
        self.solution = new_solution

        a = self.calculate_optimal_function(solution=self.solution_infeasible)
        opt1 = a[0]
        opt2 = a[1]
        front = self.fast_non_dominated_sort(opt1, opt2)
        list_solution_sort = []
        # while len(list_solution_sort) <= self.num_gen:
        for i in front:
            list_solution_sort.extend(i)
        new_solution_unfeasible = [
            self.solution_infeasible[i] for i in list_solution_sort[0 : self.num_gen]
        ]
        # new_solution_unfeasible = new_solution_unfeasible[0:self.num_gen]
        self.solution_infeasible = new_solution_unfeasible
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

    def check_sensor(self, individual):
        """
        check condition one sensor go to 2 position
        :param individual:
        :return:
        """
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
        for i in self.solution_infeasible:
            self.fix_sensor(i)
        self.solution.extend(self.solution_infeasible)
        for i in self.solution:
            # self.check_contrain_2(i)
            self.check_final(i)
        a = self.calculate_optimal_function(self.solution)
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
    ):
        """
        # fix individual have one sensor go to 2 position
        :param individual:
        :return:
        """
        flag = {i[0]: -1 for i in individual}
        sensors_not_used = []
        for i in self.list_sensors:
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
                    not in self.feasible_points[(sensor, self.list_targets[i])]
                ):
                    individual[i] = (
                        sensor,
                        random.choice(
                            self.feasible_points[(sensor, self.list_targets[i])]
                        ),
                    )
                else:
                    individual[i] = (sensor, individual[i][1])
                sensors_not_used.remove(sensor)
                flag[sensor] = i
            else:
                pass
        return -1

    def check_contrain_2(self, individual):
        """
        fix individual have two sensor go to 1 position
        :param individual:
        :return:
        """
        a = {}
        for i in range(0, self.n_targets):
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
        for i in range(self.n_targets):
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
        """
        save one solution
        :param path:
        :return:
        """
        import pickle
        with open(path, "wb") as fp:
            pickle.dump(self.solution[0], fp)

    def draw_solution(self, individual, w, h, path, h_lower):
        """
        draw a solution
        :param individual:
        :param w:
        :param h:
        :param path:
        :param h_lower:
        :return:
        """
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
        TSClass.draw_rs_list(self.list_targets, ax, c="lightslategray")
        TSClass.draw_list(self.list_targets, ax, c="r", m="*")
        TSClass.draw_list(self.list_sensors, ax, c="g", m="o")
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
        #   fig_dataset.tight_layout()
        ax.legend(loc="lower center", prop=font, ncol=3)
        plt.savefig(path)

    def draw_data(self, w, h, path, ratio):
        """
        draw dataset
        :param w:
        :param h:
        :param path:
        :param ratio:
        :return:
        """
        font = font_manager.FontProperties(
            family="Times New Roman", weight="normal", style="normal", size=20
        )
        ax = TSClass.get_ax("", 100)
        # voronoi_plot_2d(vor, ax)
        ax.set_xlim(0, w)
        ax.set_ylim(-700, h)
        # TSClass.draw_rs_list(self.listTargets, ax, c='lightslategray')
        TSClass.draw_list(self.list_targets, ax, c="r", m="*")
        TSClass.draw_list(self.list_sensors, ax, c="g", m="o")
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
        list_logs = [100, 200, 300, 350 ,400, 420, 440,450, 460, 480]
        self.get_all_feasible_points()
        self.get_cost_move()
        self.get_cover_matrix()
        self.initial()
        i = 0
        print(self.num_loop)
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
                        self.solution_infeasible.append(data)
            self.selection()
            if i in list_logs:
                ouput_cp = f'{out_path}{i}.txt'
                self.print_final_solution(ouput_cp)
            # print(self.caculator_optimal_function(self.solution[0:1]))
            # self.draw_pareto(i)
            # print(time.time()- start)
            i += 1
        # out_path = "1.txt"
        out_path = f'{out_path}500.txt'
        self.print_final_solution(out_path)

if __name__ == "__main__":
    Point.rs = 50
    for number_sensor in [200]:
        # for n_loop in [100, 200, 300, 400, 500]:
        list_sensors = []
        list_targets = []
        path_sensor = f'data/change_N/{number_sensor}/sensor.txt'
        path_target = f'data/change_N/{number_sensor}/target.txt'
        output_path = f'rs_tt/change_N/{number_sensor}_rerun/'
        with open(path_sensor, "r") as f:
            _data = f.read().split("\n")
        _data = [data for data in _data if len(data) > 1]
        for data in _data:
            a = data.split("\t")
            list_sensors.append(Point(float(a[0]), float(a[1])))

        with open(path_target, "r") as f:
            _data = f.read().split("\n")
        _data = [data for data in _data if len(data) > 1]
        for data in _data:
            a = data.split("\t")
            list_targets.append(Point(float(a[0]), float(a[1])))
        for i in range(1):
            test = NSGA(list_sensors=list_sensors, list_targets=list_targets)
            test.run(output_path)
