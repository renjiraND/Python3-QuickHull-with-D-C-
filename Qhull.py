'''	
	Renjira Naufhal Dhiaegana
	13516014
	Teknik Informatika
	Institut Teknologi Bandung
'''


#START OF CODE////////////////////////////////////////////////////////

import copy
import math
import matplotlib.pyplot as plt
import numpy.linalg as nl 
import random
import timeit

# circle radius(for random)
circle_r = 450
# circle center point(x, y)
circle_x,circle_y = 450,450

# initialize needed lists
cvx = []
lx = []
ly = []
ptlist = []

def QuickHull(S):
	# find convex hull from the set S of n points
	# initialize local lists needed

	if(len(S) == 2):
		cvx.append(max(S))
		cvx.append(min(S))
		return;

	cvhull = []
	S1 = []
	S2 = []
	lst = copy.deepcopy(S)
	mx,mi = max(S),min(S)
	cvx.append(max(lst))
	cvx.append(min(lst))

	# append 1 as z for determinant calculation
	mx.append(1)
	mi.append(1)
	cvhull.append(mx)
	cvhull.append(mi)

	# remove min and max element from list of available points
	for elem in cvhull:
		S.remove(elem)
	
	# copy list for 1 as z addition for determinant calculation
	tlist = copy.deepcopy(S);
	for lis in tlist:
		lis.append(1)

	# divide available points into 2 sets for finding hulls
	for elem in tlist:
		# append list atas/kiri
		if(nl.det([mx,mi,elem]) > 0):
			del elem[len(elem)-1]
			S1.append(elem)
		# append list bawah/kanan
		elif(nl.det([mx,mi,elem]) < 0):
			del elem[len(elem)-1]
			S2.append(elem)

	# call findhull
	FindHull(S1, mi, mx) 
	FindHull(S2, mx, mi)


def FindHull (Sk, P, Q):

	# initialize variables needed
	global cvx
	lodist,S1,S2 = [],[],[]

	# recursive function (divide and conquer)
	if(len(Sk) == 0):	# basis
		return;
	else:				# recursion
		# finding point with the largest distance to current line PQ
		for i,[x,y] in enumerate(Sk):
			lodist.append([distanceLtoP(x,y,P,Q),i])

		# append selected point to convex hull list
		C = Sk[max(lodist)[1]]
		cvx.append(C)

		# find set S1&S2 candidate points for hull searching
		findright(P,C,Sk,S1)
		findright(C,Q,Sk,S2)

	# panggil kembali fungsi rekusi hingga menemui basis
	FindHull(S1, P, C) 
	FindHull(S2, C, Q) 

# find points on the right/left side of line function
def findleft(x,y,tlist,S):
	for elem in tlist:
		# append list atas/kiri
		if(det(elem[0],elem[1],x,y) > 0.0):
			S.append(elem)

def findright(x,y,tlist,S):
	for elem in tlist:
		# append list bawah/kanan
		if(det(elem[0],elem[1],x,y) < 0.0):
			S.append(elem)

# distantce from line to point function
def distanceLtoP(x,y,mi,ma):
	return(math.fabs(det(x,y,mi,ma)))

# determinant calculating function
def det(x,y,mi,ma):
	return((mi[0]*ma[1])+(x*mi[1])+(y*ma[0])-
		  (x*ma[1])-(ma[0]*mi[1])-(mi[0]*y))

def randomPoint(N):
	global ptlist
	for i in range(int(N)):
		# random angle
		alpha = 2 * math.pi * random.random()
		# random radius
		r = circle_r * random.random()
		# calculating coordinates
		x = int(r * math.cos(alpha) + circle_x)
		y = int(r * math.sin(alpha) + circle_y)
		if not([x,y] in ptlist):
			ptlist.append([x,y])

def removeDuplicate(cvx):
	for elem in cvx:
		if(cvx.count(elem)>1):
			cvx.remove(elem)


def main():
	# global variables needed
	global ptlist, cvx

	# input N for randomizing points
	N = input("Input jumlah N : ")
	randomPoint(N)

	# plot all randomized points
	for [x,y] in ptlist:
		plt.plot([x], [y], 'r.',lw = 0.1)

	start = timeit.default_timer()
	# call quickhull, remove duplicates if any
	QuickHull(ptlist)
	removeDuplicate(cvx)

	#sort convex hull clockwise
	cvx.sort(key=lambda k: math.atan2(k[0]-circle_x, k[1]-circle_y))
	end = timeit.default_timer()

	# print convex hull points and size
	print("Convex hull points: \n","{ ",cvx," }")
	print("Number of convex hull points: ",len(cvx))
	print("Process time :", round(end-start,5), "second")

	# prepare points for line plotting
	for [x,y] in cvx:
		lx.append(x)
		ly.append(y)
	# append removed duplicate start point(required)
	lx.append(cvx[0][0])
	ly.append(cvx[0][1])

	# plot polygon(with line with 1.5 and orange color)
	plt.plot(lx, ly,lw = 1,c = "orange")
	# plot convex dots for better visualization
	for [x,y] in cvx:
		plt.plot([x], [y], 'b.')

	# title
	plt.suptitle('Quick Hull', fontsize=20, fontweight='bold',family = "Comic Sans MS")

	# ready window, show plots
	plt.axis([0, 1000, 0, 1000])
	plt.show()

# run main
main()
#END OF CODE//////////////////////////////////////////////////////////