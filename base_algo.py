from algo import algo 
import utility as util
import numpy as np


class base_algo(algo):

    def sort(self, connected, value):
        self.dtype = [('ev', int), ('value', float)]

        x = [(connected[i],value[i]) for i in range(0,len(value))]
        x = np.array(x, dtype=self.dtype)
        return np.sort(x, order='value')

    def svf(self, connected, value, A, UB, evNode, phase):
        power = np.zeros(len(value))
        B = np.copy(A)
        order = self.sort(connected, value)
        #print(self.params['value'])
        #print(order)
        for i in range(0,len(value)):
            index = order[i][0]
            j=phase[evNode[index]%55]-1
            k=3*(evNode[index]//55+1)+j
            if B[j]>=UB[i] and B[k]>=UB[i]:
                power[i]=UB[i]
            else:
                power[i]=np.minimum(B[j],B[k])
            B[j]-=power[i]
            B[k]-=power[i]
        return power

    def update(self):

        connected = self.get_connected()
        value = []
        
        if len(connected)>0:
            if self.params['value']=='edf':
                for c in connected:
                    value.append(self.arrival[c]+self.claimed_duration[c])
            if self.params['value']=='llf':
                value = self.get_laxity(connected, scale=0.0)

            value = np.array(value)
            
            available = self.get_available(self.get_trans_load(np.zeros(self.env['evNumber'])))
            
            x = self.svf(connected, value, available, self.get_UB(connected), self.env['evNodeNumber'], self.env['loadPhase'])
                
        ev_power = np.zeros(self.env['evNumber'])
        for i in range(0, len(connected)):
            ev_power[connected[i]] = x[i]
            
        self.update_remaining_demand(ev_power, self.time_unit_in_sec)
        result = {'trans_load':self.get_trans_load(ev_power).tolist(), 'ev_power':ev_power.tolist(), 'remaining_demand':self.remaining_demand.tolist()}
        self.current_time+=self.time_unit_in_sec
        
        if self.params['value']=='edf' and len(connected)>0:
            t,a,_=self.get_TA([],whole=1)
            print('edf')
            print(np.dot(t,ev_power))
            #print(a)
        return result
            
