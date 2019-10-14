import numpy as np
import utility as util
import sys

var = {}

################# Environments Variables ################
# Number of EV owners in the network
evNumber = 54
var['evNumber'] = evNumber

# Number of low voltage nodes in the network
secondaryNodes = 1760
var['secondaryNodes'] = secondaryNodes

# EV connection points

#evNodeNumber = np.array(range(0, secondaryNodes))
#np.random.shuffle(evNodeNumber)
#evNodeNumber = evNodeNumber[0:evNumber]

evNodeNumber = np.array(range(0, evNumber))
var['evNodeNumber'] = evNodeNumber.tolist()

# Type of the driver
# Type 0: conservative: claimed duration = actutal duration + std(1 hour)
# Type 1: honest risk-taker: claimed duration = actual duration - std(1 hour) 
#X Type 2: dishonest risk-taker: claimed duration = actual duration - std(45 min)
#evDriverType = np.random.randint(0, 3, evNumber)

#evDriverType = np.random.randint(0, 2, evNumber)
evDriverType = np.array([0 if i<(evNumber/2) else 1 for i in range(evNumber)])
#evDriverType = np.zeros(evNumber, dtype=int)
#evDriverType = np.ones(evNumber, dtype=int)
var['evDriverType'] = evDriverType.tolist()

# Std for type: 0, 1, 2
#evDriverStd = [1.0, 0.20, 0.45]
evDriverStd = [3.0, 3.0]


# GMMs for arrival times
probArrival = [.016, .244, .037, .064, .135, .454, .05]
meanArrival = [0.0, 2.5, 7.4, 8.5, 12.28, 18.4, 22.21]
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
batterySize = np.array([16, 30, 42, 75])*60.0 # in kWmin

# Type of each EV's battery
#evBatteryType = np.random.randint(0, len(batterySize), evNumber)
evBatteryType = 1*np.ones((evNumber,), dtype=int)

battery = [batterySize[i] for i in evBatteryType]
var['battery'] = battery


# Initial charge of each EV at the time connection in percentage
#evInitCharge = np.random.randint(0, 3, evNumber)
evInitCharge = 3*np.ones(evNumber)
# Demand of each EV in kWh
demand = np.array([(1.0-evInitCharge[e]/100.0)*batterySize[evBatteryType[e]] for e in range(0, evNumber)])
var['demand'] = demand.tolist()

# Arrival time, duration and claimed duration of each EV in hour
'''
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
    if evDriverType[e] < 1:
        # Conservative driver
        evClaimedDuration[e] = evDuration[e]+abs(np.random.normal(0, evDriverStd[evDriverType[e]]))
    else:
        # Risk-Taker driver
        evClaimedDuration[e] = evDuration[e]-abs(np.random.normal(0, evDriverStd[evDriverType[e]]))
    if evClaimedDuration[e] < 1:
        evClaimedDuration[e] = 1
'''

evArrival = 9*np.ones(evNumber)
evClaimedDuration = 8*np.ones(evNumber)
evDuration = np.array([7 if i<(evNumber/2) else 9 for i in range(evNumber)])

# in min
var['evArrival'] = np.round(evArrival*60).tolist()
var['evClaimedDuration'] = np.round(evClaimedDuration*60).tolist()
var['evDuration'] = np.round(evDuration*60).tolist()

# Discrepancy for different types of EV  
#discp_type = [0, 2700, 3600] # In minutes
#var['discrepancy'] = [discp_type[evDriverType[i]] for i in range(0, evNumber)] 
#discrepancy = evDuration - evClaimedDuration
discrepancy = np.array([-2 if i<(evNumber/2) else 2 for i in range(evNumber)])
var['discrepancy'] = np.round(discrepancy*60).tolist()
# Transformer rating for each phase in kVA
transRating=[2500,2500,2500,100,100,100,100,100,100,100,100,100,75,75,75,75,75,75,166.67,166.67,166.67,166.67,166.67,
166.67,50,50,50,75,75,75,75,75,75,75,75,75,75,75,75,100,100,100,75,75,75,75,75,75,50,50,50,100,100,100,100,100,100,75,
75,75,100,100,100,100,100,100,100,100,100,333.33,333.33,333.33,333.33,333.33,333.33,75,75,75,75,75,75,50,50,50,166.67,
166.67,166.67,166.67,166.67,166.67,166.67,166.67,166.67,166.67,166.67,166.67,50,50,50]
var['transRating'] = transRating

# Phase number for each load
loadPhase =[1,2,1,1,1,2,2,3,1,2,2,3,2,1,2,3,3,3,3,1,1,1,2,3,1,2,3,3,1,1,1,3,3,1,2,2,2,2,3,2,2,3,3,2,2,1,3,1,1,2,1,1,2,1,1]
var['loadPhase'] = loadPhase

if __name__=="__main__":
    env_file = 'env/default_env.txt'
    if len(sys.argv)>1:
        env_file = 'env/' + sys.argv[1] + '.txt'
    util.save_dict(env_file, var)
