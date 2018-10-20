"""
Sevval Boylu-20530
CS404 Homework-1 / Bloxorz game solver with A* algorithm
"""
import time
from math import sqrt
class Node:
    def __init__(self, x1, y1, x2=None, y2=None, parent=None):
        self.orientation = None
        self.coordinates = [(x1, y1)]
        if parent is not None:
            self.parent = parent
            self.cost = parent.cost + 1
        else:
            self.cost = 0

        if x1 is not None and y2 is not None:
            self.coordinates.append((x2, y2))
        else:
            self.orientation = "Standing"
        if x1 == x2:
            self.orientation = "Vertical"
        elif y1 == y2:
            self.orientation = "Horizontal"

    def setParent(self, parent, cost):
        self.parent = parent
        self.cost = cost

    def setCost(self, cost):
        self.cost = cost


def addToQueue(queue, item):
    """
    :param queue: the frontier, as a list object
    :param item: item to be inserted, (cost,node) tuple
    :return: queue
    """
    length = queue.__len__()
    if length > 0:
        min_ = queue[0]
        max_ = queue[length-1]
        if item[0] < min_[0]:
            queue.insert(0, item)  # not so sure
        elif item[0] > max_[0]:
            queue.append(item)
        else:
            index_ = 0
            for x in queue:
                if x[0] < item[0]:
                    index_ = index_ + 1
            queue.insert(index_, item)
    else:
        queue.append(item)


def in_array(item, array):
    for x in array:
        if x[1] == item:
            return x
    return None


def get_neighbors(graph, coords):
    if coords.__len__() is 1:  # standing
        x = coords[0][0]
        y = coords[0][1]
        neighbors = [Node(x, y-2, x, y-1),
                     Node(x, y+1, x, y+2),
                     Node(x-2, y, x-1, y),
                     Node(x+1, y, x+2, y)]
        for item in neighbors:
            for crd in item.coordinates:
                x = crd[0]
                y = crd[1]
                try:
                    if graph[x][y] is "X":
                        neighbors.remove(item)
                        break
                except Exception as e:  # meaning that the coordinates are out of bounds
                    neighbors.remove(item)
                    break
        return neighbors

    else:
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        if x1 == x2:  # vertical flat
            neighbors = [Node(x1, y1-1),
                         Node(x1, y2 + 1),
                         Node(x1 - 1, y1, x2 - 1, y2),
                         Node(x1 + 1, y1, x2 + 1, y2)]
            for item in neighbors:
                for crd in item.coordinates:
                    x = crd[0]
                    y = crd[1]
                    try:
                        if graph[x][y] is "X":
                            neighbors.remove(item)
                            break
                    except Exception as e:  # meaning that the coordinates are out of bounds
                        neighbors.remove(item)
                        break
            return neighbors

        elif y1 == y2:  # horizontal flat
            neighbors = [Node(x1, y1 - 1,x2, y2 - 1),
                         Node(x1, y1 + 1,x2, y2 + 1),
                         Node(x1 - 1, y1),
                         Node(x2 + 1, y2)]
            for item in neighbors:
                for crd in item.coordinates:
                    x = crd[0]
                    y = crd[1]
                    try:
                        if graph[x][y] is "X":
                            neighbors.remove(item)
                            break
                    except Exception as e:  # meaning that the coordinates are out of bounds
                        neighbors.remove(item)
                        break
            return neighbors


def heuristic(node, goal):
    coords = node.coordinates
    goal_c = goal.coordinates

    if coords.__len__() is 2:
        x = (coords[0][0]+coords[1][0])/2
        y = (coords[0][1]+coords[1][1])/2
    else:
        x = coords[0][0]
        y = coords[0][1]

    dist = sqrt( (x-goal_c[0][0])*(x-goal_c[0][0]) + (y-goal_c[0][1])*(y-goal_c[0][1]))

    return dist


def aStar(graph, start, goal):
    """
    :param graph: The game board, represented by a matrix
    :param start: Initial position of the block
    :param goal: The goal position
    :return: the path
    """
    start_time = time.time()  # for running time measuring
    frontier = [(0,start)]  # priority,node
    closed = []

    while not frontier.__len__() == 0:
        weight, node = frontier.pop(0)

        if node.coordinates == goal.coordinates:
            print("--- %s seconds ---" % (time.time() - start_time))
            return node

        succ = get_neighbors(graph, node.coordinates)
        for item in succ:
            cost = node.cost + 1 + heuristic(node, goal)  # g(x) = parent's cost+1
            item.setParent(node, cost)

            f = in_array(item, frontier)
            c = in_array(item, closed)

            if f is None and c is None:
                addToQueue(frontier, (cost, item))

            elif f is not None and f[0] > cost:
                index = frontier.index(f)
                frontier[index] = (cost, item)

            elif c is not None and c[0] > cost:
                closed.remove(c)
                addToQueue(frontier, item)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("No possible path")
    return None


if __name__ == '__main__':

    filename = input("Please enter the filename for the game board: ")
    f = open(filename, mode='r')

    Graph = []
    start_coord = []
    goal_coord = []

    i = 0

    for line in iter(f.readline, ''):
        line.replace('\n','')
        w = line.__len__()
        s = list(line[0:w])
        if 'S' in s:
            index = s.index('S')
            start_coord.append((i, index))
            if 'S' in s[index+1:]:
                index2 = s.index('S', index+1)
                start_coord.append((i, index2))
        elif 'G' in s:
            indexG = s.index('G')
            goal_coord.append((i, indexG))
        Graph.append(s)
        i = i + 1

    f.close()

    if start_coord.__len__() is 1:
        start_node = Node(start_coord[0][0], start_coord[0][1])
    else:
        start_node = Node(start_coord[0][0], start_coord[0][1], start_coord[1][0], start_coord[1][1])

    goal_node = Node(goal_coord[0][0], goal_coord[0][1])
    print("Start: ", start_coord, "\nGoal: ", goal_coord)

    final = aStar(Graph, start_node, goal_node)

    # Display the path
    path = []
    node = final
    while node.cost is not 0:
        path.append(node.coordinates)
        if node.cost is not 0:
            node = node.parent
    path.append(node.coordinates)

    path.reverse()
    print("Path: ", path)