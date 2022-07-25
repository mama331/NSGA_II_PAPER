# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:58:19 2019

@author: mama33
"""
# from insect_point import *
import math
import random
import pandas as pd
import os


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


def run(path, name):
    # path_1 = "minmoverment/" + path
    # path = "200_final"
    a = []
    b = []
    with open(path) as f:
        lines = f.read().split("\n")
        lines = list(set(lines))
    for line in lines:
        try:
            data = line.split("\t")
            a.append(float(data[0]) * (-1))
            b.append(float(data[1]) * (-1))
        except Exception as e:
            print(e)
            print(data)
    front = fast_non_dominated_sort(a, b)
    name = name.split(".")[0]
    path_out = name + ".out"
    # f = open(path_out, "r")
    sum_move = []
    max_move = []
    list_data = []
    for i in front[0]:
        # check_final(i)
        # temp = ((a[i]*(-1)), b[i]*(-1))
        list_data.append(((a[i] * (-1)), b[i] * (-1)))
        # sum_move.append(a[i]*(-1))
        # max_move.append(b[i]*(-1))
    for i in set(list_data):
        sum_move.append(i[0])
        max_move.append(i[1])
    d = {"sum_move": sum_move, "max_move": max_move}
    df = pd.DataFrame(d)
    df.to_csv(path_out)


def run_kq_test(path, name):
    a = []
    b = []
    with open(path) as f:
        lines = f.read().split("\n")
        lines = list(set(lines))
    for line in lines:
        try:
            data = line.split("\t")
            a.append(float(data[0]) * (-1))
            b.append(float(data[1]) * (-1))
        except Exception as e:
            print(e)
            print(data)
    front = fast_non_dominated_sort(a, b)
    name = name.split(".")[0]
    path_out = name + ".out"
    # f = open(path_out, "r")
    sum_move = []
    max_move = []
    list_data = []
    data = []
    for j in front:
        for i in j:
            # check_final(i)
            # temp = ((a[i]*(-1)), b[i]*(-1))
            list_data.append(((a[i] * (-1)), b[i] * (-1)))
            print(list_data)
            # sum_move.append(a[i]*(-1))
            # max_move.append(b[i]*(-1))
        data.append(list_data)
    for i in set(list_data):
        sum_move.append(i[0])
        max_move.append(i[1])
    d = {"sum_move": sum_move, "max_move": max_move}
    df = pd.DataFrame(d)
    df.to_csv(path_out)
    return data, front, a, b


if __name__ == "__main__":
    # f = open("20", "r")
    path = "2.txt"
    _, front, a, b = run_kq_test(path=path, name="2")
# =============================================================================
#     file_names = os.listdir(path)
#     for file_name in file_names:
#         #if 'voronoi' in file_name:
#         path_1 = path + file_name
#         run(path_1, file_name)
# =============================================================================
# run("200_ver1", "200_final")
# =============================================================================
#     files = ["20", "50", "100", "150", "200"]
#     for file in files:
#         run(file)
# =============================================================================

# =============================================================================
#     a = []
#     b = []
#     with open('minmoverment/200') as f:
#         for line in f:
#             data = line.split("\t")
#             a.append(float(data[0])*(-1))
#             b.append(float(data[1])*(-1))
#
#     front = fast_non_dominated_sort(a, b)
#     flag = []
#     for i in front[2]:
#         c = (a[i]*(-1), b[i]*(-1))
#         flag.append(c)
#         z = set(flag)
#         print(set(flag))
# =============================================================================
# =============================================================================
#         print(a[i]*(-1))
#         print(b[i]*(-1))
#         print("======")
# =============================================================================
# =============================================================================
#     sum_move = []
#     max_move = []
#     for i in front[0]:
#         #check_final(i)
#         sum_move.append(a[i]*(-1))
#         max_move.append(b[i]*(-1))
#     d = {"sum_move": sum_move,
#          "max_move": max_move
#          }
#     df = pd.DataFrame(d)
#     df.to_csv("20.csv")
# =============================================================================


# data = data.split("/n")
