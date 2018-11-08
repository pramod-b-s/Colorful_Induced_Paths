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
import signal
import sys

from color import colorGraph 
from triangle_free import numTriangles
from subset_test import get_k_combs


def sigint_handler(signal, frame):
    print("\ntotal number of graphs checked = "+str(total_graph_generated))
    print("\ntotal number of graphs matching required conditions = "+str(num_g_till_now))
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, xrange(n, n-r, -1), 1)
    denom = reduce(op.mul, xrange(1, r+1), 1)
    return numer//denom


def is_apt_path(subg,col_map):
	nd_list=subg.nodes()
	# print(nd_list)

	for nd in nd_list:
		flg_list=[k for k in subg.neighbors(nd)]
		flg=len(flg_list)
		if (flg==3):
			break
		else:
			# print("path")
			if(is_colorful(subg, col_map)):
				print("colorful path on chi vertices found")
				return True

	return False


def is_colorful(subg, col_map):
	ndlst=subg.nodes()
	seen_col_list=[]
	for nditr in ndlst:
		if col_map[nditr] not in seen_col_list:
			seen_col_list.append(col_map[nditr])
			continue
		else:
			return False

	return True


def get_chi(g, n):
	gcopy=colorGraph(n) 
	gcopy.graph=g 
	
	for i in range(2,n):
		# print(i)
		chiListret=gcopy.graphColouring(i)
		chiObtainedret=max(chiListret)
		# print("tried coloring with colors = "+str(i))
		if (chiObtainedret==0):
			continue
		else:
			break

	return chiListret


def get_chi_list(g, n, m):
	gcopy=colorGraph(n) 
	gcopy.graph=g 
	chiListret=gcopy.graphColouring(m)
	
	return chiListret


def get_color_map(chiListret):
	col_map_ret=[]
	colors_list=['b','g','r','m','w','c','y','k']
	
	for ele in chiListret:
		col_map_ret.append(colors_list[ele-1])

	return col_map_ret


dirname="op"
plotdirname="plots"
csvname="my_graphs.csv"

plotpath=os.path.join(dirname,plotdirname)
csvpath=os.path.join(dirname,csvname)

if not os.path.exists(dirname): 
	os.makedirs(dirname)
	os.makedirs(plotpath)

# n=random.randint(10,50)
# lwr=n
# upr=n*(n-1)/2
# m=random.randint(lwr,upr)

# n=7
# m=11
# probability of there being edge b/w v,u : set to 0.5 for conected graph
p=0.5

chi=5
girth=4

itr=0
tr=0

nlow=2
nhigh=50

num_g_till_now=0
num_g_total=1
total_graph_generated=0

## available colors
# b: blue
# g: green
# r: red
# c: cyan
# m: magenta
# y: yellow
# k: black
# w: white

for vertice_iterator in range(nlow,nhigh):

	mlow=vertice_iterator
	mhigh=vertice_iterator*(vertice_iterator-1)/2

	for edge_iterator in range(mlow,mhigh):
		n=vertice_iterator
		m=edge_iterator

		itr=0
		# num_g=ncr(mhigh,m)
		num_g=50
		
		print("\nnumber of vertices : "+str(n)+"\tnumber of edges : "+str(m)+"\n")

		while itr<num_g:
			itr=itr+1
			print("graph "+str(itr)+" generated with (n, m)\t"+str(n)+"\t"+str(m))
			total_graph_generated=total_graph_generated+1
			
			graph = nx.gnm_random_graph(n, m, seed=None, directed=False)
			# graph=nx.fast_gnp_random_graph(n, p, seed=None, directed=False)

			gnp=nx.to_numpy_matrix(graph,dtype="int")
			g=np.ndarray.tolist(gnp)

			conn=nx.is_connected(graph)
			if (conn==False):
				print("not connected")
				continue

			tr=numTriangles(g)
			len_trlist=len(tr)

			if(len_trlist):
				print("graph has triangles")
				# print(tr)
				graph.remove_edges_from(tr)
				
				gnp=nx.to_numpy_matrix(graph,dtype="int")
				g=np.ndarray.tolist(gnp)
				
				tr1=numTriangles(g)
				# print(tr1)
				len_trlist=len(tr1)
				if(len_trlist==0):
					print("triangles removed from graph")
				else:
					continue

			if(nx.is_connected(graph)==False):
				print("removing triangles causes disconnection!")
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

			
			chiList=get_chi(g,n)
			chiObtained=max(chiList)
			print("chromatic number of graph is "+str(chiObtained))
			
			# nx.draw(graph, node_color=chiList, with_labels=True)
			# plt.show()

			if(chi==chiObtained):
				print("CONDITIONS SATISFIED !!!")
			else:
				print("chromatic number doesn't match, doing mycielskian construction")
				
				itrns=chi-chiObtained
				myc_g=nx.mycielskian(graph, iterations=itrns)
				graph=myc_g
				gnp=nx.to_numpy_matrix(graph,dtype="int")
				g=np.ndarray.tolist(gnp)

				n=graph.number_of_nodes()
				chiList=get_chi_list(g,n,chi)
				chiObtained=max(chiList)
				print("chromatic number of graph now is "+str(chiObtained))


			# print(chiList)
			color_map=get_color_map(chiList)

			# nodes_list=graph.nodes()
			# print(nodes_list)
			# print(n)
			nodes_list=list(range(n))
			# print(nodes_list)
			all_k_ele_list=get_k_combs(nodes_list, chi)

			hyp_truth=0

			for k_list in all_k_ele_list:
				subg=graph.subgraph(k_list)
				sub_conn=nx.is_connected(subg)
				if (sub_conn==False):
					continue
				if(subg.number_of_edges()!=chi):
					continue
				if (is_apt_path(subg,color_map)):
					print("colorful path found")
					hyp_truth=1
					break


			if(hyp_truth==0):
				print("counter-example found")
				nx.draw(graph, node_color=color_map, with_labels=True)
				plt.savefig("counterexample"+str(num_g_till_now))

				exit(0)


			print("optimising graph for clear figure")
			edge_list=graph.edges()
			print(edge_list)

			ind_set_list=[]

			for lbl in range(1,chi+1):
				indset_tmp_list=[]

				for idx,val in enumerate(chiList):
					if (val==lbl):
						indset_tmp_list.append(idx)

				ind_set_list.append(indset_tmp_list)

			print(ind_set_list)
			
			tmpgrth=[]
			tmpgrth.append(girthCycle)
			
			edges = [zip(nodes,(nodes[1:]+nodes[:1])) for nodes in tmpgrth]
			edgesmod=edges[0]
			nec_edges=[]
			for edgsmp in edgesmod:
				lstedg=list(edgsmp)
				lstedg.sort()
				tpledg=tuple(lstedg)
				nec_edges.append(tpledg)

			# for u in range(0,len(ind_set_list)):
			# 	for v in range(u+1,len(ind_set_list)):
			# 		edgsmp=(u,v)
			# 		lstedg=list(edgsmp)
			# 		lstedg.sort()
			# 		tpledg=tuple(lstedg)
			# 		nec_edges.append(tpledg)

			# print(nec_edges)

			# edge_list=graph.edges()
			# print(edge_list)

			# for edg in list(edge_list):
			# 	if edg not in nec_edges:
			# 		graph.remove_edge(*edg)

			# gnpmod=nx.to_numpy_matrix(graph,dtype="int")
			# gmod=np.ndarray.tolist(gnpmod)		

			# chiListMod=get_chi(gmod,n)
			# print(chiListMod)
			# chiObtainedMod=max(chiListMod)
			# print(chiObtainedMod)

			# edge_list=graph.edges()
			# print(edge_list)

			# for edg in list(edge_list):
			# 	if edg in nec_edges:
			# 		continue
			# 	mod_graph=graph
			# 	mod_graph.remove_edge(*edg)
			# 	u=edg[0]
			# 	v=edg[1]
			# 	ulbl=chiList[u]
			# 	vlbl=chiList[v]
			# 	flagis=0
			# 	# print(ind_set_list[ulbl-1])
			# 	for uvert in ind_set_list[ulbl-1]:
			# 		if (flagis==1):
			# 			break
			# 		for vvert in ind_set_list[vlbl-1]:
			# 			if mod_graph.has_edge(uvert,vvert):
			# 				flagis=1
			# 				graph=mod_graph
			# 				# print("removed edge "+str(edg))
			# 				break
			# 			else:
			# 				continue


			# for edg in edge_list:
			# 	print("considering edge "+str(edg))
			# 	mod_graph=graph
			# 	mod_graph.remove_edge(*edg)

			# 	gnpmod=nx.to_numpy_matrix(mod_graph,dtype="int")
			# 	gmod=np.ndarray.tolist(gnpmod)

			# 	cycl_list_mod=nx.cycle_basis(mod_graph, 0)

			# 	if(len(cycl_list_mod)):
			# 		girthObtainedMod=len(min(cycl_list_mod, key=len))
			# 		girthCycleMod=min(cycl_list_mod, key=len)
			# 	else:
			# 		continue

			# 	if (girthObtainedMod!=girth):
			# 		continue
			# 	else:
			# 		print("girth not violated")
			# 		chiListMod=get_chi(gmod,n)
			# 		print(chiListMod)
			# 		chiObtainedMod=max(chiListMod)
			# 		print(chiObtainedMod)
			# 		# if (chiObtainedMod==0):
			# 		# 	continue

			# 		if(chiObtainedMod!=chi):
			# 			continue
			# 		else:
			# 			print("chi not violated")
			# 			print("removed edge "+str(edg))
			# 			graph=mod_graph


			gnp=nx.to_numpy_matrix(graph,dtype="int")
			g=np.ndarray.tolist(gnp)			

			print("graph "+str(num_g_till_now+1)+" generated")
			print(gnp)

			df = pd.DataFrame(data=gnp.astype(np.int))

			with open(csvpath, 'a') as f:
			    df.to_csv(f, header=False)

## TO SOLVE : COMPROMISE BETWEEN COLORED NODES AND FINDING COLOR LIST FOR CHI 5

			gpos = nx.nx_agraph.graphviz_layout(graph, prog='neato')
			# nx.draw_networkx(graph,pos=gpos) 

			sprpos=nx.spring_layout(graph,k=0.1,iterations=50)

			nx.draw(graph,pos=gpos, node_color=color_map, with_labels=True)
			# nx.draw(graph,pos=sprpos, node_color=color_map, with_labels=True)

			# plt.show()
			# plt.savefig("output30/plots/"+"_n_"+str(n)+"_m_"+str(m)+"_chi_"+str(chi)+"_g_"+str(girth)+".jpg")
			plt.savefig(os.path.join(plotpath,str(num_g_till_now)))
			plt.clf()

			num_g_till_now=num_g_till_now+1

			if(num_g_till_now==num_g_total):
				print(str(num_g_total)+" graphs generated\n")
				exit(0)
		

