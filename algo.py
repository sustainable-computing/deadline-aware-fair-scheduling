import numpy as np
import utility as util
import GetTransPower
import RunPF

class algo:
    def __init__(self, DSSObj, mat, env, time_unit_in_sec=60, start=0, mode='change', params={}):
        self.DSSObj = DSSObj
        self.P = mat['P']
        self.Q = mat['Q']
        self.env = env
        self.mode = mode
        self.params = params
        
        self.start = start*time_unit_in_sec
        self.current_time = start
        self.time_unit_in_sec = time_unit_in_sec
        self.time_factor = 3600.0/self.time_unit_in_sec
        
        self.remaining_demand = 3600.0*np.array(env['demand']) # In kWsec
        self.max_rate = 1+3600.0*np.array(env['demand']) # In kWsec

        self.arrival = np.array(self.env['evArrival'])
        self.duration = np.array(self.env['evDuration'])
        self.claimed_duration = np.array(self.env['evClaimedDuration'])
        
        self.discrepancy = np.array(self.env['discrepancy'])
        
    def get_connected(self):
        connected = []
        for i in range(0, self.env['evNumber']):
            if self.current_time >= self.arrival[i] and self.current_time <= self.arrival[i] + self.duration[i] and self.remaining_demand[i] > 0.0:
                connected.append(i)
        return np.array(connected)
    
    def get_urgent(self, connected):
        urgent = []
        for e in connected:
            if self.current_time <= self.arrival[e]+self.claimed_duration[e] and self.arrival[e]+self.claimed_duration[e] <= self.current_time+self.time_unit_in_sec:
                urgent.append(e)
        return np.array(urgent) 
        
    def get_laxity(self, urgent, scale=1.0):
        laxity = []
        for u in urgent:
            laxity.append((self.arrival[u]+self.claimed_duration[u]-self.current_time) + scale*self.discrepancy[u] - self.remaining_demand[u]/self.max_rate[u])
        return np.array(laxity)
        
    def update_remaining_demand(self, ev_power, time_in_sec):
        self.remaining_demand = np.maximum(0.0, self.remaining_demand-ev_power*time_in_sec)
        
    def get_trans_load(self, ev_power): # In kVA
        if self.mode=='change':
            DSSCircuit = RunPF.runPF(self.DSSObj, self.P[:, self.current_time], self.Q[:, self.current_time], self.env['evNodeNumber'], ev_power)
        elif self.mode=='constant':
            DSSCircuit = RunPF.runPF(self.DSSObj, self.P[:, self.start], self.Q[:, self.start], self.env['evNodeNumber'], ev_power)

        # get the transformer power magnitudes
        trans_loads = GetTransPower.getTransPower(DSSCircuit)
        trans_loads = np.ravel(trans_loads)
        trans_loads = [np.sqrt(trans_loads[i]**2+trans_loads[i+1]**2) for i in range(0,len(trans_loads),2)]
        return(np.array(trans_loads))
        
    def get_available(self, trans_loads):
        return np.maximum(0.0, self.env['transRating']-trans_loads)
    
    def get_UB(self, connected):
        temp = np.minimum(self.remaining_demand, self.max_rate)/self.time_unit_in_sec
        temp = np.maximum(util.tol, temp)
        return np.array([temp[e] for e in connected])
        
    def get_TA(self, connected):
        T = []
        A = []
        trans_number = [self.env['evNodeNumber'][e]//55+1 for e in connected]
        phase_number = [self.env['loadPhase'][self.env['evNodeNumber'][e]%55]-1 for e in connected]
        
        available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
        # For primary tranformers
        for i in range(0,3):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if phase_number[j]==i:
                    temp[j] = 1
            if np.sum(temp)>0:
                T.append(temp)
                A.append(available[i])
        
        # For secondary transformers
        for i in range(3, len(available)):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if trans_number[j]==(i//3) and phase_number[j]==(i%3):
                    temp[j] = 1
            if np.sum(temp)>0:
                T.append(temp)
                A.append(available[i])
        A = np.array(A)
        A = np.maximum(util.tol, A)
        return (np.array(T), A)
            
    def update(self):
        # Write codes for update in each time slot
        return
