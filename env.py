import numpy as np
import sys

class env:
    def __init__(self, arg=None):
        self.var = {}
        if arg != None:
            self.var = np.load(arg).item()
            return

        # Creating EVs
        evNumber = 10  # number of EV owners in our network
        self.var['evNumber'] = evNumber
        
        days = 7  # number of simulation days
        self.var['days'] = days
        
        # GMMs for arrival times
        probArrival = [.016, .244, .037, .064, .135, .454, .05]
        meanArrival = [0, 2.5, 7.4, 8.5, 12.28, 18.4, 22.21]
        stdArrival = [.09, 2.38, .9, 1.6, 1.4, 2.38, .35]
        
        self.var['probArrival '] = probArrival 
        self.var['meanArrival'] = meanArrival
        self.var['stdArrival'] = stdArrival
        
        
        # EV parameters
        secondaryNodes = 1760  # number of low voltage nodes of the network
        self.var['secondaryNodes'] = secondaryNodes
        
        evNodeNumber = np.array(range(0, secondaryNodes))
        np.random.shuffle(evNodeNumber)
        evNodeNumber = evNodeNumber[0:evNumber]
        
        self.var['evNodeNumber'] = evNodeNumber
        
        # defining the Gaussian model for each EV
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
                
        self.var['evGaussian'] = evGaussian

        # Battery sizes
        # 16kWh: Chevy Volt, Mitsubishi iMiEV
        # 30kWh: Nissan Leaf
        # 42kWh: BMW i3
        # 75kWh: Tesla 3
        batterySize = [16, 30, 42, 75]
        self.var['batterySize'] = batterySize
        
        evBatteryType = np.random.randint(0, len(batterySize), evNumber)  # type of each EV's battery
        self.var['evBatteryType'] = evBatteryType
        
        # type of the driver
        # type 0: honest and accurate std=10 minutes
        # type 1: honest but not accurate std=45 minutes
        # type 2: dishonest std=60 minutes
        evDriverType = np.random.randint(0, 3, evNumber)
        self.var['evDriverType'] = evDriverType
        
        evDriverStd = [0, .75, 1]
        self.var['evDriverStd'] = evDriverStd

        # initial charge of each EV at the time connection in percentage
        evInitCharge = np.random.randint(0, 96, (days, evNumber))
        self.var['evInitCharge'] = evInitCharge
        
        # creating empty arrays for storing arrival times, duration and claimed duration for each EV
        evArrival = np.zeros(shape=(days, evNumber))
        evDuration = np.zeros(shape=(days, evNumber))
        evClaimedDuration = np.zeros(shape=(days, evNumber))

        # EVs' schedules for the first day
        for e in range(0, evNumber):
            # arrival time
            evArrival[0, e] = round(np.random.normal(meanArrival[evGaussian[e]], stdArrival[evGaussian[e]]))%24
            # duration of connection
            evDuration[0, e] = round(np.random.normal(8,2))
            if evDuration[0, e] < 1:
                evDuration[0, e] = 1
            elif evDuration[0, e] > 14:
                evDuration[0, e] = 14
            # claimed duration
            if evDriverType[e] < 2:
                # honest driver
                evClaimedDuration[0, e] = round(evDuration[0, e]+np.random.normal(0, evDriverStd[evDriverType[e]]))
            else:
                # dishonest driver
                evClaimedDuration[0, e] = round(evDuration[0, e]-abs(np.random.normal(0, evDriverStd[evDriverType[e]])))
            if evClaimedDuration[0, e] < 1:
                evClaimedDuration[0, e] = 1

        # EVs' schedules for the next days
        for d in range(1, days):
            for e in range(0, evNumber):
                # arrival time
                evArrival[d, e] = 24*(d-1)+round(np.random.normal(meanArrival[evGaussian[e]], stdArrival[evGaussian[e]]) % 24)
                while evArrival[d, e] <= evArrival[d-1, e]+evDuration[d-1, e]:
                    evArrival[d, e] += 1
                # duration of connection
                evDuration[d, e] = round(np.random.normal(8, 2))
                if evDuration[d, e] < 1:
                    evDuration[d, e] = 1
                elif evDuration[d, e] > 14:
                    evDuration[d, e] = 14
                # claimed time
                if evDriverType[e] < 2:
                    # honest driver
                    evClaimedDuration[d, e] = round(evDuration[d, e] + np.random.normal(0, evDriverStd[evDriverType[e]]))
                else:
                    # dishonest driver
                    evClaimedDuration[d, e] = round(evDuration[d, e] - abs(np.random.normal(0, evDriverStd[evDriverType[e]])))
                if evClaimedDuration[d, e] < 1:
                    evClaimedDuration[d, e] = 1
        
        self.var['timeUnit'] = 60 # seconds
        unitsIn1Hour = 3600/self.var['timeUnit']
        
        evArrival*=unitsIn1Hour
        evClaimedDuration*=unitsIn1Hour
        evDuration*=unitsIn1Hour
        
        self.var['evArrival'] = evArrival
        self.var['evClaimedDuration'] = evClaimedDuration
        self.var['evDuration'] = evDuration
        
        self.var['currentDay'] = -1

        # Discrepancy:
        discrepancy = np.zeros(shape=(days, evNumber))
        for i in range(1, days):
            for j in range(0, i):
                discrepancy[i] += np.maximum(evDuration[j] - evClaimedDuration[j], 0.0)
            discrepancy[i]/=i
            
        self.var['discrepancy'] = discrepancy

        # Transformer ratings for each phase
        transRating=[2000,2000,2000,75,75,75,50,50,50,75,75,75,37.5,37.5,37.5,37.5,37.5,37.5,166.6666667,166.6666667,
        166.6666667,100,100,100,37.5,37.5,37.5,50,50,50,37.5,37.5,37.5,37.5,37.5,37.5,25,25,25,75,75,75,37.5,37.5,37.5,
        37.5,37.5,37.5,50,50,50,50,50,50,75,75,75,75,75,75,75,75,75,85,85,85,85,85,85,250,250,250,250,250,250,50,50,50,
        37.5,37.5,37.5,50,50,50,75,75,75,100,100,100,100,100,100,166.6666667,166.6666667,166.6666667,37.5,37.5,37.5]
        
        self.var['transRating'] = transRating
        
        # Phase # for each load
        loadPhase =[1,2,1,1,1,2,2,3,1,2,2,3,2,1,2,3,3,3,3,1,1,1,2,3,1,2,3,3,1,1,1,3,3,1,2,2,2,2,3,2,2,3,3,2,2,1,3,1,1,2,1,1,2,1,1]
        
        self.var['loadPhase'] = loadPhase
        self.var['maxRate'] = 50*np.ones(evNumber)

    def update(self, currentDay, currentTime, prevEVPower):
        # Retrieve
        evNumber = self.var['evNumber']
        evNodeNumber = self.var['evNodeNumber']
        evArrival = self.var['evArrival']
        evDuration = self.var['evDuration']
        evClaimedDuration = self.var['evClaimedDuration']
        evInitCharge = self.var['evInitCharge']
        evBatteryType = self.var['evBatteryType']

        batterySize = self.var['batterySize']
        loadPhase = self.var['loadPhase']
        discrepancy = self.var['discrepancy']

        # Initial Remaining Demand:
        if self.var['currentDay'] != currentDay:
            remainingDemand = np.zeros(evNumber)
            for i in range(0,evNumber):
                remainingDemand[i] = (1.0 - evInitCharge[currentDay][i]/100.0)*batterySize[evBatteryType[i]]

            unitsIn1Hour = 3600/self.var['timeUnit']
            remainingDemand*=unitsIn1Hour # kWmin
            self.var['remainingDemand'] = remainingDemand
            self.var['currentDay'] = currentDay
            # Maximum Rate
            # self.var['maxRate'] = remainingDemand

        # Remaining Demand Update:
        self.var['remainingDemand']-=prevEVPower
        remainingDemand = self.var['remainingDemand']
        maxRate = self.var['maxRate']
        
        # Connected EVs
        temp = []
        for i in range(0, evNumber):
            if evArrival[currentDay][i]<=currentTime and currentTime<=evArrival[currentDay][i]+evDuration[currentDay][i] and remainingDemand[i]>=0.0:
                temp.append(i)
        connected = np.array(temp)
        
        # Urgent Connected EVs
        urgent = np.zeros(len(connected))
        for i in range(len(urgent)):
            if evArrival[currentDay][connected[i]]+evClaimedDuration[currentDay][connected[i]] == currentTime+1:
                urgent[i] = 1
                
        # EV Matrix
        l = len(connected)
        evMatrix = np.zeros(shape=(99, l))

        for c in range(0, l):
            n = evNodeNumber[connected[c]]
            t = n//55+1
            p = loadPhase[n%55]-1
            evMatrix[3*t+p, c] = 1
            evMatrix[p, c] = 1
        
        
        # Laxity:
        laxity = evArrival[currentDay] + evClaimedDuration[currentDay] - currentTime + discrepancy[currentDay] - remainingDemand/maxRate
        laxity = [laxity[c] for c in connected]

        return (connected, urgent, laxity, evMatrix)
    
    def save(self,arg):
        np.save(arg, self.var)
if __name__=="__main__":
    env().save('default')
