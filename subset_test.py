
def getCombinationUtil(arr, n, r, index, data, i, global_list): 
    if(index == r): 
        tmp=[]
        for j in range(r): 
            tmp.append(data[j]) 
        # print(tmp)
        global_list.append(tmp) 
        return
  
    if(i >= n): 
        return
  
    data[index] = arr[i] 
    getCombinationUtil(arr, n, r, index + 1, data, i + 1, global_list) 
      
    getCombinationUtil(arr, n, r, index, data, i + 1, global_list) 
  

def getCombination(arr, n, r, global_list): 
    data = list(range(r)) 
    getCombinationUtil(arr, n, r, 0, data, 0, global_list) 
  
  
def get_k_combs(arr, k): 
    all_subsets_list=[]
    n = len(arr) 
    getCombination(arr, n, k, all_subsets_list) 

    return all_subsets_list