# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import pandas as pd


def draw_data_max_move(data, out_path, labels, name_data):
    import matplotlib.font_manager as font_manager

    #        from matplotlib.patches import FancyArrowPatch
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(bottom=0)
    fig.subplots_adjust(top=1)
    fig.subplots_adjust(right=1)
    fig.subplots_adjust(left=0)
    WH = max(max(data[0]), max(data[1])) + 1000
    ax = fig.add_subplot(111)
    # ax = fig.add_axes([0,0,1,1])
    ax.set_ylim(0, WH)
    X = np.arange(len(data[0]))
    tt1 = ax.bar(X - 0.125, data[0], color="g", width=0.25, label="ENSGA-II")
    tt2 = ax.bar(X + 0.125, data[1], color="r", width=0.25, label="TV-Greedy")
    # labels = ["1 cluster","2 clusters","3 clusters","4 clusters","5 clusters"]
    csfont = {"fontname": "Times New Roman"}
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    plt.ylabel("Max move distance", fontsize=15, **csfont)
    plt.xlabel(name_data, fontsize=25, **csfont)
    plt.legend(handles=[tt1, tt2], loc="best", prop=font)
    plt.show()
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0)


def draw_data_sum_move(data, out_path, labels, name_data):
    import matplotlib.font_manager as font_manager

    #        from matplotlib.patches import FancyArrowPatch
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    fig = plt.figure(figsize=(8, 8))
    fig.subplots_adjust(bottom=0)
    fig.subplots_adjust(top=1)
    fig.subplots_adjust(right=1)
    fig.subplots_adjust(left=0)
    WH = max(max(data[0]), max(data[1])) + 40000
    ax = fig.add_subplot(111)
    # ax = fig.add_axes([0,0,1,1])
    ax.set_ylim(0, WH)
    X = np.arange(len(data[0]))
    tt1 = ax.bar(X - 0.125, data[0], color="g", width=0.25, label="ENSGA-II")
    tt2 = ax.bar(X + 0.125, data[1], color="r", width=0.25, label="TV-Greedy")
    # labels = ["1 cluster","2 clusters","3 clusters","4 clusters","5 clusters"]
    csfont = {"fontname": "Times New Roman"}
    ax.set_xticks(X)
    ax.set_xticklabels(labels)
    plt.ylabel("Total move distance", fontsize=15, **csfont)
    plt.xlabel(name_data, fontsize=25, **csfont)
    plt.legend(handles=[tt1, tt2], loc="best", prop=font)
    plt.show()
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    # data0:NSGA. data1 : voronoi
    label_data = {
        "Change number of targets and sensors": ["50", "100", "150", "200", "250"],
        "Change number clusters": [
            "1 cluster",
            "2 clusters",
            "3 clusters",
            "4 clusters",
            "5 clusters",
        ],
        "Change the overlap of the sensors and target": [
            "0%",
            "25%",
            "50%",
            "75%",
            "100%",
        ],
        "Change sensing range of sensors": ["30", "40", "50", "60", "70"],
    }
    data_sum_move = {
        "Change number of targets and sensors": [
            [51237.601, 86106.319, 120126.136, 205887.069, 189769.696],
            [54813.609, 82084.828, 117497.33, 194261.133, 151015.006],
        ],
        "Change number clusters": [
            [184355.014, 153934.418, 144702.062, 97690.155, 104251.476],
            [189797.235, 152471.878, 144436.025, 99626.012, 111128.545],
        ],
        "Change the overlap of the sensors and target": [
            [494436.515, 417624.703, 285313.726, 116278.687, 74535.401],
            [498285.366, 404067.719, 278493.906, 104755.24, 67697.79],
        ],
        "Change sensing range of sensors": [
            [217438.731, 213109.722, 205887.069, 173693.366, 161825.959],
            [225312.042, 215392.415, 194261.133, 176245.569, 161768.318],
        ],
    }
    data_max_move = {
        "Change number of targets and sensors": [
            [2148.841, 2223.66, 2168.801, 2806.696, 2344.208],
            [3058.421, 2679.817, 2767.156, 3244.391, 2733.115],
        ],
        "Change number clusters": [
            [2755.597, 2359.642, 2546.637, 1419.264, 1797.742],
            [2686.109, 2542.554, 3160.025, 2072.24, 2965.767],
        ],
        "Change the overlap of the sensors and target": [
            [4505.04, 4300.898, 3573.734, 2044.117, 1325.344],
            [5941.302, 5412.428, 5467.116, 4890.025, 2815.048],
        ],
        "Change sensing range of sensors": [
            [2859.228, 2817.34, 2806.696, 2770.117, 2838.712],
            [3648.461, 3540.31, 3244.391, 3019.674, 2887.334],
        ],
    }

    data = [[], []]
    data[0] = [51237.601, 86106.319, 120126.136, 205887.069, 189769.696]
    data[1] = [54813.609, 82084.828, 117497.33, 194261.133, 151015.006]
    path = "fig_ans_per_fun/"
    for key in data_max_move.keys():
        name = "max_move_" + key.replace(" ", "_") + ".png"
        path_file = path + name
        draw_data_max_move(data_max_move[key], path_file, label_data[key], key)
    # path = "fig_ans_per_fun"
    # draw_data_sum_move(data,"test_functions.png", ["50","100","150","200","250"], "Change number of targets and sensors")
    for key in data_sum_move.keys():
        name = "sum_move_" + key.replace(" ", "_") + ".png"
        path_file = path + name
        draw_data_sum_move(data_sum_move[key], path_file, label_data[key], key)
