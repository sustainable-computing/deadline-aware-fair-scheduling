import util
import aux
import primal
import env
import numpy as np
import sys
import GetTransPower
import RunPF
from tqdm import tqdm

DSSObj, mat, env = util.load(sys.argv)

P = mat['P']  # real power at the secondary nodes in kW
Q = mat['Q']  # reactive power in kVar


#d = env.var['days']-5
d = 0
epsilon = 1e-8
evPower = np.zeros(env.var['evNumber'])
allEVpower = {}
for t in tqdm(range(1000, 1060)):
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
    
    LB = aux.solve(laxity, urgent, 0.8, UB, A, evMatrix)
    x = primal.solve(LB,UB,A,evMatrix)
    for c in range(0, l):
        evPower[connected[c]] = x[c]
    allEVpower[t] = evPower
    print(evPower)
np.save('central', allEVpower)

