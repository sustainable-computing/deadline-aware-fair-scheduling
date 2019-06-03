# import numpy as np
import DSSStartup
import scipy.io as spio
import numpy as np
import sys
import GetTransCurrent
import GetTransPower
import RunPF
import aux
import primal
import baseline
# import pickle

# the file that has the dss description:
dss_path = 'master33Full.dss'         # use loadTopologyIEEE13woSwitch
print(dss_path)
DSSObj = DSSStartup.dssstartup(dss_path)

# loading the aggregated loads at the secondary nodes
mat = spio.loadmat('secAggLoads.mat', squeeze_me=True)

P = mat['P']  # real power at the secondary nodes in kW
Q = mat['Q']  # reactive power in kVar

# Creating EVs
evNumber = 10  # number of EV owners in our network
days = 7  # number of simulation days
# GMMs for arrival times
probArrival = [.6, .1, .3]
meanArrival = [8, 13, 18]
stdArrival = [1, 2, 1]
# EV parameters
secondaryNodes = 1760  # number of low voltage nodes of the network
evNodeNumber = np.random.random_integers(0, secondaryNodes-1, evNumber)
evGaussian = [0]*evNumber
# defining the Gaussian model for each EV
for e in range(0,evNumber):
    rnd = np.random.rand(1)
    if rnd < probArrival[0]:
        evGaussian[e] = 0
    elif rnd < probArrival[0]+probArrival[1]:
        evGaussian[e] = 1
    else:
        evGaussian[e] = 2

# Battery sizes
# 16kWh: Chevy Volt, Mitsubishi iMiEV
# 30kWh: Nissan Leaf
# 42kWh: BMW i3
# 75kWh: Tesla 3
batterySize = [16, 30, 42, 75]
evBatteryType = np.random.random_integers(0, len(batterySize)-1, evNumber)  # type of each EV's battery

# type of the driver
# type 0: honest and accurate std=10 minutes
# type 1: honest but not accurate std=45 minutes
# type 2: dishonest std=60 minutes
evDriverType = np.random.random_integers(0, 2, evNumber)
evDriverStd = [.17, .75, 1]

# initial charge of each EV at the time connection in percentage
evInitCharge = np.random.random_integers(0, 95, (days, evNumber))

# creating empty arrays for storing arrival times, duration and claimed duration for each EV
evArrival = np.zeros(shape=(days, evNumber))
evDuration = np.zeros(shape=(days, evNumber))
evClaimedDuration = np.zeros(shape=(days, evNumber))

# EVs' schedules for the first day
for e in range(0, evNumber):
    # arrival time
    evArrival[0, e] = np.random.normal(meanArrival[evGaussian[e]], stdArrival[evGaussian[e]])%24
    # duration of connection
    evDuration[0, e] = np.random.normal(8,2)
    if evDuration[0, e] < 1:
        evDuration[0, e] = 1
    elif evDuration[0, e] > 14:
        evDuration[0, e] = 14
    # claimed duration
    if evDriverType[e] < 2:
        # honest driver
        evClaimedDuration[0, e] = evDuration[0, e]+np.random.normal(0, evDriverStd[evDriverType[e]])
    else:
        # dishonest driver
        evClaimedDuration[0, e] = evDuration[0, e]-abs(np.random.normal(0, evDriverStd[evDriverType[e]]))
    if evClaimedDuration[0, e] < 1:
        evClaimedDuration[0, e] = 1

# EVs' schedules for the next days
for d in range(1, days):
    for e in range(0, evNumber):
        # arrival time
        evArrival[d, e] = 24*(d-1)+np.random.normal(meanArrival[evGaussian[e]], stdArrival[evGaussian[e]]) % 24
        while evArrival[d, e] <= evArrival[d-1, e]+evDuration[d-1, e]:
            evArrival[d, e] += 1
        # duration of connection
        evDuration[d, e] = np.random.normal(8, 2)
        if evDuration[d, e] < 1:
            evDuration[d, e] = 1
        elif evDuration[d, e] > 14:
            evDuration[d, e] = 14
        # claimed time
        if evDriverType[e] < 2:
            # honest driver
            evClaimedDuration[d, e] = evDuration[d, e] + np.random.normal(0, evDriverStd[evDriverType[e]])
        else:
            # dishonest driver
            evClaimedDuration[d, e] = evDuration[d, e] - abs(np.random.normal(0, evDriverStd[evDriverType[e]]))
        if evClaimedDuration[d, e] < 1:
            evClaimedDuration[d, e] = 1

evArrival*=60
evClaimedDuration*=60
evDuration*=60

# Remaining Demand:
remain = np.zeros(shape=(days, evNumber))
for i in range(0,days):
    for j in range(0,evNumber):
        remain[i][j] = (1.0 - evInitCharge[i][j]/100.0)*batterySize[evBatteryType[j]]
remain*=60.0

# Discrepancy:
discrepancy = np.zeros(shape=(days, evNumber))
for i in range(1, days):
    for j in range(0, i):
        discrepancy[i] += np.maximum(evDuration[j] - evClaimedDuration[j], 0.0)
    discrepancy[i]/=i

# Maximum Rate
maxRate = remain

# Laxity:
Laxity = evClaimedDuration + discrepancy - remain/maxRate

# Transformer ratings for each phase
transRating=[2000,2000,2000,75,75,75,50,50,50,75,75,75,37.5,37.5,37.5,37.5,37.5,37.5,166.6666667,166.6666667,
166.6666667,100,100,100,37.5,37.5,37.5,50,50,50,37.5,37.5,37.5,37.5,37.5,37.5,25,25,25,75,75,75,37.5,37.5,37.5,
37.5,37.5,37.5,50,50,50,50,50,50,75,75,75,75,75,75,75,75,75,85,85,85,85,85,85,250,250,250,250,250,250,50,50,50,
37.5,37.5,37.5,50,50,50,75,75,75,100,100,100,100,100,100,166.6666667,166.6666667,166.6666667,37.5,37.5,37.5]

# Phase # for each load
loadPhase =[1,2,1,1,1,2,2,3,1,2,2,3,2,1,2,3,3,3,3,1,1,1,2,3,1,2,3,3,1,1,1,3,3,1,2,2,2,2,3,2,2,3,3,2,2,1,3,1,1,2,1,1,2,1,1]

timeStep = 60  # seconds
d = days-1
epsilon = 1e-8
for t in range(0, len(P[0,:])):
    # Performing load flow for the first time step
    evPower = np.zeros(evNumber)
    DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], evNodeNumber, evPower)

    # get the transformer power magnitudes
    transPowers = GetTransPower.getTransPower(DSSCircuit)
    transPowers = np.ravel(transPowers)
    
    # Available Capacity: 
    A = [transRating - 0*np.sqrt(transPowers[i]*transPowers[i]+transPowers[i+1]*transPowers[i+1]) for i in range(0,2,len(transPowers))]
    A = np.ravel(A)

    # Urgent EVs:
    urgent = np.zeros(evNumber)
    for i in range(0, evNumber):
        if remain[d][i] > epsilon and evClaimedDuration[d][i] <= 1:
            urgent[i] = 1
    # Upper Bound:
    UB = np.minimum(remain[d], maxRate[d])
    
    # build the evMatrix for the current time-step
    # (a more efficient way is to just update this at each time-step)
    evMatrix = np.zeros(shape=(evNumber, len(A)))
    # now we need to find which EVs are connected to the grid
    currentTime = t  #min
    for e in range(0, evNumber):
        """
            currentTime = t  #min
            flag = 0
            while flag == 0 and d >= 0:
                if currentTime >= evArrival[d,e]:
                    flag = 1
                else:
                    d -= 1
            if d >= 0:
        """
        if currentTime-evArrival[d,e]>=0.0 and currentTime-evArrival[d,e]<=evDuration[d,e] and remain[d][e]>epsilon:
            # this EV is connected
            evMatrix[e, loadPhase[evNodeNumber[e]%55]-1] = 1  # main transformer
            evMatrix[e, 3*(evNodeNumber[e]//55+1)+loadPhase[evNodeNumber[e]%55]-1] = 1  # secondary transformers
    
    LB = epsilon + aux.solve(Laxity[d], urgent, 0.95, UB, A, evMatrix.T)
    evPower = primal.solve(LB,UB,A,evMatrix.T)
    evClaimedDuration[d]-=1
    remain[d]-=evPower
    #print(baseline.algo(Laxity[d],A,UB,evNodeNumber,loadPhase))
    #sys.exit()
    

