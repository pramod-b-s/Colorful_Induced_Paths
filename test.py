## graph theory testing

import networkx as nx

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import sys
import time
import datetime as dt
import os 
import operator as op

from color import colorGraph 
from triangle_free import numTriangles


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, xrange(n, n-r, -1), 1)
    denom = reduce(op.mul, xrange(1, r+1), 1)
    return numer//denom


if not os.path.exists("output"): 
	os.makedirs("output")
	os.makedirs("output/plots")

# n=random.randint(6,20)
# lwr=n
# upr=n*(n-1)/2
# # m=random.randint(lwr,int(lwr+0.2*upr))
# m=random.randint(lwr,lwr+5)

n=6
m=11
# probability of there being edge b/w v,u : set to 0.5 for conected graph
p=0.2

chi=5
girth=4

itr=0
tr=0
cnt=0
num_g=5


while itr<num_g:
	cnt=cnt+1
	print(str(n)+"\t"+str(m))
	graph = nx.gnm_random_graph(n, m, seed=None, directed=False)
	# graph=nx.fast_gnp_random_graph(n, p, seed=None, directed=False)

	gnp=nx.to_numpy_matrix(graph,dtype="int")
	g=np.ndarray.tolist(gnp)

	print("graph "+str(cnt)+" generated")

	conn=nx.is_connected(graph)
	if (conn==False):
		# continue
		print("not connected")
		continue

	tr=numTriangles(g)

	if(tr):
		print("graph has triangle")
		continue

	cycl_list=nx.cycle_basis(graph, 0)

	if(len(cycl_list)):
		girthObtained=len(min(cycl_list, key=len))
		girthCycle=min(cycl_list, key=len)
		print("girth = "+str(girthObtained))
	else:
		print("no cycles")
		continue


	if (girthObtained!=girth):
		print("girth doesn't match")
		continue
	else:
		print("girth matches")

	gcopy=colorGraph(n) 
	gcopy.graph=g 

	for i in range(2,n):
		chiObtained=gcopy.graphColouring(i)
		
		if (chiObtained):
			break
		else:
			continue

	print("chromatic number of graph is "+str(chiObtained))

	if(chi==chiObtained):
		print("CONDITIONS SATISFIED !!!")
		itr=itr+1
		
		print("graph "+str(itr)+" generated")
		print(gnp)
		
		df = pd.DataFrame(data=gnp.astype(np.int))

		with open("output/my_graphs.csv", 'a') as f:
		    df.to_csv(f, header=False)
		
		nx.draw_networkx(graph,pos=nx.spring_layout(graph)) 
		plt.show()
		plt.savefig("output/plots/"+"graph_"+str(itr)+"_"+str(dt.datetime.now())[:-10]+"_n_"+str(n)+"_m_"+str(m)+".jpg")
		plt.clf()

	else:
		print("unsuitable!")
		continue
		