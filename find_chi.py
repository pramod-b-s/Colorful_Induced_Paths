
def isSafe(g, v, colour, c, n): 
    for i in range(0,n):
    	#(g[v][i]) and 
        if ( (colour[i]==c) ): 
            return False
    return True
  

def graphColourUtil(g, m, colour, v, n): 
    if v == n-1: 
        return True

    for c in range(1, m+1): 
        if isSafe(g, v, colour, c, n) == True: 
            colour[v] = c 
            if graphColourUtil(g, m, colour, v+1, n) == True: 
                return True
            colour[v] = 0


def graphColouring(g, m, n): 
    colour = [0] * n 
    if graphColourUtil(g, m, colour, 0, n) == False: 
        return 0

    # print("Solution exist and Following are the assigned colours:")
    # for c in colour: 
    #     print(c) 
    return max(colour)
