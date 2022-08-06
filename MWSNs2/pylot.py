import PointClass
import TSClass
import TVGreedy
import pandas as pd
import numpy as np

# point0 = PointClass.Point(0, 0)
PointClass.Point.rs = 50
for _ in range(0, 1):
    sensor = []
    target = []
    # df = pd.ExcelFile("/home/toanvd/Documents/run_100/Thaydoisonode.xlsx")
    # # dfs = pd.read_excel("Thaydoisonode.xlsx", sheet_name="20")
    # dfs = df.parse("200")
    # for i in dfs.sensor:
    #     sensor.append(eval(i))
    # for j in dfs.target:
    #     target.append(eval(j))

    # =============================================================================
    with open("data/change_N/50/sensor.txt",'r') as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i)>1]
    for i in _data:
        a = i.split("\t")
        sensor.append((float(a[0]),float(a[1])))

    with open("data/change_N/50/target.txt",'r') as f:
        _data = f.read().split("\n")
    _data = [i for i in _data if len(i)>1]
    for i in _data:
        a = i.split("\t")
        target.append((float(a[0]),float(a[1])))
    # =============================================================================

    np.random.shuffle(sensor)
    np.random.shuffle(target)
    listX = [i[0] for i in target]
    listY = [i[1] for i in target]
    # listX = [25, 80, 55, 70]
    # listY = [35, 80, 40, 40]
    # listX = [55, 80]
    # listY = [40, 40]
    listTargets = []
    for i in range(len(listX)):
        x = listX[i]
        y = listY[i]
        listTargets.append(TSClass.Target(i, x, y))

    # listX = [75, 40, 55, 65, 62.5, 15]
    # listY = [75, 80, 70, 50, 6, 40]
    # listX = [60, 30]
    # listY = [40, 40]
    listX = [i[0] for i in sensor]
    listY = [i[1] for i in sensor]
    listSensors = []
    for i in range(len(listX)):
        x = listX[i]
        y = listY[i]
        listSensors.append(TSClass.Sensor(i, x, y))

    # TSClass.draw_ax(listTargets, listSensors, 'Example')
    # Thêm các target và sensor vào mạng
    WSNs = TVGreedy.TVGreedyWSNs(listTargets, listSensors)
    # print(TVGreedy.main(WSNs))
# =============================================================================
    with open('rs/tv_greedy/change_N/50.txt',"a") as f:
        kq = TVGreedy.main(WSNs)
        print(str(kq))
        f.write(str(kq[0]))
        f.write("\t")
        f.write(str(kq[1]))
        f.write("\n")
# =============================================================================
# tìm cách di chuyển sensor
# total = TVGreedy.main(WSNs)
# print(TVGreedy.main(WSNs))
