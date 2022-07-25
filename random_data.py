# -*- coding: utf-8 -*-
import numpy as np
import TSClass
import matplotlib.pyplot as plt
import random
from Point import Point
from pathlib import Path
import os


def random_data(N):
    # N = 200
    cov = [[1, 0], [0, 1]]
    x = np.random.multivariate_normal([3, 3], cov, N)
    x = x * 1000
    s_x = np.random.uniform(0, 6000, N)
    s_y = np.random.uniform(0, 6000, N)
    t_x = x[:, 0]
    t_y = x[:, 1]
    return t_x, t_y, s_x, s_y


def random_data_overlap(ratio):
    # ratio = 25
    ratio = ratio / 100
    N = 200
    w = 6000
    h = 6000
    s_x = np.random.uniform(0, w / 2 + ratio * w / 2, N)
    s_y = np.random.uniform(0, h, N)
    t_x = np.random.uniform(w / 2 - ratio * w / 2, w, N)
    t_y = np.random.uniform(0, h, N)
    return t_x, t_y, s_x, s_y


def random_1cluster():
    N = 200
    s_x = np.random.uniform(0, 6000, N)
    s_y = np.random.uniform(0, 6000, N)
    t_x = np.random.uniform(2000, 4000, N)
    t_y = np.random.uniform(2000, 4000, N)
    return t_x, t_y, s_x, s_y


def draw_data(t_x, t_y, s_x, s_y, w, h):
    listSensors = []
    for i in range(len(s_x)):
        x = s_x[i]
        y = s_y[i]
        listSensors.append(TSClass.Sensor(i, x, y))
    listTargets = []
    for i in range(len(t_x)):
        x = t_x[i]
        y = t_y[i]
        listTargets.append(TSClass.Target(i, x, y))
    ax = TSClass.get_ax("Check", 100)
    # voronoi_plot_2d(vor, ax)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    TSClass.draw_list(listTargets, ax, c="b")
    TSClass.draw_list(listSensors, ax, c="g")
    TSClass.draw_rs_list(listTargets, ax, c="r")
    # =============================================================================
    #     for i in individual:
    #         ax.plot([i[0].x, i[1].x], [i[0].y, i[1].y], color='r')
    # =============================================================================
    plt.show()


def create_forder(path):
    return Path(path).mkdir(parents=True, exist_ok=True)


def save_data(t_x, t_y, s_x, s_y, path):
    path_forder = "data/change_N/"
    path = path_forder + path
    create_forder(path)
    path_sensor = os.path.join(path, "sensor.txt")
    path_target = os.path.join(path, "target.txt")
    with open(path_sensor, "w") as f:
        for i, j in zip(s_x, s_y):
            f.write(str(i))
            f.write("\t")
            f.write(str(j))
            f.write("\n")

    with open(path_target, "w") as f:
        for i, j in zip(t_x, t_y):
            f.write(str(i))
            f.write("\t")
            f.write(str(j))
            f.write("\n")


if __name__ == "__main__":
    Point.rs = 80
    t_x, t_y, s_x, s_y = random_data(250)
    draw_data(t_x, t_y, s_x, s_y, 6000, 6000)
    save_data(t_x, t_y, s_x, s_y, "250")
