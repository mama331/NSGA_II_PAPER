#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 00:45:19 2021

@author: toanvd
"""

"""ted on Tue Dec 10 23:33:49 2019

@author: mama33
"""

from insect_point import *
import math
import random
import pandas as pd


def get_individual_1(point_cover, sensor_cp):
    individual = []
    for i in range(num_target):
        b = random.randint(0, len(sensor_cp) - 1)
        feasible_point = point_cover[i][:]
        # feasible_point.extend(insect_points(target[i], sensor[sensor_cp[b]], R))
        # print(feasible_point)
        if calculate_distance(target[i], sensor[sensor_cp[b]]) <= (R + 0.001):
            feasible_point.append(sensor[sensor_cp[b]])
        else:
            feasible_point.extend(insect_points(target[i], sensor[sensor_cp[b]], R))
        k = random.randint(0, len(feasible_point) - 1)
        a = feasible_point[k]
        m = (sensor_cp[b], a)
        sensor_cp.pop(b)
        # =============================================================================
        #         try:
        #             sensor_cp.pop(b)
        #         except:
        #             continue
        # =============================================================================
        individual.append(m)
    return individual


def get_unfeasible_individual(point_cover):
    sensor_cp = [i for i in range(0, num_sensor)]
    individual = []
    b = random.randint(0, len(sensor_cp) - 1)
    for i in range(num_target):
        feasible_point = point_cover[i][:]
        # print(feasible_point)
        # feasible_point.extend(insect_points(target[i], sensor[sensor_cp[b]], R))
        # print(feasible_point)
        if calculate_distance(target[i], sensor[sensor_cp[b]]) <= (R + 0.001):
            feasible_point.append(sensor[sensor_cp[b]])
        else:
            feasible_point.extend(insect_points(target[i], sensor[sensor_cp[b]], R))
        # print(feasible_point)
        k = random.randint(0, len(feasible_point) - 1)
        a = feasible_point[k]
        m = (sensor_cp[b], a)
        individual.append(m)
    return individual


# =========================
def initial():
    solution = []
    solution_unfeasible = []
    while len(solution) < num_gen:
        # sensor_cp = sensor[:]
        sensor_cp = [i for i in range(0, num_sensor)]
        point_cp = point_cover_target[:]
        # individual = get_individual(point_cp,sensor_cp)
        individual = get_individual_1(point_cp, sensor_cp)
        individual_unfeasible = get_unfeasible_individual(point_cp)
        solution.append(individual)
        solution_unfeasible.append(individual_unfeasible)
        # solution.append(1)
    return solution, solution_unfeasible


def crossover(individual1, individual2, k):
    a = individual1[0:k] + individual2[k:num_target]
    b = individual2[0:k] + individual1[k:num_target]
    return [a, b]


def run_crossover():
    for i in range(0, num_gen):
        if random.random() < ratio_crossover:
            if random.random() < ratio_crossover_different:
                k = random.randint(0, num_target - 1)
                a = random.randint(0, len(solution_unfeasible) - 1)
                datas = crossover(solution[i], solution_unfeasible[a], k)
                for data in datas:
                    if check_sensor(data):
                        solution.append(data)
                    else:
                        if random.random() < ratio_change:
                            data1 = fix_sensor(data)
                            solution.append(data1)
                        else:
                            solution_unfeasible.append(data)
            else:
                k = random.randint(0, num_target - 1)
                a = random.randint(0, num_gen - 1)
                datas = crossover(solution[i], solution[a], k)

                while a == i:
                    a = random.randint(0, num_gen - 1)
                for data in datas:
                    if check_sensor(data):
                        solution.append(data)
                    else:
                        if random.random() < ratio_change:
                            data1 = fix_sensor(data)
                            solution.append(data1)
                        else:
                            solution_unfeasible.append(data)

    for i in range(0, num_gen):
        if random.random() < ratio_crossover:
            if random.random() < ratio_crossover_different:
                k = random.randint(0, num_target - 1)
                a = random.randint(0, len(solution_unfeasible) - 1)
                datas = crossover(solution[i], solution_unfeasible[a], k)
                for data in datas:
                    if check_sensor(data):
                        solution.append(data)
                    else:
                        if random.random() < ratio_change:
                            data1 = fix_sensor(data)
                            solution.append(data1)
                        else:
                            solution_unfeasible.append(data)
            else:
                k = random.randint(0, num_target - 1)
                a = random.randint(0, num_gen - 1)
                datas = crossover(solution[i], solution[a], k)
                while a == i:
                    a = random.randint(0, num_gen - 1)
                for data in datas:
                    if check_sensor(data):
                        solution.append(data)
                    else:
                        if random.random() < ratio_change:
                            data1 = fix_sensor(data)
                            solution.append(data1)
                        else:
                            solution_unfeasible.append(data)


def mutation(individual, k):
    new_individual = individual[:]
    a = random.randint(0, len(sensor) - 1)
    feasible_point = point_cover_target[k][:]
    if calculate_distance(target[k], sensor[a]) <= (R + 0.001):
        feasible_point.append(sensor[a])
    else:
        feasible_point.extend(insect_points(target[k], sensor[a], R))
    l = random.randint(0, len(feasible_point) - 1)
    b = feasible_point[l]
    m = (a, b)
    new_individual[k] = m
    # check_sensor(new_individual)
    return new_individual


def run_mutation():
    temp = []
    for i in range(0, len(solution)):
        if random.random() < ratio_mutation:
            a = random.randint(0, len(solution) - 1)
            b = random.randint(0, num_target - 1)
            temp.append(mutation(solution[a], b))
    for i in range(0, len(solution)):
        if random.random() < ratio_mutation:
            a = random.randint(0, len(solution) - 1)
            b = random.randint(0, num_target - 1)
            temp.append(mutation(solution[a], b))
            # solution.extend(mutation(solution[a], b))
            # solution[a] = mutation(solution[a], b)
    # for i in range(0, len(solution_unfeasible)):
    #     if random.random() < ratio_mutation:
    #         a =  random.randint(0, len(solution_unfeasible) -1)
    #         b =  random.randint(0, num_target -1)
    #         temp.append(mutation(solution_unfeasible[a], b) )
    for i in temp:
        if check_sensor(i):
            solution.append(i)
        else:
            if random.random() < ratio_change:
                data = fix_sensor(i)
                solution.append(data)
            else:
                solution_unfeasible.append(i)


def run_selection():
    opt1 = caculator_optimal_function(solution)[0]
    opt2 = caculator_optimal_function(solution)[1]
    front = fast_non_dominated_sort(opt1, opt2)
    # =============================================================================
    #     for i in front[0]:
    #         print("+",opt1[i]*(-1), opt2[i]*(-1),"+",)
    #     print("==============================")
    # =============================================================================
    # print(opt2[i])
    # print(solution,front)
    # print_pareto(solution,front)
    list_solution_sort = []
    while len(list_solution_sort) <= num_gen:
        for i in front:
            list_solution_sort.extend(i)
    new_solution = [solution[i] for i in list_solution_sort]
    new_solution = new_solution[0:num_gen]

    opt3 = caculator_optimal_function(solution_unfeasible)[0]
    opt4 = caculator_optimal_function(solution_unfeasible)[1]
    front1 = fast_non_dominated_sort(opt3, opt4)
    # =============================================================================
    #     for i in front1[0]:
    #         print("+",opt3[i]*(-1), opt4[i]*(-1),"+",)
    #     print("==============================")
    # =============================================================================
    # print(opt2[i])
    # print(solution,front)
    # print_pareto(solution,front)
    list_solution_unfeasible_sort = []
    while len(list_solution_unfeasible_sort) <= num_gen:
        for i in front1:
            list_solution_unfeasible_sort.extend(i)
    new_solution_unfeasible = [solution[i] for i in list_solution_sort]
    new_solution = new_solution[0:num_gen]
    new_solution_unfeasible = new_solution_unfeasible[0:num_gen]

    return new_solution, new_solution_unfeasible


def optimal_function(indi):
    indi_cp = set(indi)
    list_distance = [calculate_distance(sensor[i[0]], i[1]) for i in indi_cp]
    # print(list_distance)
    return [sum(list_distance) * (-1), max(list_distance) * (-1)]


def caculator_optimal_function(solution):
    funtion1 = [optimal_function(i)[0] for i in solution]
    funtion2 = [optimal_function(i)[1] for i in solution]

    # =============================================================================
    #     funtion1 = [optimal_function(check_final(i))[0] for i in solution]
    #     funtion2 = [optimal_function(check_final(i))[1] for i in solution]
    # =============================================================================

    # print(funtion2)
    return [funtion1, funtion2]


def check_sensor(individual):
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
            continue
    return check


def fix_sensor(individual):
    a = -10
    flag = {i[0]: -1 for i in individual}
    # print(flag)
    for i in range(0, len(individual)):
        if flag[individual[i][0]] == -1:
            flag[individual[i][0]] = i
            # print(flag)
        elif individual[i][1] != individual[flag[individual[i][0]]][1]:
            while a in flag or a < 0:
                a = random.randint(0, num_sensor - 1)
                if individual[i][1] not in point_cover_target[i]:
                    if calculate_distance(target[i], sensor[a]) <= (R + 0.001):
                        individual[i] = (a, sensor[a])
                    else:
                        individual[i] = (a, insect_points(target[i], sensor[a], R)[0])
                else:
                    individual[i] = (a, individual[i][1])
            flag[a] = i
        else:
            continue
    return individual


def fast_non_dominated_sort(values1, values2):
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


def index_of(a, list):
    for i in range(0, len(list)):
        if list[i] == a:
            return i
    return -1


def sort_by_values(list1, values):
    sorted_list = []
    while len(sorted_list) != len(list1):
        if index_of(min(values), values) in list1:
            sorted_list.append(index_of(min(values), values))
        values[index_of(min(values), values)] = math.inf
    return sorted_list


def crowding_distance(values1, values2, front):
    distance = [0 for i in range(0, len(front))]
    sorted1 = sort_by_values(front, values1[:])
    sorted2 = sort_by_values(front, values2[:])
    distance[0] = 4444444444444444
    distance[len(front) - 1] = 4444444444444444
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (
            values1[sorted1[k + 1]] - values2[sorted1[k - 1]]
        ) / (max(values1) - min(values1))
    for k in range(1, len(front) - 1):
        distance[k] = distance[k] + (
            values1[sorted2[k + 1]] - values2[sorted2[k - 1]]
        ) / (max(values2) - min(values2))
    return distance


def check_final(individual):
    a = {}
    for i in range(0, num_target):
        for j in point_cover_target[i]:
            try:
                k = a[j]
                if get_min_gen(individual[k], individual[i]):
                    individual[i] = individual[k]
                else:
                    individual[k] = individual[i]
            except:
                a[individual[i][1]] = i
    return individual


def check_final_1(individual):
    cover = []
    for i in range(len(individual)):
        cover_check = []
        flag = 0
        for j in range(len(target)):
            if calculate_distance(individual[i][1], target[j]) < R + 0.01:
                cover_check.append(j)
            for k in cover_check:
                if k not in cover:
                    flag = 1
                    cover.append(k)
        if flag == 0:
            a = tuple([individual[i][0], sensor[individual[i][0]]])
            # individual[i][1] = sensor[individual[i][0]]
            individual[i] = a
    return individual


def print_final_solution():
    for i in range(0, len(solution)):
        solution[i] = check_final(solution[i])
    for i in range(0, len(solution)):
        solution[i] = check_final_1(solution[i])
    opt1 = caculator_optimal_function(solution)[0]
    opt2 = caculator_optimal_function(solution)[1]
    front = fast_non_dominated_sort(opt1, opt2)
    f = open("200_25%_final", "a")
    for i in front[0]:
        # check_final(i)
        f.write(str(opt1[i] * (-1)))
        f.write("\t")
        f.write(str(opt2[i] * (-1)))
        f.write("\n")
    f.close()
    # print(solution[i])
    # print("+",opt1[i]*(-1), opt2[i]*(-1),"+",)


def get_min_gen(i, j):
    a = calculate_distance(i[0], i[1])
    b = calculate_distance(j[0], j[1])
    if a >= b:
        return True
    else:
        return False


if __name__ == "__main__":
    sensor = []
    target = []
    # =============================================================================
    #     dfs = pd.read_excel("Thaydoisonode.xlsx", sheet_name="Sensor")
    #     for i,j in zip(dfs.x, dfs.y):
    #         sensor.append((i,j))
    #
    #     dfs = pd.read_excel("Thaydoisonode.xlsx", sheet_name="Target")
    #     for i,j in zip(dfs.x, dfs.y):
    #         target.append((i,j))
    # =============================================================================

    # =============================================================================
    #     df = pd.ExcelFile('500t500s_1.xlsx')
    #     #dfs = pd.read_excel("Thaydoisonode.xlsx", sheet_name="20")
    #     dfs = df.parse("sensor")
    #     _x = dfs.x.tolist()
    #     _y = dfs.y.tolist()
    #     for i in range(0,len(_x)):
    #         sensor.append((_x[i],_y[i]))
    #
    #
    #     dfs = df.parse("target")
    #     _x = dfs.x.tolist()
    #     _y = dfs.y.tolist()
    #     for i in range(0,len(_x)):
    #         target.append((_x[i],_y[i]))
    # =============================================================================
    with open("30_sensor", "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        sensor.append((float(a[0]), float(a[1])))

    with open("30_target", "r") as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i) > 1]
    for i in _data:
        a = i.split("\t")
        target.append((float(a[0]), float(a[1])))

    # num_mutation = 8
    # =============================================================================
    #     df = pd.read_csv("SensorOverlaping.xlsx", sheet_name = "0%",
    #                  usecols =["sensor", "target"]
    #                  )
    #     targets =  df.target.tolist()
    #     sensors =  df.sensor.tolist()
    #     targets = [i.strip('][').split(', ') for i in targets]
    #     sensors = [i.strip('][').split(', ') for i in sensors]
    #     for i in targets:
    #         data = i[0].split(" ")
    #         try:
    #             j = (float(data[0]), float(data[1]))
    #             target.append(j)
    #         except Exception as e:
    #             print(e)
    #
    #     for i in sensors:
    #         try:
    #             j = (float(i[0]), float(i[1]))
    #             sensor.append(j)
    #         except Exception as e:
    #             print(e)
    #
    # =============================================================================
    # =============================================================================
    #     with open("target25%.txt", "r") as f:
    #         targets = f.read()
    #     targets = targets.split("\n")
    #     targets = [i.strip('][').split(', ') for i in targets]
    #     for i in targets:
    #         try:
    #             j = (float(i[0]), float(i[1]))
    #             target.append(j)
    #         except Exception as e:
    #             print(e)
    #
    #     with open("sensor25%.txt", "r") as f:
    #         sensors = f.read()
    #     sensors = sensors.split("\n")
    #     sensors = [i.strip('][').split(', ') for i in sensors]
    #     for i in targets:
    #         try:
    #             j = (float(i[0]), float(i[1]))
    #             sensor.append(j)
    #         except Exception as e:
    #             print(e)
    # =============================================================================

    ratio_mutation = 0.2
    num_loop = 500
    num_gen = 200
    # num_crossover = 10
    ratio_crossover = 0.8
    ratio_crossover_different = 0.5
    ratio_change = 0.8
    # sensor = [(1,2) , (3,4), (5,6)]
    num_sensor = len(sensor)
    # target= [(2,3),(4,5),(6,7)]
    num_target = len(target)
    R = 50
    accept_point = acceptable_point(sensor, target, R)
    point_cover_target = caculator_point_cover_target(accept_point, target, R)
    # point_cover_target = [[1,2],[0,1],[0,1,2] ]
    # num_target = len(target)
    # indi = get_individual(point_cover_target, sensor)
    solution, solution_unfeasible = initial()
    i = 0
    # =============================================================================
    #     datasets = ["20", "50", "100", "150", "200" ]
    #     for dataset in datasets:
    #         sensor = []
    #         target = []
    #         dfs = pd.read_excel("Thaydoisonode.xlsx", sheet_name=dataset)
    #         for i in dfs.sensor:
    #             sensor.append(eval(i))
    #         for j in dfs.target:
    #             target.append(eval(j))
    #         num_sensor = len(sensor)
    #         num_target = len(target)
    #         accept_point = acceptable_point(sensor, target, R)
    #         point_cover_target = caculator_point_cover_target(accept_point, target, R)
    #         i = j = 0
    #         while j < 30:
    #             solution, solution_unfeasible = initial()
    #             while i < num_loop:
    #                 run_crossover()
    #                 run_mutation()
    #                 solution, solution_unfeasible = run_selection()
    #                 i = i+1
    #             #run(solution)
    #             print_final_solution(dataset)
    #             j = j+1
    # =============================================================================
    import time

    while i < num_loop:
        start = time.time()
        run_crossover()
        run_mutation()
        solution, solution_unfeasible = run_selection()
        i = i + 1
        # print(time.time()-start)
        # break
    # run(solution)
    print_final_solution()

    # run_crossover()
    # run_mutation()
    # solution,solution_unfeasible  = run_selection()
    # run_mutation()
