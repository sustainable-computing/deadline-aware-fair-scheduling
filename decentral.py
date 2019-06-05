import util
import aux
import env
import numpy as np
import sys
import GetTransPower
import RunPF


DSSObj, mat, env = util.load(sys.argv)

P = mat['P']  # real power at the secondary nodes in kW
Q = mat['Q']  # reactive power in kVar


#d = env.var['days']-5
d = 0
epsilon = 1e-8
tol=1e-3

maxIteration=2000

gamma1 = 0.0001
gamma2 = 0.0001
theta = 0.95

evPower = np.zeros(env.var['evNumber'])
lamda = np.zeros(99)
mu = np.zeros(99)

for t in range(1000, len(P[0,:])):
    
    lamda*=0
    mu*=0
    
    # Performing load flow for the first time step
    DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], env.var['evNodeNumber'], 0*evPower)

    # get the transformer power magnitudes
    transPowers = GetTransPower.getTransPower(DSSCircuit)
    
    transPowers = np.ravel(transPowers)
    
    # Available Capacity: 
    A = [env.var['transRating'][i>>1] - np.sqrt(transPowers[i]*transPowers[i]+transPowers[i+1]*transPowers[i+1]) for i in range(0,len(transPowers),2)]
    A = np.ravel(A)

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
    for s in range(maxIteration):
        direction = np.dot(evMatrix, x)
        lamda = np.maximum(epsilon,lamda - gamma1*(A-direction))
        mu = np.maximum(epsilon, mu - gamma2*(theta*A-direction))
        
        direction = np.dot(evMatrix.T, mu)
        aux.w_update(laxity, urgent)
        y = np.minimum(np.maximum(epsilon, aux.w*np.reciprocal(direction)), UB)
        
        direction = np.dot(evMatrix.T, lamda)
        x = np.minimum(np.maximum(y, np.reciprocal(direction)), UB)
        if np.linalg.norm(prevX-x) <= tol:
            break
        prevX = x
    for c in range(0, l):
        evPower[connected[c]] = x[c]
