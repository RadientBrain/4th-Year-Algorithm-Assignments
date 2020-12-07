import cv2
import numpy as np
import matplotlib.pyplot as plt

class ConvexHull:
  def __init__(self):
    pass
  def show(self):
    print('Something')

  def fit(self, X, Y=None, strategy='graham'):
    if Y is not None:
      self.X = np.array(X)
      self.Y = np.array(Y)
    else:
      self.X = np.array(X).reshape(-1, 2)[:, 0]
      self.Y = np.array(X).reshape(-1, 2)[:, 1]
    if strategy == 'graham':
      self.graham_scan()
    else:
      self.bruteforce()

  def plot_points(self, name):
    import matplotlib.pyplot as plt
    plt.scatter(x=self.X, y=self.Y, label='Points')
    boundary_x = np.append(self.boundary_points_[:, 0], self.boundary_points_[0, 0])
    boundary_y = np.append(self.boundary_points_[:, 1], self.boundary_points_[0, 1])
    plt.plot(boundary_x, boundary_y, color='g', label='boundary')
    plt.legend()
    plt.savefig(name) 
    plt.show()
    plt.pause(5)
    plt.close()


  def bruteforce():
      pass
    

  def graham_scan(self):
    init_point_ = np.array([ self.X[np.argmin(self.Y)], np.min(self.Y) ])
    other_points = [ np.array([x, y]) for x, y in zip(self.X, self.Y) if not np.all(init_point_ == (x, y))]
    other_points = np.array(other_points).reshape(-1, 2)
    
    angles_ = [ self.angle_bw_points(init_point_, point) for point in other_points ]

    indx = np.lexsort((other_points[:, 1], other_points[:, 0], angles_))
    other_points = other_points[indx]

    self.boundary_points_ = np.array([init_point_, other_points[0]])
    self.inner_points_ = np.array([])
    for point in other_points[1:]:
      while( self.turn_bw_points2(self.boundary_points_[-2], self.boundary_points_[-1], point) > 0):
        self.inner_points_ = np.append(self.inner_points_, self.boundary_points_[-1])
        self.boundary_points_ = self.boundary_points_[:-1]
      self.boundary_points_ = np.append(self.boundary_points_, point.reshape(-1, 2), axis=0)

  def angle_bw_points(self, a, b):
    delta_y = b[1] - a[1]
    delta_x = b[0] - a[0]
    angle = np.arctan2(delta_y,delta_x)
    return np.rad2deg(angle)
  def turn_bw_points2(self, a, b, c):
    area = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
    if area > 0:
      return 1
    elif area < 0:
      return -1
    else:
      return 0
  def turn_bw_points(self, a, b):
    det = a[0]*b[1] - b[0]*a[1]
    if det<0:
      return -1
    else:
      return 1

image = 'Beng-5.png'
image = cv2.imread(image)
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
y, x = np.where(grayImage <125)
y = abs(y-grayImage.shape[0])

f = open("pointsQ2.txt", "w")
for pointx, pointy in zip(x,y):
  f.write(str(pointx)+","+str(pointy)+"\n")
f.close()

#list = []

#f = open("pointsQ2.txt", "r")

#from Q1 import Convex_hull_through_graham

ch = ConvexHull()
ch.fit(list(zip(x, y)))
ch.plot_points("output_fig_Q2.png")
