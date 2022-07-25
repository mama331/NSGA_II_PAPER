#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 09:51:07 2021

@author: toanvd
"""

import os
import pandas as pd
import math


def check_dominated(a, b, c, d):
    flag = False
    if a < c:
        if b <= d:
            flag = True
    if b < d:
        if a <= c:
            flag = True
    return flag


def C(nsga_sum, nsga_max, voronoi_sum, voronoi_max):
    num_ngsa = len(nsga_sum)
    num_voronoi = len(voronoi_sum)
    count_nsga = 0
    count_voronoi = 0
    for i in range(0, num_ngsa):
        for j in range(0, num_voronoi):
            # flag = True
            if check_dominated(
                voronoi_sum[j], voronoi_max[j], nsga_sum[i], nsga_max[i]
            ):
                count_voronoi += 1
                break

    for i in range(0, num_voronoi):
        for j in range(0, num_ngsa):
            if check_dominated(
                nsga_sum[j], nsga_max[j], voronoi_sum[i], voronoi_max[i]
            ):
                count_nsga += 1
                # print(count_nsga)
                break
    # return [count_voronoi/num_ngsa, count_nsga/num_voronoi]
    return [count_nsga / num_voronoi, count_voronoi / num_ngsa]


def M3(nsga_sum, nsga_max, voronoi_sum, voronoi_max):
    M_nsga = math.sqrt(
        (max(nsga_max) - min(nsga_max)) ** 2 + (max(nsga_sum) - min(nsga_sum)) ** 2
    )
    M_voronoi = math.sqrt(
        (max(voronoi_sum) - min(voronoi_sum)) ** 2
        + (max(voronoi_max) - min(voronoi_max)) ** 2
    )
    # M_u = math.sqrt((max(nsga_max.extend()) - min(nsga_max)) ** 2 + (max(nsga_sum) - min(nsga_sum)) ** 2)
    nsga_sum.extend(voronoi_sum)
    nsga_max.extend(voronoi_max)
    U_sum = nsga_sum
    U_max = nsga_max
    U_sum = [-1 * i for i in U_sum]
    U_max = [-1 * i for i in U_max]
    front = fast_non_dominated_sort(U_sum, U_max)
    U_sum = [U_sum[i] for i in front[0]]
    U_max = [U_max[i] for i in front[0]]
    M_u = math.sqrt((max(U_sum) - min(U_sum)) ** 2 + (max(U_max) - min(U_max)) ** 2)
    return M_nsga, M_voronoi, M_u


# def min_point(x, y):


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


def get_min_distance(a, b, list_a, list_b):
    distance = []
    if len(list_a) == 1:
        return 0
    for i in range(0, len(list_a)):
        distance.append(math.sqrt((a - list_a[i]) ** 2 + (b - list_b[i]) ** 2))
    distance = [i for i in distance if i > 0]
    return min(distance)


def S(nsga_sum, nsga_max, voronoi_sum, voronoi_max):
    nsga_distance = []
    voronoi_distance = []
    for i in range(len(nsga_sum)):
        a = get_min_distance(nsga_sum[i], nsga_max[i], nsga_sum, nsga_max)
        nsga_distance.append(a)
        # print(nsga_distance)
    for i in range(len(voronoi_sum)):
        a = get_min_distance(voronoi_sum[i], voronoi_max[i], voronoi_sum, voronoi_max)
        voronoi_distance.append(a)
        # print(voronoi_distance)
    return sum(nsga_distance) / len(nsga_sum), sum(voronoi_distance) / len(voronoi_sum)


def run():
    n = 200
    # =============================================================================
    #     path = '/home/toanvd/Documents/kq_run_paper/change_N'
    #     file = os.listdir(path)
    #     for j in ['250','200','150','100','50']:
    #         file = [i for i in file if '50' in i and '150' not in i and '250' not in i]
    #         for i in file:
    #             if 'nsga' in i:
    #                 nsga = pd.read_csv(os.path.join(path,i))
    #             else:
    #                 voronoi = pd.read_csv(os.path.join(path,i))
    # =============================================================================
    path_nsga = "/home/toanvd/Documents/kq_run_paper/random_data/nsga_200_70.out"
    path_voronoi = "/home/toanvd/Documents/kq_run_paper/random_data/200_70_voronoi.out"
    nsga = pd.read_csv(path_nsga)
    voronoi = pd.read_csv(path_voronoi)
    nsga_sum = nsga["sum_move"].tolist()
    nsga_max = nsga["max_move"].tolist()

    voronoi_sum = voronoi["sum_move"]
    voronoi_max = voronoi["max_move"]
    c = C(nsga_sum, nsga_max, voronoi_sum, voronoi_max)
    m = M3(nsga_sum, nsga_max, voronoi_sum, voronoi_max)
    s = S(nsga_sum, nsga_max, voronoi_sum, voronoi_max)
    print(c)
    print(m)
    print(s)


def min_ans(nsga, voronoi):
    c = pd.read_csv(nsga)
    d = pd.read_csv(voronoi)
    sum_move = c["sum_move"].tolist() + d["sum_move"].tolist()
    max_move = c["max_move"].tolist() + d["max_move"].tolist()
    return (
        min(c["sum_move"].tolist()),
        min(c["max_move"].tolist()),
        min(d["sum_move"].tolist()),
        min(d["max_move"].tolist()),
    )
    # return min(sum_move), min(max_move)


if __name__ == "__main__":
    a = [
        [
            "/home/toanvd/Documents/kq_run_paper/overlap/0_overlap.out",
            "/home/toanvd/Documents/kq_run_paper/overlap/overlap_0_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/overlap/25_overlap.out",
            "/home/toanvd/Documents/kq_run_paper/overlap/overlap_25_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/overlap/50_overlap.out",
            "/home/toanvd/Documents/kq_run_paper/overlap/overlap_50_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/overlap/75_overlap.out",
            "/home/toanvd/Documents/kq_run_paper/overlap/overlap_75_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/overlap/100_overlap.out",
            "/home/toanvd/Documents/kq_run_paper/overlap/overlap_100_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/cluster/clusterkq_nsga_1cumout.txt",
            "/home/toanvd/Documents/kq_run_paper/cluster/1_cum_voronoiout.txt",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/cluster/clusterkq_nsga_ii_2cumout.txt",
            "/home/toanvd/Documents/kq_run_paper/cluster/2_cum_voronoiout.txt",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/cluster/clusterkq_nsga_ii_3out.txt",
            "/home/toanvd/Documents/kq_run_paper/cluster/3_1out.txt",
            "",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/cluster/clusterkq_nsga_ii_4cumout.txt",
            "/home/toanvd/Documents/kq_run_paper/cluster/4_cum_voronoiout.txt",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/cluster/clusterkq_nsga_ii_5cumout.txt",
            "/home/toanvd/Documents/kq_run_paper/cluster/5_cum_voronoiout.txt",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/random_data/200_30_nsga.out",
            "/home/toanvd/Documents/kq_run_paper/random_data/200_30_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/random_data/nsga_200_40.out",
            "/home/toanvd/Documents/kq_run_paper/random_data/200_40_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/random_data/200_50_nsga.out",
            "/home/toanvd/Documents/kq_run_paper/random_data/200_50_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/random_data/nsga_200_60.out",
            "/home/toanvd/Documents/kq_run_paper/random_data/200_60_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/random_data/nsga_200_70.out",
            "/home/toanvd/Documents/kq_run_paper/random_data/200_70_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor50_nsgaii.out",
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_50_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor100_nsgaii.out",
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_100_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_150_nsgaii.out",
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_150_voronoi.out",
        ],
        [
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_250_nsgaII.out",
            "/home/toanvd/Documents/kq_run_paper/change_N/thaydoisensor_250_voronoi.out",
        ],
    ]
    with open("min_ans_data.txt", "w") as f:
        for i in a:
            f.write(i[0].split("/")[-1])
            f.write("\n")
            f.write(str(min_ans(i[0], i[1])))
            f.write("\n")

# run()
# =============================================================================
#     nsga_agg = [i/n for i in nsga_sum]
#     voronoi_agg = [i/n for i in voronoi_sum]
# =============================================================================

# a , b = C(nsga_sum, nsga_max, voronoi_sum, voronoi_max)

# bo 250 [0.0, 0.5]
# (32529.32850252638, 14653.605717414079, 71283.0588863896)
# (4622.004916579086, 2225.80896393383)
