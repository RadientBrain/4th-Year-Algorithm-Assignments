import matplotlib.pyplot as plt
from random import randint
import math



class RangeRegion:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top



def isInsideRange(reg1, reg2):
    return  ((reg2.left < reg1.left <= reg2.right) and (reg2.left < reg1.right <= reg2.right) and \
            (reg2.bottom < reg1.bottom <= reg2.bottom) and (reg2.bottom < reg1.top <= reg2.top))
      

def doesRegionIntersect(reg1, reg2):
    return not ((reg1.right < reg2.left or reg2.right < reg1.left) or (reg1.top < reg1.bottom or reg2.top < reg1.bottom))


def isInRegion(point, reg):
    return  ((reg.left < point[0] <= reg.right) and (reg.bottom < point[1] <= reg.top)) 




class TREE:
    def __init__(self, point, left=None, right=None, querybox=None):
        self.point = point
        self.left = left
        self.right = right
        self.querybox = querybox



def reportSubTree(node):
    points = []
    node_list = [node]
    while len(node_list) > 0:
        ptr = node_list.pop()
        if (ptr.left is None) and (ptr.right is None):
            points.append(ptr.point)
        node_list.append(ptr.right)
        node_list.append(ptr.left)

    return points


def buildKdTree(pointsSortedByX, pointsSortedByY, depth, querybox):

    if len(pointsSortedByX) == 0:
        return None
    elif len(pointsSortedByX) == 1:
        return TREE(pointsSortedByX[0], querybox=querybox)

    else:

        # for even number of points
        if depth % 2 == 1:
            median_index = math.ceil(len(pointsSortedByX)/2) - 1
            median_point = pointsSortedByX[median_index]

            P1SortedByX = []
            P2SortedByX = []
            for p in pointsSortedByX:
                if p[0]<=median_point[0]:
                    P1SortedByX.append(p)
                else:
                    P2SortedByX.append(p)

            P1SortedByY = []
            P2SortedByY = []
            for p in pointsSortedByY:
                if p[0]<=median_point[0]:
                    P1SortedByY.append(p)
                else:
                    P2SortedByY.append(p)

            region_l = RangeRegion(querybox.left, querybox.bottom, median_point[0], querybox.top)
            region_r = RangeRegion(median_point[0], querybox.bottom, querybox.right, querybox.top)

        # for odd number of points
        else:
            median_index = math.ceil(len(pointsSortedByY)/2) - 1
            median_point = pointsSortedByY[median_index]

            P1SortedByY = []
            P2SortedByY = []
            for p in pointsSortedByY:
                if p[1]<=median_point[1]:
                    P1SortedByY.append(p)
                else:
                    P2SortedByY.append(p)

            P1SortedByX = []
            P2SortedByX = []
            for p in pointsSortedByX:
                if p[1]<=median_point[1]:
                    P1SortedByX.append(p)
                else:
                    P2SortedByX.append(p)

            region_l = RangeRegion(querybox.left, querybox.bottom, querybox.right, median_point[1])
            region_r = RangeRegion(querybox.left, median_point[1], querybox.right, querybox.top)



        v_left  = buildKdTree(P1SortedByX, P1SortedByY, depth+1, region_l)
        v_right = buildKdTree(P2SortedByX, P2SortedByY, depth+1, region_r)

        return TREE(median_point, v_left, v_right, querybox)


def searchKdTree(node, querybox):
    if node.left is None and node.right is None:
        if isInRegion(node.point, querybox):
            return [node.point]

    else:
        result_points = []

        if (node.left is not None):
            if isInsideRange(node.left.querybox, querybox):
                res = reportSubTree(node.left)
                if res is not None:
                    result_points += res
            elif doesRegionIntersect(node.left.querybox, querybox):
                res = searchKdTree(node.left, querybox)
                if res is not None:
                    result_points += res

        if (node.right is not None):
            if isInsideRange(node.right.querybox, querybox):
                res = reportSubTree(node.right)
                if res is not None:
                    result_points += res

            elif doesRegionIntersect(node.right.querybox, querybox):
                res = searchKdTree(node.right, querybox)
                if res is not None:
                    result_points += res

        return result_points


def generateRandomPoints(n, limit):
    return [(randint(-limit, limit), randint(-limit, limit)) for _ in range(n)]


def plotPoints(points):
    X = [p[0] for p in points]
    Y = [p[1] for p in points]
    plt.scatter(X, Y)


def plotBox(querybox):
    plt.plot([querybox.left, querybox.right, querybox.right, querybox.left, querybox.left], 
                [querybox.bottom, querybox.bottom, querybox.top, querybox.top, querybox.bottom],'r--')



if __name__ == "__main__":
    MAX_RANGE = 100

    points = generateRandomPoints(50, MAX_RANGE)
    plotPoints(points)

    pointsSortedByX = sorted(points, key=lambda p: p[0])
    pointsSortedByY = sorted(points, key=lambda p: p[1])

    root = buildKdTree(pointsSortedByX, pointsSortedByY, 1, RangeRegion(-MAX_RANGE, -MAX_RANGE, MAX_RANGE, MAX_RANGE))


    left = randint(-MAX_RANGE, 0)
    right = randint(left, MAX_RANGE)
    bottom = randint(-MAX_RANGE, 0)
    top = randint(bottom, MAX_RANGE)

    querybox = RangeRegion(left, bottom, right, top)

    result = searchKdTree(root, querybox)
    # we can print the resultant tree
    # print(result)

    plotPoints(result)
    plotBox(querybox)

    plt.savefig('2d-Range_Search.png')
    plt.show()