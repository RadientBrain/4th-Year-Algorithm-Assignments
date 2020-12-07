from Q2 import ConvexHull
import cv2
import numpy as np
import matplotlib.pyplot as plt

def getCavity(concave_bp):
  ch = ConvexHull()
  ch.fit(concave_bp)
  convex_bp = ch.boundary_points_
  for i in range(len(concave_bp)):
    if np.all(convex_bp[0]==concave_bp[i]):
      init_indx = i
      break
  cavities = []
  cavityFound = False
  i = 0
  for j in range(len(concave_bp)):
    if np.all(convex_bp[i] == concave_bp[(init_indx + j)%len(concave_bp)]):
      i+= 1
      if cavityFound == True:
        cavityFound = False
        cavity.append(convex_bp[i-1])
        cavities.append(cavity)
    elif cavityFound == True:
      cavity.append(concave_bp[(init_indx + j)%len(concave_bp)])
    else:
      cavityFound = True
      cavity = [convex_bp[i-1], concave_bp[(init_indx + j)%len(concave_bp)]]
  return cavities
  
def plotCavity(concave_bp, cavities, name):
  plt.plot(np.append(concave_bp[:, 0], concave_bp[0, 0]),
           np.append(concave_bp[:, 1], concave_bp[0, 1]),
           label='Concave Boundary')
  i = 1
  for cavity in cavities:
    cavity = np.array(cavity)
    plt.plot(np.append(cavity[:, 0], cavity[0, 0]),
             np.append(cavity[:, 1], cavity[0, 1]),
             linestyle = ':', label =f'Cavity {i}')
    i+=1
  plt.legend()
  plt.savefig(name)
  plt.show()


image = 'Concave Hexagon.jpg'
image = cv2.imread(image)
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
y, x = np.where(grayImage <125)
y = abs(y-grayImage.shape[0])

f = open("pointsQ3.txt", "w")
for pointx, pointy in zip(x,y):
  f.write(str(pointx)+","+str(pointy)+"\n")
f.close()

l1 = []
file1 = open('pointsQ3.txt', 'r') 
Lines1 = file1.readlines()
for line in Lines1:
  line = line.split(",")
  a = int(line[0])
  b = int(line[1])
  l1.append([a,b])
file1.close()

points = np.array(l1)
plotCavity(points, getCavity(points), "output_fig_Q3.png")
