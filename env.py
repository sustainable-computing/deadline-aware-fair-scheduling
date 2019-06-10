import numpy as np
import utility as util
import sys

var = {}

################# Environments Variables ################
# Number of EV owners in the network
evNumber = 1000  
var['evNumber'] = evNumber

# Number of low voltage nodes in the network
secondaryNodes = 1760
var['secondaryNodes'] = secondaryNodes

# EV connection points
evNodeNumber = np.array(range(0, secondaryNodes))
np.random.shuffle(evNodeNumber)
evNodeNumber = evNodeNumber[0:evNumber]
var['evNodeNumber'] = evNodeNumber.tolist()

# Type of the driver
# Type 0: honest and accurate std=10 minutes
# Type 1: honest but not accurate std=45 minutes
# Type 2: dishonest std=60 minutes
evDriverType = np.random.randint(0, 3, evNumber)
var['evDriverType'] = evDriverType.tolist()

# Std for type: 0, 1, 2
evDriverStd = [0.1, 0.75, 1.0]


# GMMs for arrival times
probArrival = [.016, .244, .037, .064, .135, .454, .05]
meanArrival = [0, 2.5, 7.4, 8.5, 12.28, 18.4, 22.21]
stdArrival = [.09, 2.38, .9, 1.6, 1.4, 2.38, .35]

# Defining the Gaussian model for each EV
evGaussian = [0]*evNumber
for e in range(0,evNumber):
    rnd = np.random.rand(1)
    if rnd < probArrival[0]:
        evGaussian[e] = 0
    elif rnd < sum(probArrival[0:2]):
        evGaussian[e] = 1
    elif rnd < sum(probArrival[0:3]):
        evGaussian[e] = 2
    elif rnd < sum(probArrival[0:4]):
        evGaussian[e] = 3
    elif rnd < sum(probArrival[0:5]):
        evGaussian[e] = 4
    elif rnd < sum(probArrival[0:6]):
        evGaussian[e] = 5
    else:
        evGaussian[e] = 6


# Battery sizes
# 16kWh: Chevy Volt, Mitsubishi iMiEV
# 30kWh: Nissan Leaf
# 42kWh: BMW i3
# 75kWh: Tesla 3
batterySize = [16, 30, 42, 75]

# Type of each EV's battery
evBatteryType = np.random.randint(0, len(batterySize), evNumber)


# Initial charge of each EV at the time connection in percentage
evInitCharge = np.random.randint(0, 96, evNumber)

# Demand of each EV in kWh
demand = np.array([(1.0-evInitCharge[e]/100.0)*batterySize[evBatteryType[e]] for e in range(0, evNumber)])
var['demand'] = demand.tolist()

# Arrival time, duration and claimed duration of each EV in hour
evArrival = np.zeros(evNumber)
evDuration = np.zeros(evNumber)
evClaimedDuration = np.zeros(evNumber)

# EVs' schedules 
for e in range(0, evNumber):
    # Arrival time in hour
    evArrival[e] = np.random.normal(meanArrival[evGaussian[e]], stdArrival[evGaussian[e]])%24
    # Duration of connection in hour
    evDuration[e] = np.random.normal(8,2)
    if evDuration[e] < 1:
        evDuration[e] = 1
    elif evDuration[e] > 14:
        evDuration[e] = 14
    # Claimed duration in hour
    if evDriverType[e] < 2:
        # Honest driver
        evClaimedDuration[e] = evDuration[e]+np.random.normal(0, evDriverStd[evDriverType[e]])
    else:
        # Dishonest driver
        evClaimedDuration[e] = evDuration[e]-abs(np.random.normal(0, evDriverStd[evDriverType[e]]))
    if evClaimedDuration[e] < 1:
        evClaimedDuration[e] = 1

var['evArrival'] = np.round(evArrival*3600).tolist()
var['evClaimedDuration'] = np.round(evClaimedDuration*3600).tolist()
var['evDuration'] = np.round(evDuration*3600).tolist()

# Discrepancy for different types of EV  
discp_type = [0, 2700, 3600] # In second
var['discrepancy'] = [discp_type[evDriverType[i]] for i in range(0, evNumber)] 


# Transformer rating for each phase in kVA
transRating=[2000,2000,2000,75,75,75,50,50,50,75,75,75,37.5,37.5,37.5,37.5,37.5,37.5,166.6666667,166.6666667,
166.6666667,100,100,100,37.5,37.5,37.5,50,50,50,37.5,37.5,37.5,37.5,37.5,37.5,25,25,25,75,75,75,37.5,37.5,37.5,
37.5,37.5,37.5,50,50,50,50,50,50,75,75,75,75,75,75,75,75,75,85,85,85,85,85,85,250,250,250,250,250,250,50,50,50,
37.5,37.5,37.5,50,50,50,75,75,75,100,100,100,100,100,100,166.6666667,166.6666667,166.6666667,37.5,37.5,37.5]
var['transRating'] = transRating

# Phase number for each load
loadPhase =[1,2,1,1,1,2,2,3,1,2,2,3,2,1,2,3,3,3,3,1,1,1,2,3,1,2,3,3,1,1,1,3,3,1,2,2,2,2,3,2,2,3,3,2,2,1,3,1,1,2,1,1,2,1,1]
var['loadPhase'] = loadPhase

if __name__=="__main__":
    env_file = 'env/default_env.txt'
    if len(sys.argv)>1:
        env_file = 'env/' + sys.argv[1] + '.txt'
    util.save_dict(env_file, var)
