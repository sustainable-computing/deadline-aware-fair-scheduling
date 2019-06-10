import numpy as np
import util
import aux
import primal
import env
import sys
import GetTransPower
import RunPF
from tqdm import tqdm

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
    
if __name__=="__main__":
    DSSObj, mat, env = util.load(sys.argv)

    P = mat['P']  # real power at the secondary nodes in kW
    Q = mat['Q']  # reactive power in kVar

    #d = env.var['days']-5
    d = 0
    epsilon = 1e-8
    evPower = np.zeros(env.var['evNumber'])
    allEVpower = {}
    for t in tqdm(range(0, 60)):
        # Performing load flow for the first time step
        DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], env.var['evNodeNumber'], 0*evPower)

        # get the transformer power magnitudes
        transPowers = GetTransPower.getTransPower(DSSCircuit)
        
        transPowers = np.ravel(transPowers)
        
        # Available Capacity: 
        A = [env.var['transRating'][i//2] - np.sqrt(transPowers[i]*transPowers[i]+transPowers[i+1]*transPowers[i+1]) for i in range(0,len(transPowers),2)]
        A = np.maximum(0.0, np.ravel(A))

        connected, urgent, laxity, evMatrix = env.update(d,t,evPower)
        evPower*=0
        l = len(connected)
        if l==0:
            continue
        # Upper Bound:
        UB = np.minimum(env.var['remainingDemand'], env.var['maxRate'])
        UB = np.ravel([UB[c] for c in connected])
        
        x = algo(laxity, A, UB, env.var['evNodeNumber'],env.var['loadPhase'])
        for c in range(0, l):
            evPower[connected[c]] = x[c]
        allEVpower[t]=np.copy(evPower)
    np.save('base', allEVpower)

