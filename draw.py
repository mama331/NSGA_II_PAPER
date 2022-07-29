import os

def test_draw():
    path = "data/cplex_data/50/"
    # path_sensor = os.path.join(path, "50_sensor")
    # path_target = os.path.join(path, "50_target")
    # listSensors = []
    # listTargets = []
    # with open(path_sensor, "r") as f:
    #     _data = f.read().split("\n")
    # _data = [i for i in _data if len(i) > 1]
    # for i in _data:
    #     a = i.split("\t")
    #     listSensors.append(Point(float(a[0]), float(a[1])))

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
    test.draw_solution(a, 1000, 1000, "fig_dataset/heuristic_create_individual.png")
    a = test.heuristic_create_unfeasible_individual()
    test.draw_solution(a, 1000, 1000, "fig_dataset/heuristic_create_infeasible_individual.png")
    a = test.random_create_individual()
    test.draw_solution(a, 1000, 1000, "fig_dataset/random_create_individual.png")
    a = test.random_create_unfeasible_individual()
    test.draw_solution(a, 1000, 1000, "fig_dataset/random_create_infeasible_individual.png")


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
        out_path = "fig_dataset/data1/data_overlap_" + j + ".png"
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
    a = test.calculate_optimal_function(solution=test.solution)
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