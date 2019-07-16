import numpy as np
import utility as util
import GetTransPower
import RunPF

class algo:
    def __init__(self, DSSObj, env, P, Q, slot_len_in_min=10, start_hr=0, mode='change', params={}):
        self.DSSObj = DSSObj
        #self.P = mat['P']
        #self.Q = mat['Q']
        self.env = env
        self.mode = mode
        self.params = params
        self.P_init = P
        self.Q_init = Q
        
        self.trans_accu = 0.90
        
        self.slot_len_in_min = slot_len_in_min
        
        self.n_slot_per_hr = 60 // self.slot_len_in_min
        #self.start_slot = start_slot*slot_len_in_min
        self.current_slot = start_hr*self.n_slot_per_hr
        #self.time_factor = 3600.0/self.slot_len_in_min
        
        self.remaining_demand = 60.0*np.array(env['demand']) # In kWmin
        #self.remaining_demand_d = 60.0*np.array(env['demand']) # In kWmin

        #self.max_rate = 1+60.0*np.array(env['demand']) # In kWmin
        self.max_rate = 6.6*np.ones(env['evNumber']) # In kW

        self.arrival = np.round(np.array(self.env['evArrival'])/(60*slot_len_in_min))
        self.duration = np.round(np.array(self.env['evDuration'])/(60*slot_len_in_min))
        self.claimed_duration = np.round(np.array(self.env['evClaimedDuration'])/(60*slot_len_in_min))
        
        self.discrepancy = np.array(self.env['discrepancy'])/(60*slot_len_in_min)
        
    def get_connected(self):
        connected = []
        for i in range(0, self.env['evNumber']):
            if self.current_slot >= self.arrival[i] and self.current_slot <= self.arrival[i] + self.duration[i] and self.remaining_demand[i] > 0.0:
                connected.append(i)
        return np.array(connected)
        
    def get_over_time(self, connected):
        over_time = []
        for c in connected:
            if self.current_slot > self.arrival[c] + self.claimed_duration[c]:
                over_time.append(True)
            else:
                over_time.append(False)
        return over_time
        
    def get_claimed(self, connected):
        claimed = []
        for c in connected:
            claimed.append(self.claimed_duration[c])
        return claimed
    
    def get_urgent(self, connected):
        urgent = []
        for e in connected:
            
            if self.current_slot < self.arrival[e]+self.claimed_duration[e]:
                urgent.append(e)
        return np.array(urgent) 
        
    def get_laxity(self, urgent, scale=1.0):
        laxity = []
        for u in urgent:
            l = (self.arrival[u]+self.claimed_duration[u]-self.current_slot) + scale*self.discrepancy[u] 
            l -= (self.remaining_demand[u]/self.max_rate[u])/self.slot_len_in_min
            laxity.append(l)
        return np.array(laxity)
        
    def get_driver_type(self, connected):
        driver_type = []
        for c in connected:
            driver_type.append(self.env['evDriverType'][c])
        return np.array(driver_type)
        
    def update_remaining_demand(self, ev_power, duration):
        self.remaining_demand = np.maximum(0.0, self.remaining_demand - ev_power*duration)
        
    def get_trans_load(self, ev_power, P, Q): # In kVA
        
        if self.mode=='change':
            within_hr = int(self.current_slot % (60 // self.slot_len_in_min))
            DSSCircuit = RunPF.runPF(self.DSSObj, P[:, within_hr], Q[:, within_hr], self.env['evNodeNumber'], ev_power)
        elif self.mode=='constant':
            DSSCircuit = RunPF.runPF(self.DSSObj, self.P_init[:, 0], self.Q_init[:, 0], self.env['evNodeNumber'], ev_power)
        
        # get the transformer power magnitudes
        trans_loads = GetTransPower.getTransPower(DSSCircuit)
        trans_loads = np.ravel(trans_loads)

        trans_loads = [np.sqrt(trans_loads[i]**2+trans_loads[i+1]**2) for i in range(0,len(trans_loads),2)]
        return(np.array(trans_loads))
        
    def get_available(self, trans_loads):

        return self.trans_accu*np.maximum(0.0, np.array(self.env['transRating']) - trans_loads)
    
    def get_UB(self, connected):
        #temp = np.minimum(self.remaining_demand/self.slot_len_in_min, self.max_rate)
        temp = self.max_rate
        #temp = np.maximum(util.tol, temp)
        return np.array([temp[e] for e in connected])
        
    def get_TAU(self, connected, P, Q, whole=0):
        if whole==1:
            connected = np.array(range(0,self.env['evNumber']))
        T = []
        A = []
        U = []
        trans_number = [self.env['evNodeNumber'][e]//55+1 for e in connected]
        phase_number = [self.env['loadPhase'][self.env['evNodeNumber'][e]%55]-1 for e in connected]
        
        available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber']),P,Q))
        # For primary tranformers
        for i in range(0,3):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if phase_number[j]==i:
                    temp[j] = 1
            if np.sum(temp)>0 or whole==1:
                T.append(temp)
                A.append(available[i])
                U.append(i)
        
        # For secondary transformers
        for i in range(3, len(available)):
            temp = np.zeros(len(connected))
            for j in range(0, len(connected)):
                if trans_number[j]==(i//3) and phase_number[j]==(i%3):
                    temp[j] = 1
            if np.sum(temp)>0 or whole==1:
                T.append(temp)
                A.append(available[i])
                U.append(i)
        A = np.array(A)
        #A = np.maximum(util.tol, A)
        return (np.array(T), A, np.array(U))
            
    def update(self, P, Q):
        # Write codes for update in each time slot
        return
