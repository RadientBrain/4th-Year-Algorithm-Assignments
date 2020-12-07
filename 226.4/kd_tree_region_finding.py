import matplotlib.pyplot as plt
from random import randint
import math



class TreeNode:
    def __init__(self, point, left=None, right=None, region=None):
        self.point = point
        self.left = left
        self.right = right
        self.region = region


class QueryBox:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top



def region_contains(reg1, reg2):
    return  ((reg2.left < reg1.left <= reg2.right) and (reg2.left < reg1.right <= reg2.right) and \
            (reg2.bottom < reg1.bottom <= reg2.bottom) and (reg2.bottom < reg1.top <= reg2.top))

    
def region_intersects(reg1, reg2):
    return not ((reg1.right < reg2.left or reg2.right < reg1.left) or (reg1.top < reg1.bottom or reg2.top < reg1.bottom))


def region_has_point(point, reg):
    return  ((reg.left < point[0] <= reg.right) and (reg.bottom < point[1] <= reg.top)) 




def report_subtree(node):
    points = []

    stack = [node]
    while len(stack) > 0:
        ptr = stack.pop()
        if (ptr.left is None) and (ptr.right is None):
            points.append(ptr.point)
        stack.append(ptr.right)
        stack.append(ptr.left)

    return points


def build_KD_Tree(pointsSortedByX, pointsSortedByY, depth, region):

    if len(pointsSortedByX) == 0:
        return None
    elif len(pointsSortedByX) == 1:
        return TreeNode(pointsSortedByX[0], region=region)

    else:

        # even
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

            region_l = QueryBox(region.left, region.bottom, median_point[0], region.top)
            region_r = QueryBox(median_point[0], region.bottom, region.right, region.top)

        # odd
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

            region_l = QueryBox(region.left, region.bottom, region.right, median_point[1])
            region_r = QueryBox(region.left, median_point[1], region.right, region.top)



        v_left  = build_KD_Tree(P1SortedByX, P1SortedByY, depth+1, region_l)
        v_right = build_KD_Tree(P2SortedByX, P2SortedByY, depth+1, region_r)

        return TreeNode(median_point, v_left, v_right, region)


def search_KD_Tree(node, querybox):
    if node.left is None and node.right is None:
        if region_has_point(node.point, querybox):
            return [node.point]

    else:
        result_points = []

        if (node.left is not None):
            if region_contains(node.left.region, querybox):
                res = report_subtree(node.left)
                if res is not None:
                    result_points += res
            elif region_intersects(node.left.region, querybox):
                res = search_KD_Tree(node.left, querybox)
                if res is not None:
                    result_points += res

        if (node.right is not None):
            if region_contains(node.right.region, querybox):
                res = report_subtree(node.right)
                if res is not None:
                    result_points += res

            elif region_intersects(node.right.region, querybox):
                res = search_KD_Tree(node.right, querybox)
                if res is not None:
                    result_points += res

        return result_points






def plot_points(points):
    X = [p[0] for p in points]
    Y = [p[1] for p in points]
    plt.scatter(X, Y)


def plot_box(box, **kwargs):
    plt.plot([box.left, box.right, box.right, box.left, box.left], 
                [box.bottom, box.bottom, box.top, box.top, box.bottom], **kwargs)


def plot_regions(node):
    if (node is not None) and  (node.region is not None):
        plot_box(node.region, color="blue", alpha=0.1, linewidth=1)
        plot_regions(node.left)
        plot_regions(node.right)


def random_points(n, max_points):
    return [(randint(-max_points, max_points), randint(-max_points, max_points)) for _ in range(n)]





if __name__ == "__main__":
    MAX_RANGE = 100

    points = random_points(20, MAX_RANGE)
    plot_points(points)
    plt.show()

    pointsSortedByX = sorted(points, key=lambda p: p[0])
    pointsSortedByY = sorted(points, key=lambda p: p[1])

    root = build_KD_Tree(pointsSortedByX, pointsSortedByY, 1, QueryBox(-MAX_RANGE, -MAX_RANGE, MAX_RANGE, MAX_RANGE))


    left = randint(-MAX_RANGE, 0)
    right = randint(left, MAX_RANGE)
    bottom = randint(-MAX_RANGE, 0)
    top = randint(bottom, MAX_RANGE)

    querybox = QueryBox(left, bottom, right, top)

    #plot_points(points)    
    #plot_regions(root)
    #plt.show()

    result = search_KD_Tree(root, querybox)
    

    plot_points(points)
    plot_regions(root)    
    plot_points(result)
    plot_box(querybox, color="red")
    plt.show()

    #plt.show()
