def numTriangles(g):
	nodes = len(g) 
	count_Triangle = 0 
	
	ret_list=[]
	tr_list=[]
	tmp_list=[]

	# Consider every possible triplet of edges in graph 
	for i in range(nodes): 
		for j in range(nodes): 
			for k in range(nodes): 
				# check the triplet if it satisfies the condition 
				if( i!=j and i !=k and j !=k and g[i][j] and g[j][k] and g[k][i]): 
					tmp_list=[]
					tmp_list.append(i)
					tmp_list.append(j)
					tmp_list.append(k)
					tmp_list.sort()
					
					t=tuple(tmp_list)
					
					if t not in tr_list:
						tr_list.append(t)
						ret_list.append((i,j))
	# print("tr list")
	# print(tr_list)
	return ret_list