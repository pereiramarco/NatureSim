import math

def distance_between_points(point1,point2):
    return math.sqrt(pow(point2[0]-point1[0],2) + pow(point2[1]-point1[1],2))

def get_closest_point(goal,points):
    closest = points[0]
    closest_dist = distance_between_points(goal,closest[0])
    for point in points[1:]:
        dist = distance_between_points(goal,point[0])
        if dist<closest_dist:
            closest_dist = dist
            closest = point
    return closest[1]


def lowest_cost(possible_nodes, costs_grid):
    lowest = possible_nodes[0]
    for node in possible_nodes[1:]:
        if costs_grid[node[1]][node[0]][0]<costs_grid[lowest[1]][lowest[0]][0]:
            lowest = node
    return lowest