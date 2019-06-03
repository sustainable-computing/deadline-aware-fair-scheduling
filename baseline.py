import numpy as np

dtype = [('ev', int), ('value', float)]

def sort(value):
    x = [(i,value[i]) for i in range(0,len(value))]
    x = np.array(x, dtype=dtype)
    return np.sort(x, order='value')
    
def algo(value,A,UB,evNode,phase):
    power = np.zeros(len(value))
    B = np.copy(A)
    order = sort(value)
    for i in range(0,len(value)):
        index = order[i][0]
        j=phase[evNode[index]%55]-1
        k=3*(evNode[index]//55+1)+j
        if B[j]>=UB[index] and B[k]>=UB[index]:
            power[index]=UB[index]
        else:
            power[index]=np.minimum(B[j],B[k])
        B[j]-=power[index]
        B[k]-=power[index]
    return power
