# -*- coding: utf-8 -*-
import math
import numpy as np

# =============================================================================
# def insect_points_two_circle(cir1, cir2, R):
#     d = math.sqrt((cir2[0]-cir1[0])**2+(cir2[1]-cir1[1])**2)
#     if d < 2*R:
#         x0 = float(cir2[0]-cir1[0])/R
#         y0 = float(cir2[1]-cir1[1])/R
#         beta1 = math.asin(x0/(x0**2+y0**2)) - 2*math.pi/3
#         beta2 = math.asin(x0/(x0**2+y0**2)) + 2*math.pi/3
#         insect1 = (cir2[0]+R*math.sin(beta1),cir2[1]+R*math.cos(beta1))
#         insect2 = (cir2[0]+R*math.sin(beta2),cir2[1]+R*math.cos(beta2))
#         return [insect1, insect2]
#     elif d == 2*R:
#         return [((cir1[0]+cir2[0])/2,(cir1[1]+cir2[1])/2)]
#     else:
#         return []
#
# =============================================================================


def insect_points_two_circle(cir1, cir2, R):
    x0 = cir1[0]
    y0 = cir1[1]
    x1 = cir2[0]
    y1 = cir2[1]
    r0 = r1 = R
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return []
    # One circle within other
    if d < abs(r0 - r1):
        return []
    # coincident circles
    if d == 0 and r0 == r1:
        return []
    else:
        a = (r0**2 - r1**2 + d**2) / (2 * d)
        h = math.sqrt(r0**2 - a**2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d
        point1 = (x3, y3)
        point2 = (x4, y4)
        if d == R:
            return [point1]
        else:
            return [point1, point2]


def calculate_distance(point1, point2):
    dist = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    return dist


def insect_points(cir, point, R):
    d = math.sqrt((point[0] - cir[0]) ** 2 + (point[1] - cir[1]) ** 2)
    if d > R:
        return [
            (cir[0] + R / d * (point[0] - cir[0]), cir[1] + R / d * (point[1] - cir[1]))
        ]
    else:
        return []


def acceptable_point(sensor, target, R):
    # near_cir = [[] for i in range(target)]
    accept_point = []
    # point_cover_target = [[] for i in range(len(target))]
    for i in range(0, len(target)):
        for j in range(i + 1, len(target)):
            # print(target[i], target[j])
            k = insect_points_two_circle(target[i], target[j], R)
            # print(k)
            # accept_point.extend(k)
            for point in k:
                if (
                    point[0] >= 0
                    and point[0] <= 1000
                    and point[1] >= 0
                    and point[1] <= 1000
                ):
                    accept_point.append(point)
                    # accept_point.extend(k)
                else:
                    continue
            # near_cir[i].append(j)
            # near_cir[j].append(i)
            # point_cover_target[i].extend(k)
            # point_cover_target[j].extend(k)
    # =============================================================================
    #     for i in target:
    #         for j in sensor:
    #             accept_point.extend(insect_points(i, j, R))
    # =============================================================================
    # point_cover_target[i].extend(insect_points(i,j))
    # accept_point.extend(sensor)
    # =============================================================================
    #     for i in range(0,len(target)):
    #         for j in range(0,len(accept_point)):
    #             if calculate_distance(target[i], accept_point[j]) <= R:
    #                 point_cover_target[i].append(accept_point[j])
    #             else:
    #                 pass
    #     return([accept_point, point_cover_target])
    # =============================================================================
    return accept_point


def caculator_point_cover_target(accept_point, target, R):
    point_cover_target = [[] for i in range(len(target))]
    for i in range(0, len(target)):
        for j in range(0, len(accept_point)):
            # print(calculate_distance(target[i], accept_point[j]))
            if calculate_distance(target[i], accept_point[j]) <= (R + 0.001):
                point_cover_target[i].append(accept_point[j])
            else:
                pass
    return point_cover_target


def cost_matrix():
    pass


if __name__ == "__main__":
    target = [(0, 0), (1, 1)]
    sensor = [(3, 3)]
    # =============================================================================
    #     sensor = [(0, 1)]
    #     target = [(2,1)]
    # =============================================================================
    R = 2
    accept_point, point_cover_target = acceptable_point(sensor, target, R)

    # print(insect_points_two_circle((30, 40),(45,40)))
