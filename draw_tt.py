import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from NSGA_II_1 import NSGA

def load_data(path):
    opt1 = []
    opt2 = []
    with open(path, 'r') as f:
        data = f.read().split("toanvd")[0:20]
    for rs in data:
        for per_rs in rs.split("\n"):
            if per_rs:
                opt1.append(per_rs.split("\t")[0])
                opt2.append(per_rs.split("\t")[1])
    opt1 = [-float(op1) for op1 in opt1 if op1]
    opt2 = [-float(op2) for op2 in opt2 if op2]
    return opt1, opt2


def fast_non_dominated_sort_rs(path):
    opt1, opt2 = load_data(path)
    nsga = NSGA([], [])
    front = nsga.fast_non_dominated_sort(opt1, opt2)
    X = [-opt1[j] for j in front[0]]
    Y = [-opt2[j] for j in front[0]]
    return X, Y



def draw(X, Y):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    font = font_manager.FontProperties(
        family="Times New Roman", weight="normal", style="normal", size=15
    )
    clor = ["r", "b", "g", "orange", "m", "y", "k", "w"]
    n_loops = [100, 200, 300, 400, 440, 460, 480, 500]
    for i in range(len(X)):
        tt2 = plt.scatter(X[i], Y[i], marker="o", c=clor[i], linewidths=3, facecolors="none")
        x_1 = [x for x, _ in sorted(zip(X[i], Y[i]))]
        y_1 = [x for _, x in sorted(zip(X[i], Y[i]))]
        plt.plot(x_1, y_1, c=clor[i], linestyle="--", label="Number loop " + str(n_loops[i]))
    csfont = {"fontname": "Times New Roman"}
    plt.xlabel("Total move distance", fontsize=20, **csfont)
    plt.ylabel("Max move distance", fontsize=20, **csfont)
    plt.legend(loc="best", prop=font)
    plt.savefig("pareto_front.png", bbox_inches="tight")
    return

def run():
    list_X = []
    list_Y = []
    for n_loop in [100,200,300,400,440,460,480,500]:
        # path = f'rs_tt/change_N/200/{n_loop}.txt'
        path = f'rs_tt/change_N/200_rerun/{n_loop}.txt'
        X, Y = fast_non_dominated_sort_rs(path)
        list_X.append(X)
        list_Y.append(Y)
    draw(list_X, list_Y)


if __name__ == "__main__":
    # path = "rs_tt/change_N/200/100.txt"
    # load_data(path)
    run()