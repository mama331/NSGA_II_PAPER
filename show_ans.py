#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 16:15:17 2021

@author: toanvd
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 13:48:52 2020

@author: toanvd
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import os
import pandas as pd


def draw_tt1(data, out_path):
    import matplotlib.font_manager as font_manager

    #        from matplotlib.patches import FancyArrowPatch
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    fig = plt.figure(figsize=(8, 8))
    ax = plt.gca()
    # fig.tight_layout()
    sum_move_nsga = data[1]["sum_move"].tolist()
    max_move_nsga = data[1]["max_move"].tolist()
    # =============================================================================
    #     for x,y in zip(sum_move_nsga,max_move_nsga):
    #         ax.add_patch(plt.Circle((x, y), radius=50, color='r', alpha=0.3))
    # =============================================================================
    # plt.Circle((x,y, 2), color='r', fill=False)
    # tt1 = plt.scatter(data[0]['max_move'].tolist(),data[0]['sum_move'].tolist() , marker=9, c='b', label='cplex')
    tt2 = plt.scatter(
        data[1]["sum_move"].tolist(),
        data[1]["max_move"].tolist(),
        marker="o",
        c="r",
        label="ENSGA-II",
        linewidths=3,
        facecolors="none",
    )
    tt3 = plt.scatter(
        data[2]["sum_move"].tolist(),
        data[2]["max_move"].tolist(),
        marker="s",
        c="g",
        label="TV-Greedy",
        linewidths=3,
        facecolors="none",
    )

    # =============================================================================
    #     if len(data[0]['max_move'].tolist()) > 2:
    #         X = data[0]['max_move'].tolist()
    #         Y = data[0]['sum_move'].tolist()
    #         x_1 = [x for x,_ in sorted(zip(X,Y))]
    #         y_1 = [x for _,x in sorted(zip(X,Y))]
    #         plt.plot(x_1,y_1,c ='b')
    # =============================================================================

    if len(data[1]["sum_move"].tolist()) >= 2:
        X = data[1]["sum_move"].tolist()
        Y = data[1]["max_move"].tolist()
        x_1 = [x for x, _ in sorted(zip(X, Y))]
        y_1 = [x for _, x in sorted(zip(X, Y))]
        plt.plot(x_1, y_1, c="r", linestyle="--")
    if len(data[2]["sum_move"].tolist()) >= 2:
        X = data[2]["sum_move"].tolist()
        Y = data[2]["max_move"].tolist()
        x_1 = [x for x, _ in sorted(zip(X, Y))]
        y_1 = [x for _, x in sorted(zip(X, Y))]

        plt.plot(x_1, y_1, c="g", linestyle="--")
        # plt.plot(data[0]['sum_move'].tolist(),data[0]['max_move'].tolist(),c = 'b')
    csfont = {"fontname": "Times New Roman"}
    plt.xlabel("Total move distance", fontsize=20, **csfont)
    plt.ylabel("Max move distance", fontsize=20, **csfont)
    plt.legend(handles=[tt2, tt3], loc="best", prop=font)
    # =============================================================================
    #     plt.xlim([min_x, max_x])
    #     plt.ylim([min_y, max_y])
    # =============================================================================
    # =============================================================================
    #     ax.set_yticks([250,275])
    #     ax.set_yticklabels(['250','275'])
    # =============================================================================
    fig.savefig(out_path, bbox_inches="tight")
    plt.show()


def draw_tt():
    pass


def read_input(nsga, voronoi, out_path):
    # path = "/home/toanvd/Documents/run_cplex/kq_out/60_cplex_nsga"
    # list_files = [(path + i) for i in os.listdir(path)]
    data = [0, 0, 0]
    # data[0] = pd.read_csv("/home/toanvd/Documents/kq_run_paper/random_data")
    data[1] = pd.read_csv(nsga)
    data[2] = pd.read_csv(voronoi)
    draw_tt1(data, out_path)


# path = '/home/toanvd/Documents/kq_run_paper'
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

    # draw_tt1(data[0],data[1],data[2])


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

b = [
    [
        "/home/toanvd/Documents/kq_run_paper/cplex/30/30_nsga.out",
        " /home/toanvd/Documents/kq_run_paper/cplex/30/30_voronoi.out",
        "/home/toanvd/Documents/kq_run_paper/cplex/30/30_cplex.out",
    ],
    [
        "/home/toanvd/Documents/kq_run_paper/cplex/50/50_nsga.out",
        "/home/toanvd/Documents/kq_run_paper/cplex/50/50_voronoi.out",
        "/home/toanvd/Documents/kq_run_paper/cplex/50/50_cplex.out",
    ],
]
c = "/home/toanvd/Documents/kq_run_paper/overlap/0_overlap.out"
c = c.replace(".out", "")
c = c.replace("nsgaii", "")
c = c.replace("nsgaII", "")
c = c.replace("nsga", "")
c = c.replace("voronoi", "")
for i in a:
    # c = '/home/toanvd/Documents/kq_run_paper/overlap/0_overlap.out'
    c = i[0].split("/")[-1]
    c = c.replace(".out", "")
    c = c.replace("nsgaii", "")
    c = c.replace("nsgaII", "")
    c = c.replace("nsga", "")
    c = c.replace("nsga_ii_", "")
    c = c + "_image.png"
    # c = os.path.join('fig_ans',c)
    read_input(i[0], i[1], os.path.join("fig_ans", c))

# files = find_all_file_excel(path)
# files = [i for i in files if 'backup' not in i]
# =============================================================================
# with open("file.txt",'w') as f:
#     f.write("\n".join(files))
# =============================================================================
# read_input()
