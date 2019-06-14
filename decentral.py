import util
import aux
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
tol=1e-3

maxIteration=2000

gamma1 = 1e-10
gamma2 = 1e-10
theta = 0.8

evPower = np.zeros(env.var['evNumber'])
lamda = np.zeros(99)
mu = np.zeros(99)
allEVpower = {}
for t in tqdm(range(0, 60)):
    
    lamda*=0
    mu*=0
    
    # Performing load flow for the first time step
    DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], env.var['evNodeNumber'], 0*evPower)

    # get the transformer power magnitudes
    transPowers = GetTransPower.getTransPower(DSSCircuit)
    
    transPowers = np.ravel(transPowers)
    
    # Available Capacity: 
    A = [env.var['transRating'][i>>1] - np.sqrt(transPowers[i]*transPowers[i]+transPowers[i+1]*transPowers[i+1]) for i in range(0,len(transPowers),2)]
    A = np.maximum(0.0, np.ravel(A))

    connected, urgent, laxity, evMatrix = env.update(d,t,evPower)
    evPower*=0
    l = len(connected)
    if l==0:
        continue
    # Upper Bound:
    UB = np.minimum(env.var['remainingDemand'], env.var['maxRate'])
    UB = [UB[c] for c in connected]
    
    x = np.zeros(l)
    prevX = x
    y = np.zeros(l)
    for s in range(100):
        DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], env.var['evNodeNumber'], evPower)

        # get the transformer power magnitudes
        transPowers = GetTransPower.getTransPower(DSSCircuit)
        
        transPowers = np.ravel(transPowers)
        
        # Available Capacity: 
        A = [env.var['transRating'][i>>1] - np.sqrt(transPowers[i]*transPowers[i]+transPowers[i+1]*transPowers[i+1]) for i in range(0,len(transPowers),2)]
        A = np.maximum(0.0, np.ravel(A))
        
        direction = np.dot(evMatrix, x)
        
        lamda = np.maximum(0.0,lamda - gamma1*(A-direction))
        mu = np.maximum(0.0, mu - gamma2*(theta*A-direction))
        #print(lamda)
        direction = np.dot(evMatrix.T, mu)
        aux.w_update(laxity, urgent)
        y = np.minimum(aux.w*util.reciprocal(direction), UB)
        
        direction = np.dot(evMatrix.T, lamda)
        x = np.minimum(np.maximum(y, util.reciprocal(direction)), UB)
        #if np.linalg.norm(prevX-x) <= tol:
        #    break
        prevX = x
        for c in range(0, l):
            evPower[connected[c]] += x[c]
        _,_,_,_ = env.update(d,t,evPower)
        UB = np.minimum(env.var['remainingDemand'], env.var['maxRate'])
        UB = [UB[c] for c in connected]
        #print(env.var['remainingDemand'])
        
    print(evPower)
    allEVpower[t] = evPower
np.save('decentral', allEVpower)