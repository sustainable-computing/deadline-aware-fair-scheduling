# import numpy as np
import DSSStartup
import scipy.io as spio
import numpy as np
import sys
import GetTransCurrent
# import GetTransPower
import RunPF
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
evNumber = 1000  # number of EV owners in our network
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

# setting up the initial EV powers to zero, as we assume no EV is connected at the beginning of simulation
evPower = np.zeros(evNumber)
timeStep = 60  # seconds
for t in range(0, len(P[0,:])):
    # Performing load flow for the first time step
    DSSCircuit = RunPF.runPF(DSSObj, P[:, t], Q[:, t], evNodeNumber, evPower)

    # get the transformer current magnitudes
    transCurrents = GetTransCurrent.getTransCurrent(DSSCircuit)
    
    # build the evMatrix for the current time-step
    # (a more efficient way is to just update this at each time-step)
    evMatrix = np.zeros(shape=(evNumber, len(transCurrents)))
    # now we need to find which EVs are connected to the grid
    for e in range(0, evNumber):
        currentTime = t*timeStep/3600  #hours
        d = days-1
        flag = 0
        while flag == 0 and d >= 0:
            if currentTime >= evArrival[d,e]:
                flag = 1
            else:
                d -= 1
        if d >= 0:
            if currentTime-evArrival[d,e] <= evDuration[d,e]:
                # this EV is connected
                evMatrix[e, 0] = 1  # main transformer
                evMatrix[e, evNodeNumber[e]//55+1] = 1  # secondary transformers

    # now we need to define the EV charging power "evPower" for the next time-step
    # Available resource: 
    A = [ratings[i]-np.sum(P[i*55-55:i*55-1, t]) for i in range(0,evNumber)]
    
    # Truthful factors




