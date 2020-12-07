from matplotlib import pyplot as plt
from random import randint

from SweepLineAlgorithm.treeset import TreeSet
from SweepLineAlgorithm.priorityqueue import PriorityQueue

def sweep_line_algorithm(self):
            self.current = Point()

            pointsPQ = PriorityQueue()
            tree = TreeSet()

            pointsPQ.pushAll([seg.p for seg in self.segments])
            pointsPQ.pushAll([seg.q for seg in self.segments])

            res = 0
            #print [str(x) for x in pointsPQ]

            while not pointsPQ.isEmpty():

                self.current.__update__(pointsPQ.pop())

                #print "Round", current

                if self.current.status == 'left':
                    #print "Adding", self.current.segment
                    low, high = tree.add_high_low(self.current.segment)

                    low = tree.lower(self.current.segment)
                    high = tree.higher(self.current.segment)
                    #print "Actual:", self.current.segment
                    #print "Low:", low, self.current.segment.intersect(low) if low else False
                    #print "High:", high, self.current.segment.intersect(high) if high else False

                    if low:
                        if self.current.segment.intersect(low):
                            a = self.current.segment.intersection_point(low)
                            #print "Adding a:", a, self.current.segment, low
                            pointsPQ.push(a)

                    if high:
                        if self.current.segment.intersect(high):
                            a = self.current.segment.intersection_point(high)
                            #print "Adding 2:", a, self.current.segment, high
                            pointsPQ.push(a)

                elif self.current.status == "right":
                    low = tree.lower(self.current.segment)
                    high = tree.higher(self.current.segment)

                    if low and high:
                        if low.intersect(high):
                            a = low.intersection_point(high)
                            #print "Adding 3:", a, low, high
                            pointsPQ.push(a)

                    tree.remove(self.current.segment)
                    #print "Removing", self.current.segment

                elif self.current.status == "int":
                    # exchange the position in tree of the two segments intersecting in current
                    s1, s2 = self.current.segment
                    #print "Between, swapping:", str(s1), str(s2)

                    tree.swap(s1, s2)

                    #print "After swap:", s1, s2, s1 is tree.lower(s2), s2 is tree.lower(s1)
                    #print "Modifying segments starts"
                    old_s1 = s1.p.node
                    old_s2 = s2.p.node

                    s1.set_p_node(self.current.node)
                    s2.set_p_node(self.current.node)

                    #print "Tree after modification:", [str(x) for x in tree]

                    # s1
                    if s1 is tree.lower(s2):
                        #print "... s1, s2, ..."

                        low = tree.lower(s1)
                        #print "s1:", s1, "low:", low, s1.intersect(low) if low else False

                        if low is not None:
                            if s1.intersect(low):
                                pointsPQ.push(s1.intersection_point(low))

                        high = tree.higher(s2)
                        #print "s2:", s2, "high:", high, s2.intersect(high) if high else False

                        if high is not None:
                            if s2.intersect(high):
                                pointsPQ.push(s2.intersection_point(high))

                    elif s2 is tree.lower(s1):
                        #print "... s2, s1, ..."

                        high = tree.higher(s1)
                        #print "s1:", s1, "high:", high, s1.intersect(high) if high else False

                        if high is not None:
                            if s1.intersect(high):
                                pointsPQ.push(s1.intersection_point(high))

                        low = tree.lower(s2)
                        #print "s2:", s2, "low:", low, s2.intersect(low) if low else False

                        if low is not None:
                            if s2.intersect(low):
                                pointsPQ.push(s2.intersection_point(low))

                    else:
                        print("Error") #raise SweepPlaneException("Intersection point error!")
                    res += 1

                    s1.set_p_node(old_s1)
                    s2.set_p_node(old_s2)

                else:
                    print("Error 2") #raise SweepPlaneException("Node without status!")
                #print "Tree", [str(x) for x in tree]
                #print ""
            self.nodes = self.nodes[:self.original_n_nodes]
            return res



def random_line_generator(n=10):
    with open('points.txt','w+') as f:        
        coordinates = [[randint(0, n), randint(0, n)] for _ in range(n)]   
        print(coordinates)             
        return coordinates
                
def plot_lines(coordinates):
    
    for i in range(0,len(coordinates),2):
        plt.plot(coordinates[i],coordinates[i+1],color='black')
    plt.ylabel('y axis')
    plt.xlabel('x axis')
    plt.savefig('line_fig.png')
        


if __name__ == '__main__':
    
    x = random_line_generator(14)
    plot_lines(x)
    